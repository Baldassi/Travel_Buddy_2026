"""
TravelBuddy – Unit Tests
Isolate individual models and utility functions.
"""
import pytest
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Trip, RSVP


# ── Auth Module ──────────────────────────────────────────────────────────────

class TestPasswordHashing:
    def test_correct_password_returns_true(self):
        hashed = generate_password_hash("secure_password_123")
        assert check_password_hash(hashed, "secure_password_123") is True

    def test_wrong_password_returns_false(self):
        hashed = generate_password_hash("secure_password_123")
        assert check_password_hash(hashed, "wrong_password") is False

    def test_user_set_and_check_password(self, db):
        user = User(username="hashtest", email="hash@test.com")
        user.set_password("mypassword")
        assert user.check_password("mypassword") is True
        assert user.check_password("notmypassword") is False

    def test_password_not_stored_as_plaintext(self, db):
        user = User(username="plain", email="plain@test.com")
        user.set_password("plaintext")
        assert user.password_hash != "plaintext"


# ── Trip Module ──────────────────────────────────────────────────────────────

class TestTripModel:
    def test_trip_creation_attributes(self, db):
        trip = Trip(destination="London", date="2026-08-15", user_id=1)
        assert trip.destination == "London"
        assert trip.date == "2026-08-15"

    def test_rsvp_count_default_zero(self, db, sample_trip):
        assert sample_trip.rsvp_count == 0

    def test_spots_left_equals_max_when_empty(self, db, sample_trip):
        assert sample_trip.spots_left == sample_trip.max_guests

    def test_spots_left_decreases_with_rsvps(self, db, sample_trip):
        rsvp = RSVP(guest_name="Alice", trip_id=sample_trip.id)
        db.session.add(rsvp)
        db.session.commit()
        assert sample_trip.spots_left == sample_trip.max_guests - 1

    def test_spots_left_never_negative(self, db, sample_trip):
        for i in range(sample_trip.max_guests + 2):
            rsvp = RSVP(guest_name=f"Guest {i}", trip_id=sample_trip.id)
            db.session.add(rsvp)
        db.session.commit()
        assert sample_trip.spots_left == 0


# ── RSVP Module ──────────────────────────────────────────────────────────────

class TestRSVPModel:
    def test_rsvp_creation_attributes(self, db):
        rsvp = RSVP(guest_name="John Doe", trip_id=1)
        assert rsvp.guest_name == "John Doe"
        assert rsvp.trip_id == 1

    def test_rsvp_repr(self, db):
        rsvp = RSVP(guest_name="Jane", trip_id=2)
        assert "Jane" in repr(rsvp)
