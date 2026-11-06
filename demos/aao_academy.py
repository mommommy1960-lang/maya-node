"""Synthetic training records only. Not for real staff or public deployment."""
import os,sqlite3,secrets
from datetime import datetime,timezone
from flask import Flask,request,jsonify,send_from_directory
from pathlib import Path
app=Flask(__name__)
app.config["MAX_CONTENT_LENGTH"]=4096
DB=os.environ.get("MAYA_ACADEMY_DB","maya_academy_demo.sqlite")
OPERATOR_TOKEN=os.environ.get("MAYA_ACADEMY_TOKEN")
INSTRUCTOR_TOKEN=os.environ.get("MAYA_ACADEMY_INSTRUCTOR_TOKEN")
INSTRUCTOR_ID=os.environ.get("MAYA_ACADEMY_INSTRUCTOR_ID","").strip()
EXPECTED=["no","no","escalate","no","no"]
def connect():
 c=sqlite3.connect(DB);c.row_factory=sqlite3.Row
 c.execute("CREATE TABLE IF NOT EXISTS completions(id TEXT PRIMARY KEY,learner_id TEXT,role TEXT,score INTEGER,passed INTEGER,at TEXT,instructor_id TEXT)")
 return c
def instructor_authorized():
 v=request.headers.get("X-Maya-Instructor-Token","")
 return bool(INSTRUCTOR_TOKEN and len(INSTRUCTOR_TOKEN)>=24 and INSTRUCTOR_TOKEN!=OPERATOR_TOKEN and INSTRUCTOR_ID.startswith("demo-") and len(INSTRUCTOR_ID)<=64 and secrets.compare_digest(v,INSTRUCTOR_TOKEN))
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
 if not isinstance(learner,str) or not learner.startswith("demo-") or len(learner)>64 or role not in ("pantry","coordinator","approver","receiver","administrator") or not isinstance(answers,list) or len(answers)!=5 or any(not isinstance(x,str) for x in answers):
  return jsonify(error="Synthetic learner and valid answers required"),400
 score=sum(x==y for x,y in zip(answers,EXPECTED))
 passed=score==5 and data.get("practical_passed") is True and instructor_authorized()
 rid=secrets.token_hex(12)
 instructor_id=INSTRUCTOR_ID if passed else None
 with connect() as c:c.execute("INSERT INTO completions VALUES(?,?,?,?,?,?)",(rid,learner,role,score,int(passed),datetime.now(timezone.utc).isoformat(),instructor_id))
 return jsonify(id=rid,score=score,passed=passed,synthetic_only=True),201
@app.get("/api/training/records")
def records():
 if not authorized():return jsonify(error="Unauthorized"),401
 with connect() as c:return jsonify(records=[dict(x) for x in c.execute("SELECT * FROM completions ORDER BY at DESC LIMIT 100")])
if __name__=="__main__":
 if not OPERATOR_TOKEN or len(OPERATOR_TOKEN)<24:raise SystemExit("Set MAYA_ACADEMY_TOKEN")
 app.run(host="127.0.0.1",port=8766,debug=False)
