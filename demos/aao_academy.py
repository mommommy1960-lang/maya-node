"""Synthetic training records only. Not for real staff or public deployment."""
import os,sqlite3,secrets,hmac,hashlib,base64,json,time
from datetime import datetime,timezone,timedelta
from flask import Flask,request,jsonify,send_from_directory
from pathlib import Path
app=Flask(__name__)
app.config["MAX_CONTENT_LENGTH"]=4096
DB=os.environ.get("MAYA_ACADEMY_DB","maya_academy_demo.sqlite")
OPERATOR_TOKEN=os.environ.get("MAYA_ACADEMY_TOKEN")
INSTRUCTOR_TOKEN=os.environ.get("MAYA_ACADEMY_INSTRUCTOR_TOKEN")
INSTRUCTOR_ID=os.environ.get("MAYA_ACADEMY_INSTRUCTOR_ID","").strip()
STAFF_SIGNING_KEY=os.environ.get("MAYA_ACADEMY_STAFF_SIGNING_KEY")
SUPERVISOR_TOKEN=os.environ.get("MAYA_ACADEMY_SUPERVISOR_TOKEN")
SUPERVISOR_ID=os.environ.get("MAYA_ACADEMY_SUPERVISOR_ID","").strip()
RETENTION_DAYS=30  # Synthetic demonstration default; real policy requires approval
EXPECTED=["no","no","escalate","no","no"]
def connect():
 c=sqlite3.connect(DB);c.row_factory=sqlite3.Row
 c.execute("CREATE TABLE IF NOT EXISTS completions(id TEXT PRIMARY KEY,learner_id TEXT,role TEXT,score INTEGER,passed INTEGER,at TEXT,instructor_id TEXT)")
 c.execute("CREATE TABLE IF NOT EXISTS access_audit(id TEXT PRIMARY KEY,actor_id TEXT,action TEXT,at TEXT)")
 return c
def instructor_authorized():
 v=request.headers.get("X-Maya-Instructor-Token","")
 return bool(INSTRUCTOR_TOKEN and len(INSTRUCTOR_TOKEN)>=24 and INSTRUCTOR_TOKEN!=OPERATOR_TOKEN and INSTRUCTOR_ID.startswith("demo-") and len(INSTRUCTOR_ID)<=64 and secrets.compare_digest(v,INSTRUCTOR_TOKEN))
def staff_identity():
 token=request.headers.get("X-Maya-Staff-Identity","")
 if not STAFF_SIGNING_KEY or len(STAFF_SIGNING_KEY)<32 or len(token)>1024:return None
 try:
  payload,sig=token.split(".",1)
  expected=hmac.new(STAFF_SIGNING_KEY.encode(),payload.encode(),hashlib.sha256).hexdigest()
  if not secrets.compare_digest(sig,expected):return None
  claims=json.loads(base64.urlsafe_b64decode(payload+"="*(-len(payload)%4)))
  if not isinstance(claims,dict) or not isinstance(claims.get("sub"),str) or not claims["sub"].startswith("demo-") or len(claims["sub"])>64:return None
  if type(claims.get("exp")) is not int or not time.time()<claims["exp"]<=time.time()+3600:return None
  return claims["sub"]
 except (ValueError,TypeError,UnicodeError,KeyError):return None

def supervisor_authorized():
 v=request.headers.get("X-Maya-Supervisor-Token","")
 return bool(SUPERVISOR_TOKEN and len(SUPERVISOR_TOKEN)>=24 and SUPERVISOR_ID.startswith("demo-") and len(SUPERVISOR_ID)<=64 and SUPERVISOR_TOKEN not in (OPERATOR_TOKEN,INSTRUCTOR_TOKEN) and secrets.compare_digest(v,SUPERVISOR_TOKEN))
def authorized():
 v=request.headers.get("Authorization","").removeprefix("Bearer ")
 return bool(OPERATOR_TOKEN and len(OPERATOR_TOKEN)>=24 and secrets.compare_digest(v,OPERATOR_TOKEN))
@app.after_request
def headers(r):
 r.headers["Cache-Control"]="no-store";r.headers["X-Content-Type-Options"]="nosniff";return r
@app.get("/academy")
def academy_page():
 return send_from_directory(Path(__file__).with_name("academy"),"index.html")
@app.post("/api/training/complete")
def complete():
 if not authorized():return jsonify(error="Unauthorized"),401
 data=request.get_json(silent=True) or {}
 learner=data.get("learner_id");role=data.get("role");answers=data.get("answers")
 if staff_identity()!=learner:return jsonify(error="Verified training identity required"),403
 if not isinstance(learner,str) or not learner.startswith("demo-") or len(learner)>64 or role not in ("pantry","coordinator","approver","receiver","administrator") or not isinstance(answers,list) or len(answers)!=5 or any(not isinstance(x,str) for x in answers):
  return jsonify(error="Synthetic learner and valid answers required"),400
 score=sum(x==y for x,y in zip(answers,EXPECTED))
 passed=score==5 and data.get("practical_passed") is True and instructor_authorized()
 rid=secrets.token_hex(12)
 instructor_id=INSTRUCTOR_ID if passed else None
 with connect() as c:c.execute("INSERT INTO completions VALUES(?,?,?,?,?,?,?)",(rid,learner,role,score,int(passed),datetime.now(timezone.utc).isoformat(),instructor_id))
 return jsonify(id=rid,score=score,passed=passed,synthetic_only=True),201
@app.post("/api/training/retention-cleanup")
def retention_cleanup():
 if not authorized() or not supervisor_authorized():return jsonify(error="Supervisor authorization required"),403
 cutoff=(datetime.now(timezone.utc)-timedelta(days=RETENTION_DAYS)).isoformat()
 with connect() as c:
  deleted=c.execute("DELETE FROM completions WHERE at < ?",(cutoff,)).rowcount
  c.execute("INSERT INTO access_audit VALUES(?,?,?,?)",(secrets.token_hex(12),SUPERVISOR_ID,"retention_cleanup_deleted_"+str(deleted),datetime.now(timezone.utc).isoformat()))
 return jsonify(deleted=deleted,synthetic_only=True),200
@app.get("/api/training/supervisor-records")
def supervisor_records():
 if not authorized() or not supervisor_authorized():return jsonify(error="Supervisor authorization required"),403
 with connect() as c:
  c.execute("INSERT INTO access_audit VALUES(?,?,?,?)",(secrets.token_hex(12),SUPERVISOR_ID,"supervisor_records_read",datetime.now(timezone.utc).isoformat()))
  records=[dict(x) for x in c.execute("SELECT * FROM completions ORDER BY at DESC LIMIT 100")]
 return jsonify(records=records,synthetic_only=True)
@app.get("/api/training/records")
def records():
 if not authorized():return jsonify(error="Unauthorized"),401
 learner=staff_identity()
 if learner is None:return jsonify(error="Verified training identity required"),403
 with connect() as c:return jsonify(records=[dict(x) for x in c.execute("SELECT * FROM completions WHERE learner_id=? ORDER BY at DESC LIMIT 100",(learner,))])
if __name__=="__main__":
 if not OPERATOR_TOKEN or len(OPERATOR_TOKEN)<24:raise SystemExit("Set MAYA_ACADEMY_TOKEN")
 app.run(host="127.0.0.1",port=8766,debug=False)
