from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime

class Flashcard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500), nullable=False)
    answer = db.Column(db.String(500), nullable=False)
    category = db.Column(db.String(100), nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    owner = db.relationship('User', back_populates='flashcards')
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    flashcards = db.relationship('Flashcard', back_populates='owner', cascade="all, delete-orphan")