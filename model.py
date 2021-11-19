from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from flask_login import current_user
from sqlalchemy.orm import backref, defaultload
from sqlalchemy import ForeignKey


app = Flask(__name__)
app.secret_key = 'fefpaojpoaiefjpoiajo'  # Change this!

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.user'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=True)
    password = db.Column(db.String(32), nullable=False)
    about = db.Column(db.String(64), nullable=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32), nullable=False)
    url = db.Column(db.String(64), nullable=False)
    publish_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False )
