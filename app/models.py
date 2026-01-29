from app import db
from datetime import datetime

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    attendances = db.relationship('Attendance', backref='event', lazy=True)

class Attendance(db.Model):
    __tablename__ = 'attendances'
    id = db.Column(db.Integer, primary_key=True)
    participant_name = db.Column(db.String(200), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)
