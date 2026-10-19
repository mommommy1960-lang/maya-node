import json,sqlite3,sys
db=sqlite3.connect(sys.argv[1]);db.row_factory=sqlite3.Row
commands=json.loads(sys.stdin.read())
try:
    result=[]
    with db:
        for c in commands:
            cur=db.execute(c['sql'],c.get('values',[]))
            rows=[dict(r) for r in cur.fetchall()] if cur.description else []
            result.append({'results':rows,'meta':{'changes':max(0,cur.rowcount)}})
    print(json.dumps(result))
except Exception as e:
    print(json.dumps({'error':str(e)}));sys.exit(1)
