"""MAYA AAO food-rescue operator. Synthetic-only until explicit partner authorization.

Run: pip install flask; MAYA_AAO_OPERATOR_TOKEN=<long-random-token> python -m demos.aao_service
Do not expose directly to the public internet. Put behind TLS and a gateway.
"""
import os, json, sqlite3, time, secrets
from datetime import datetime, timezone
from flask import Flask, request, jsonify

app = Flask(__name__)
DB = os.environ.get("MAYA_AAO_DB", "maya_aao.sqlite3")
TOKEN = os.environ.get("MAYA_AAO_OPERATOR_TOKEN")
APPROVER_TOKEN = os.environ.get("MAYA_AAO_APPROVER_TOKEN")
APPROVER_ID = os.environ.get("MAYA_AAO_APPROVER_ID", "").strip()
SYNTHETIC_ONLY = os.environ.get("MAYA_AAO_SYNTHETIC_ONLY", "true").lower() != "false"
MAX_BYTES = 8192
app.config["MAX_CONTENT_LENGTH"] = MAX_BYTES

def now():
    return datetime.now(timezone.utc).isoformat()

def conn():
    c = sqlite3.connect(DB, timeout=10)
    c.row_factory = sqlite3.Row
    c.execute("PRAGMA journal_mode=WAL")
    c.execute("CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY, at TEXT NOT NULL, actor TEXT NOT NULL, kind TEXT NOT NULL, payload TEXT NOT NULL)")
    c.execute("CREATE TABLE IF NOT EXISTS cases (id TEXT PRIMARY KEY, pantry TEXT NOT NULL, item TEXT NOT NULL, quantity INTEGER NOT NULL, deadline TEXT NOT NULL, status TEXT NOT NULL, recipient TEXT, transport TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS survey (id TEXT PRIMARY KEY, at TEXT NOT NULL, role TEXT, problem TEXT NOT NULL, surplus TEXT, alert TEXT)")
    c.commit()
    return c

def record(c, actor, kind, payload):
    c.execute("INSERT INTO events(at,actor,kind,payload) VALUES(?,?,?,?)", (now(),actor,kind,json.dumps(payload,sort_keys=True)))

def auth():
    supplied = request.headers.get("Authorization","").removeprefix("Bearer ")
    return bool(TOKEN and len(TOKEN)>=24 and secrets.compare_digest(supplied,TOKEN))

def approver_auth():
    supplied = request.headers.get("X-Maya-Approver-Token", "")
    return bool(APPROVER_TOKEN and len(APPROVER_TOKEN) >= 24 and APPROVER_ID and APPROVER_TOKEN != TOKEN and secrets.compare_digest(supplied, APPROVER_TOKEN))

def fail(message,code):
    return jsonify(error=message),code

@app.after_request
def security(response):
    response.headers["Cache-Control"]="no-store"
    response.headers["X-Content-Type-Options"]="nosniff"
    response.headers["X-Frame-Options"]="DENY"
    response.headers["Referrer-Policy"]="no-referrer"
    return response

@app.get("/health")
def health():
    return jsonify(status="ok", mode="synthetic" if SYNTHETIC_ONLY else "partner-authorized", telephony="disabled", inventory_connectors="not configured")

@app.post("/api/survey")
def survey():
    if request.mimetype != "application/json": return fail("JSON required",415)
    data=request.get_json(silent=True) or {}
    if data.get("consent") is not True: return fail("Consent required",400)
    fields={k:str(data.get(k,"")).strip() for k in ("role","problem","surplus","alert")}
    if not fields["problem"] or any(len(v)>1200 for v in fields.values()): return fail("Invalid response length",400)
    # Public intake must be protected with an external rate limiter/CAPTCHA and approved privacy policy before hosting.
    if os.environ.get("MAYA_AAO_PUBLIC_SURVEY_ENABLED") != "true": return fail("Public collection disabled until privacy and abuse controls are approved",503)
    receipt=secrets.token_hex(12)
    with conn() as c:
        c.execute("INSERT INTO survey VALUES(?,?,?,?,?,?)",(receipt,now(),*(fields[k] for k in ("role","problem","surplus","alert"))))
        record(c,"survey","submission",{"receipt":receipt})
    return jsonify(receipt=receipt,status="received"),201

@app.post("/api/cases")
def create_case():
    if not auth(): return fail("Operator authorization required",401)
    data=request.get_json(silent=True) or {}
    if not SYNTHETIC_ONLY: return fail("Real inventory connector requires separate verified authorization",403)
    try:
        pantry,item,deadline=(str(data[k]).strip() for k in ("pantry","item","deadline"))
        quantity=int(data["quantity"])
        if not all((pantry,item,deadline)) or quantity<1 or quantity>100000 or max(map(len,(pantry,item,deadline)))>160: raise ValueError()
    except (KeyError,ValueError,TypeError): return fail("Invalid inventory case",400)
    case_id=secrets.token_hex(8)
    with conn() as c:
        c.execute("INSERT INTO cases VALUES(?,?,?,?,?,?,?,?)",(case_id,pantry,item,quantity,deadline,"open",None,None))
        record(c,"operator","case_opened",{"case_id":case_id,"synthetic":True})
    return jsonify(id=case_id,status="open"),201

@app.get("/api/cases")
def cases():
    if not auth(): return fail("Operator authorization required",401)
    with conn() as c: return jsonify(cases=[dict(row) for row in c.execute("SELECT * FROM cases ORDER BY deadline")])

@app.post("/api/cases/<case_id>/transition")
def transition(case_id):
    if not auth(): return fail("Operator authorization required",401)
    data=request.get_json(silent=True) or {}
    action=data.get("action")
    steps={"open":{"propose":"proposed","escalate":"escalated"},"proposed":{"approve":"approved","reject":"open","escalate":"escalated"},"approved":{"dispatch":"dispatched","escalate":"escalated"},"dispatched":{"confirm_delivery":"delivered","escalate":"escalated"},"escalated":{"propose":"proposed","cancel":"canceled"}}
    with conn() as c:
        row=c.execute("SELECT * FROM cases WHERE id=?",(case_id,)).fetchone()
        if row is None: return fail("Unknown case",404)
        nxt=steps.get(row["status"],{}).get(action)
        if not nxt: return fail("Transition not allowed",409)
        if action in ("approve","dispatch","confirm_delivery"):
            if data.get("human_approved") is not True or not approver_auth():
                return fail("Independent authenticated approver required",403)
        if action=="confirm_delivery":
            evidence=data.get("delivery_evidence")
            if not isinstance(evidence,dict) or evidence.get("synthetic") is not True or evidence.get("type") not in ("receiver_attestation","simulated_receipt") or not isinstance(evidence.get("reference"),str) or not evidence["reference"].startswith("demo-") or len(evidence["reference"])>100:
                return fail("Synthetic delivery evidence required before confirmation",400)
        recipient=str(data.get("recipient") or row["recipient"] or "")[:160]
        transport=str(data.get("transport") or row["transport"] or "")[:160]
        if action=="dispatch" and (not recipient or not transport): return fail("Recipient and transport required",400)
        c.execute("UPDATE cases SET status=?,recipient=?,transport=? WHERE id=?",(nxt,recipient,transport,case_id))
        record(c,"authorized-operator",action,{"case_id":case_id,"from":row["status"],"to":nxt,"human_approved":bool(data.get("human_approved")),"approver_id":APPROVER_ID if action in ("approve","dispatch","confirm_delivery") else None,"delivery_evidence":data.get("delivery_evidence") if action=="confirm_delivery" else None})
    return jsonify(id=case_id,status=nxt)

@app.get("/api/events")
def events():
    if not auth(): return fail("Operator authorization required",401)
    with conn() as c: return jsonify(events=[dict(r) for r in c.execute("SELECT * FROM events ORDER BY id DESC LIMIT 200")])

@app.post("/api/notify")
def notify():
    if not auth(): return fail("Operator authorization required",401)
    return fail("Calls and SMS are disabled until provider credentials, recipient opt-in, limits, and escalation roster are verified",503)

if __name__=="__main__":
    if not TOKEN or len(TOKEN)<24: raise SystemExit("Set a random MAYA_AAO_OPERATOR_TOKEN of at least 24 characters")
    app.run(host="127.0.0.1",port=int(os.environ.get("PORT","8765")),debug=False)
