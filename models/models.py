from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Character(db.Model):
    __tablename__ = 'characters'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    status = db.Column(db.String(15))
    species = db.Column(db.String(50))
    type = db.Column(db.String(50))
    gender = db.Column(db.String(15))
    origin_name = db.Column(db.String(50))
    location_name = db.Column(db.String(50))
    image_url = db.Column(db.String(100))