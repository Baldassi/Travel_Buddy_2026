"""
TravelBuddy – Regression Tests
Guards against previously identified bugs resurfacing.
"""
import pytest
from models import RSVP


class TestDuplicateRSVP:
    """Bug #42 – Users could submit the same RSVP twice to the same trip."""

    def test_duplicate_rsvp_rejected(self, logged_in_client, sample_trip):
        logged_in_client.post(f"/rsvp/{sample_trip.id}", data={
            "guest_name": "Duplicate Dave",
        })
        resp = logged_in_client.post(f"/rsvp/{sample_trip.id}", data={
            "guest_name": "Duplicate Dave",
        }, follow_redirects=True)
        assert b"already registered" in resp.data

    def test_different_guests_same_trip_allowed(self, logged_in_client, sample_trip):
        logged_in_client.post(f"/rsvp/{sample_trip.id}", data={"guest_name": "Alice"})
        resp = logged_in_client.post(f"/rsvp/{sample_trip.id}", data={
            "guest_name": "Bob",
        }, follow_redirects=True)
        assert b"already registered" not in resp.data


class TestFullyBookedTrip:
    """Bug #55 – Guests could be added even when a trip was fully booked."""

    def test_cannot_rsvp_when_trip_is_full(self, logged_in_client, sample_trip, db):
        # Fill the trip to capacity (max_guests=5 from fixture)
        for i in range(sample_trip.max_guests):
            rsvp = RSVP(guest_name=f"Filler {i}", trip_id=sample_trip.id)
            db.session.add(rsvp)
        db.session.commit()

        resp = logged_in_client.post(f"/rsvp/{sample_trip.id}", data={
            "guest_name": "Late Guest",
        }, follow_redirects=True)
        assert b"fully booked" in resp.data.lower()


class TestAuthSecurity:
    """Bug #10 – Unauthenticated users could access protected routes directly."""

    def test_unauthenticated_cannot_create_trip(self, test_client):
        resp = test_client.post("/trips/create", data={
            "destination": "Hack City",
            "date": "2026-01-01",
        }, follow_redirects=True)
        # Should redirect to login, not succeed
        assert b"Hack City" not in resp.data or b"login" in resp.data.lower()

    def test_unauthenticated_cannot_add_rsvp(self, test_client, sample_trip):
        resp = test_client.post(f"/rsvp/{sample_trip.id}", data={
            "guest_name": "Ghost",
        }, follow_redirects=True)
        assert b"Ghost" not in resp.data or b"login" in resp.data.lower()


class TestDuplicateRegistration:
    """Bug #03 – Duplicate usernames/emails were accepted during registration."""

    def test_duplicate_username_rejected(self, test_client, sample_user):
        resp = test_client.post("/register", data={
            "username": "testuser",   # same as sample_user
            "email": "other@test.com",
            "password": "pass1234",
            "confirm_password": "pass1234",
        }, follow_redirects=True)
        assert b"already taken" in resp.data

    def test_duplicate_email_rejected(self, test_client, sample_user):
        resp = test_client.post("/register", data={
            "username": "newname",
            "email": "test@travelbuddy.com",  # same as sample_user
            "password": "pass1234",
            "confirm_password": "pass1234",
        }, follow_redirects=True)
        assert b"already registered" in resp.data

    def test_password_mismatch_rejected(self, test_client):
        resp = test_client.post("/register", data={
            "username": "mismatch",
            "email": "mismatch@test.com",
            "password": "pass1234",
            "confirm_password": "different",
        }, follow_redirects=True)
        assert b"do not match" in resp.data
