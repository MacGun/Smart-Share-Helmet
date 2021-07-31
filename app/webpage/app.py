from flask import Flask, render_template, request, redirect
import pymysql as sql
from datetime import datetime

app         = Flask(__name__)

#database configuration
DB          = sql.connect(
                user='root',
                passwd='134625',
                host='localhost',
                db='hexpod',
                charset='utf8'
            )
CUR         = DB.cursor(sql.cursors.DictCursor)
PORT        = 5000
HOST        = "http://cloud.park-cloud.co19.kr:{port}/".format(port=PORT)
TABLE_K     = "kickboard_real"
TABLE_L     = "kickboard_log"
SELECT_ALL  = {
    "table"     : TABLE_K,
    "condition" :"",
    "target"    : "*"
}
QUERY_BASIC = {
    "table"     : TABLE_K,
    "condition" : "",
}
LOG_BASIC   = {
    "table"     : TABLE_L,
    "condition" : ""
}


def get_time_stamp():
    now = datetime.now()
    return {'timestamp': now.strftime("%Y-%m-%d %H:%M:%S")}

def query(func, query_dict):
    func = func.lower()
    if func == 'select':
        MSG_FORM    = "select {target} from {table} {condition};".format(**query_dict)
    elif func == 'update':
        STMT        = ",".join(['{}={}'.format(key, value) if type(value) == type(int) else '{}="{}"'.format(key, value) for (key, value) in query_dict.items() if key != 'condition' and key != 'table'])
        MSG_FORM    = "update {table} set {stmt} {condition};".format(stmt=STMT, **query_dict)
    elif func == 'insert':
        VALUES      = '{table} ("{timestamp}",{id},"{name}","{phone}",{lend},{helmet},{ischarging}) "{condition}"'.format(**query_dict).split()
        MSG_FORM    = "insert into {table} values {values} {condition};".format(table=VALUES[0], values=VALUES[1], condition=VALUES[2])
    return MSG_FORM

def write_log():
    CUR.execute(query("select", SELECT_ALL))
    result = CUR.fetchone()
    query_dict = {
        **get_time_stamp(),
        **result,
        **LOG_BASIC
    }
    CUR.execute(query("insert", query_dict))
    DB.commit()

def get_log(rows=30):
    CUR.execute(query("select", {
                **SELECT_ALL,
                "table"     : "kickboard_log",
                "condition" : "order by timestamp desc limit {}".format(rows)
    }))
    result = CUR.fetchall()
    return result;

@app.route('/', methods=['POST','GET'])
def lending():
    CUR.execute(query('select', SELECT_ALL))
    checks = CUR.fetchone()
    if request.method == 'POST':
        data = request.form
        query_dict = {
                        **QUERY_BASIC,
                        'lend'      : 1,
                        'name'      : data['inputName'],
                        'phone'     : data['inputPhone']
                     }
        CUR.execute(query("update", query_dict))
        write_log()
        return redirect(HOST+"finish", code=302)
    return render_template('lend_page.html', checks=checks, host=HOST)

@app.route('/return', methods=['POST'])
def return_kickboard():
    if request.method == 'POST':
        CUR.execute(query("select", SELECT_ALL))
        result = CUR.fetchone()
        if result['ischarging'] == 1:
            query_dict = {
                **QUERY_BASIC,
                "name"      : "",
                "phone"     : "",
                "lend"      : 0
            }
            CUR.execute(query('update', query_dict))
            write_log()
            return redirect(HOST, code=302)
        else:
            return render_template('return_error.html', host=HOST)

@app.route('/checkCharger', methods=['GET', 'POST'])
def checkCharger():
    update = lambda state: CUR.execute(query("update", {
                    **QUERY_BASIC,
                    'ischarging': int(state)
                }))
    if request.method == 'POST':
        state = request.form['state']
        if state == '1' or state == '0':
            update(state)
            write_log()
        if state == '1':
            return "Mounted."
        elif state == '0':
            return "not Mounted."
        else:
            return "ERROR"
    elif request.method == "GET":
        state = request.args['state']
        if state == '1' or state == '0':
            update(state)
            write_log()
        if state == '1':
            return "Mounted."
        elif state == '0':
            return "not Mounted."
        else:
            return "ERROR"
    else:
        return "Error"

@app.route('/finish')
def finish():
    return render_template('finish.html')

@app.route('/admin')
def show_all():
    CUR.execute(query("select", SELECT_ALL))
    kicks = CUR.fetchone()
    return render_template('show_kick.html', kicks=kicks)

@app.route('/helmet', methods=["POST","GET"])
def helmet():
    update = lambda state: CUR.execute(query("update", {
                **QUERY_BASIC,
                "helmet": int(state)
            }))
    if request.method == 'POST':
        state = request.form['state']
        if state == '1' or state == '0':
            update(state)
            write_log()
        if state == '1':
            return "200"
        elif state == '0':
            return "200"
        else:
            return "wrong value."
            
    elif request.method == 'GET':
        state = request.args['state']
        if state == '1' or state == '0':
            update(state)
            write_log()
        if state == '1':
            return "200"
        elif state == '0':
            return "200"
        else:
            return "wrong value."
    else:
        return('wrong connect from helmet api page')

@app.route('/log', methods=['GET', 'POST'])
def showLog():
    logs = get_log()
    return render_template("log.html", logs=logs)

if __name__ =="__main__":
    app.run(host="0.0.0.0", port=PORT, debug=True)
