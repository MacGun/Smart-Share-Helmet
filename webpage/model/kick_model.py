from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Kick(db.Model):
    __tablename__ = 'kickboard'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    phone = db.Column(db.String(20))
    lend = db.Column(db.Boolean)

    def __init__(self, id,name,phone,lend):
        self.id = id
        self.name = name
        self.phone = phone
        self.lend = lend
