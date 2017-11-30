from sqlite3 import dbapi2 as mysql
import json
from flask import Flask, request, render_template

app = Flask(__name__)
db = mysql.connect("test.db", check_same_thread=False)
db.commit()
cur = db.cursor()


@app.route('/')
def index():
    return render_template('index.html')

tmp_time =0
@app.route('/data')
def data():
    global tmp_time
    if tmp_time >0:
        sql = 'select * from memory where time >%s' % (tmp_time/1000)
    else:
        sql='select * from memory'
    cur.execute(sql)
    db.commit()
    arr = []
    for i in cur.fetchall():
        arr.append([i[5] * 1000, i[3]])
    if len(arr)>0:
        tmp_time=arr[-1][0]
    return json.dumps(arr)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
