from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    webhook = db.Column(db.String)
    # users = db.relationship("Tracker", secondary="tracker")


class Tracker(db.Model):
    __tablename__ = "tracker"
    tracker_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    tuser_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    name = db.Column(db.String, nullable=False)
    desc = db.Column(db.String)
    type = db.Column(db.String, nullable=False)
    settings = db.Column(db.String)
    last_modified = db.Column(db.String)
    last_modified_value = db.Column(db.String)


class Log(db.Model):
    __tablename__ = "log"
    log_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    timestamp = db.Column(db.String, default=datetime.utcnow)
    ltracker_id = db.Column(
        db.Integer, db.ForeignKey("tracker.tracker_id"), nullable=False
    )
    ltype = db.Column(db.Integer, db.ForeignKey("tracker.tracker_id"), nullable=False)
    note = db.Column(db.String)
    value = db.Column(db.String, nullable=False)
