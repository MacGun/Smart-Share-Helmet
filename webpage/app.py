from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from model.kick_model import Kick

app = Flask(__name__)

#database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:134625@112.145.215.121:3306/hexpod"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db=SQLAlchemy(app)

HOST = "http://cloud.park-cloud.co19.kr:5000/"

@app.route('/', methods=['POST','GET'])
def lending():
    checks = Kick.query.all()
    if request.method == 'POST':
        name = request.form['inputName']
        phone = request.form['inputPhone']
        #user = Kick(name=name, phone=phone, lend=True)
        user = db.session.query(Kick).filter(Kick.id ==1).first()
        user.name = name
        user.phone = phone
        user.lend=True
        db.session.commit()
        return redirect(HOST+"finish", code=302)
    return render_template('lend_page.html', checks=checks, host=HOST)

@app.route('/return', methods=['POST'])
def return_kickboard():
    if request.method == 'POST':
        user = db.session.query(Kick).filter(Kick.id ==1).first()
        if user.ischarging == 1:
            user.name = ""
            user.phone = ""
            user.lend=False
            db.session.commit()
            return redirect(HOST, code=302)
        else:
            db.session.commit()
            return render_template('return_error.html', host=HOST)

@app.route('/checkCharger', methods=['GET', 'POST'])
def checkCharger():
    if request.method == 'POST':
        state = request.form['state']
        if state == '1':
            user = db.session.query(Kick).filter(Kick.id == 1).first()
            user.ischarging = 1;
            db.session.commit()
            return "Mounted."
        elif state == '0':
            user = db.session.query(Kick).filter(Kick.id == 1).first()
            user.ischarging = 0;
            db.session.commit()
            return "not Mounted."
        else:
            return "ERROR"
    elif request.method == "GET":
        state = request.args['state']
        if state == '1':
            user = db.session.query(Kick).filter(Kick.id == 1).first()
            user.ischarging = 1;
            db.session.commit()
            return "Mounted."
        elif state == '0':
            user = db.session.query(Kick).filter(Kick.id ==1 ).first()
            user.ischarging = 0;
            db.session.commit()
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
    kicks = Kick.query.all()
    print(kicks[0].helmet)
    return render_template('show_kick.html', kicks=kicks)

@app.route('/helmet', methods=["POST","GET"])
def helmet():
    if request.method == 'POST':
        try:
            state = request.form['state']
            if state == '1':
                user = db.session.query(Kick).filter(Kick.id == 1).first()
                user.helmet = 1;
                db.session.commit()
                print(user.helmet)
                return "200"
            elif state == '0':
                user = db.session.query(Kick).filter(Kick.id == 1).first()
                user.helmet = 0;
                db.session.commit()
                print(user.helmet)
                return "200"
            else:
                return "wrong value."
        except Exception as e:
            params = request.form
            print(e)
            print(params)
            return "wrong parameter."
    elif request.method == 'GET':
        try:
            state = request.args['state']
            if state == '1':
                user = db.session.query(Kick).filter(Kick.id == 1).first()
                user.helmet = 1;
                db.session.commit()
                return "200"
            elif state == '0':
                user = db.session.query(Kick).filter(Kick.id == 1).first()
                user.helmet = 0;
                db.session.commit()
                return "200"
            else:
                return "wrong value."
        except Exception as e:
            params = request.args
            print(e)
            print(params)
            return "wrong parameter."
    else:
        return('wrong connect from helmet api page')

if __name__ =="__main__":
    app.run(host="0.0.0.0", debug=True)
