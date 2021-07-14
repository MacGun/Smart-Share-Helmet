from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Kick(db.Model):
    __tablename__ = 'kickboard_real'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    phone = db.Column(db.String(20))
    lend = db.Column(db.Boolean)
    helmet = db.Column(db.Boolean)
    ischarging = db.Column(db.Boolean)

    def __init__(self, id,name,phone,lend):
        self.id = id
        self.name = name
        self.phone = phone
        self.lend = lend
        self.helmet = helmet
        self.ischarging = ischarging
