from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from model.kick_model import Kick

app = Flask(__name__)

#database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:134625@112.145.215.121:3306/hexpod"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db=SQLAlchemy(app)

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
        return redirect("http://112.145.215.121:5000/finish", code=302)
    return render_template('lend_page.html', checks=checks)

@app.route('/return', methods=['POST'])
def return_kickboard():
    if request.method == 'POST':
        user = db.session.query(Kick).filter(Kick.id ==1).first()
        user.name = ""
        user.phone = ""
        user.lend=False
        db.session.commit()
        return redirect("http://112.145.215.121:5000", code=302)
@app.route('/finish')
def finish():
    return render_template('finish.html')

@app.route('/admin')
def show_all():
    kicks = Kick.query.all()
    return render_template('show_kick.html', kicks=kicks)

if __name__ =="__main__":
    app.run(host="0.0.0.0", debug=True)
