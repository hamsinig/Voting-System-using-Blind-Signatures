# models.py
from flask_sqlalchemy import SQLAlchemy
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Voter(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    password=db.Column(db.String(100),nullable=False)
    age = db.Column(db.Integer)
    aadhar_id = db.Column(db.String(20), unique=True)
    voter_id = db.Column(db.String(50), unique=True)
    request_sent=db.Column(db.String(50),default="No")
    role=db.Column(db.String(50),default="voter")
    blinded_msg=db.Column(db.Integer)
    msg=db.Column(db.Integer)
    r=db.Column(db.Integer)
    s=db.Column(db.Integer)
    v1=db.Column(db.Integer)
    v2=db.Column(db.Integer)
    already_voted=db.Column(db.Boolean)
    
    
    





