from flask import Flask, render_template, request, redirect
import pymongo as mongo
from datetime import datetime

app         = Flask(__name__)

#database configuration
CLIENT          = mongo.MongoClient('localhost', 27017)
DB              = CLIENT['kick']
DB_KICKBOARD    = DB.kickboard_real
DB_LOG          = DB.kickboard_log

PORT        = 5000
HOST        = "http://cloud.park-cloud.co19.kr:{port}/".format(port=PORT)


def get_time_stamp():
    now = datetime.now()
    return {'date': now.strftime("%Y-%m-%d %H:%M:%S")}


def write_log():
    result = DB_KICKBOARD.find_one({})
    query   = {
        **get_time_stamp(),
        **{key:value for (key,value) in result.items() if key != '_id'}
    }
    DB_LOG.insert_one(query)

def get_log(rows=30):
    RES = DB_LOG.find({}, limit=rows)
    result = [*RES]
    return result

@app.route('/', methods=['POST','GET'])
def lending():
    checks = DB_KICKBOARD.find_one({})
    checks['date'] = checks['date'].strftime("%Y-%m-%d %H:%M:%S")
    if request.method == 'POST':
        data    = request.form
        DB_KICKBOARD.update_one({
            "id" : 1
        }, {
            "$set"  : {
                "name"  : data['inputName'],
                "phone" : data['inputPhone'],
                "lend"  : True
            }
        })
        write_log()
        return redirect(HOST+"finish", code=302)
    return render_template('lend_page.html', checks=checks, host=HOST)

@app.route('/return', methods=['POST'])
def return_kickboard():
    if request.method == 'POST':
        result = DB_KICKBOARD.find_one({})
        if result['ischarging']:
            query = {
                "name"      : None,
                "phone"     : None,
                "lend"      : False
            }
            RES = DB_KICKBOARD.update_one({"id":1}, {"$set": query})
            write_log()
            return redirect(HOST, code=302)
        else:
            return render_template('return_error.html', host=HOST)

@app.route('/checkCharger', methods=['GET', 'POST'])
def checkCharger():
    if request.method == 'POST':
        state = request.form['state']
        if state == '1' or state == '0':
            DB_KICKBOARD.update_one({"id":1}, {
                "$set" : {"ischarging" : bool(int(state))}
            })
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
            DB_KICKBOARD.update_one({"id":1}, {
                "$set" : {"ischarging" : bool(int(state))}
            })
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
    kicks = DB_KICKBOARD.find_one({})
    return render_template('show_kick.html', kicks=kicks)

@app.route('/helmet', methods=["POST","GET"])
def helmet():
    if request.method == 'POST':
        state = request.form['state']
        if state == '1' or state == '0':
            DB_KICKBOARD.update_one({"id": 1}, {
                "$set": {
                    "helmet" : bool(int(state))
                }
            })
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
            DB_KICKBOARD.update_one({"id": 1}, {
                "$set": {
                    "helmet" : bool(int(state))
                }
            })
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
