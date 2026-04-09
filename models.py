"""
TravelBuddy – SQLAlchemy models
All data is stored in travelbuddy.db (SQLite file, no external DB required).
"""
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    trips = db.relationship("Trip", backref="owner", lazy=True, cascade="all, delete-orphan")

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f"<User {self.username}>"


class Trip(db.Model):
    __tablename__ = "trips"

    id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, default="")
    date = db.Column(db.String(20), nullable=False)          # ISO date string
    max_guests = db.Column(db.Integer, default=10)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    rsvps = db.relationship("RSVP", backref="trip", lazy=True, cascade="all, delete-orphan")

    @property
    def rsvp_count(self) -> int:
        return len(self.rsvps)

    @property
    def spots_left(self) -> int:
        return max(0, self.max_guests - self.rsvp_count)

    def __repr__(self) -> str:
        return f"<Trip {self.destination} on {self.date}>"


class RSVP(db.Model):
    __tablename__ = "rsvps"

    id = db.Column(db.Integer, primary_key=True)
    guest_name = db.Column(db.String(120), nullable=False)
    guest_email = db.Column(db.String(120), default="")
    trip_id = db.Column(db.Integer, db.ForeignKey("trips.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint("guest_name", "trip_id", name="uq_guest_trip"),
    )

    def __repr__(self) -> str:
        return f"<RSVP {self.guest_name} → Trip {self.trip_id}>"
