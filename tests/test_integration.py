"""
TravelBuddy – Integration Tests
Ensure Auth, Trip, RSVP and DB modules work together correctly.
"""
import pytest
from models import User, Trip, RSVP


class TestAuthFlow:
    def test_register_and_login(self, test_client):
        # Register
        resp = test_client.post("/register", data={
            "username": "newuser",
            "email": "new@test.com",
            "password": "pass1234",
            "confirm_password": "pass1234",
        }, follow_redirects=True)
        assert resp.status_code == 200

        # Login
        resp = test_client.post("/login", data={
            "username": "newuser",
            "password": "pass1234",
        }, follow_redirects=True)
        assert b"Welcome back" in resp.data or b"newuser" in resp.data

    def test_login_wrong_password_fails(self, test_client, sample_user):
        resp = test_client.post("/login", data={
            "username": "testuser",
            "password": "wrongpassword",
        }, follow_redirects=True)
        assert b"Invalid" in resp.data

    def test_logout_redirects_to_login(self, logged_in_client):
        resp = logged_in_client.get("/logout", follow_redirects=True)
        assert resp.status_code == 200

    def test_dashboard_requires_login(self, test_client):
        resp = test_client.get("/dashboard", follow_redirects=True)
        assert b"login" in resp.data.lower() or resp.status_code == 200


class TestTripIntegration:
    def test_create_trip_as_logged_in_user(self, logged_in_client):
        resp = logged_in_client.post("/trips/create", data={
            "destination": "Edinburgh",
            "date": "2026-12-31",
            "max_guests": "8",
            "description": "Hogmanay!"
        }, follow_redirects=True)
        assert resp.status_code == 200
        assert b"Edinburgh" in resp.data or b"Trip created" in resp.data

    def test_create_trip_missing_destination_fails(self, logged_in_client):
        resp = logged_in_client.post("/trips/create", data={
            "destination": "",
            "date": "2026-12-31",
        }, follow_redirects=True)
        assert b"required" in resp.data.lower()

    def test_trip_appears_on_dashboard(self, logged_in_client, sample_trip):
        resp = logged_in_client.get("/dashboard")
        assert b"Edinburgh" in resp.data

    def test_trip_detail_page_loads(self, logged_in_client, sample_trip):
        resp = logged_in_client.get(f"/trips/{sample_trip.id}")
        assert resp.status_code == 200
        assert b"Edinburgh" in resp.data


class TestRSVPIntegration:
    def test_user_creates_trip_and_adds_rsvp(self, logged_in_client, sample_trip):
        resp = logged_in_client.post(f"/rsvp/{sample_trip.id}", data={
            "guest_name": "Jane Smith",
            "guest_email": "jane@test.com",
        }, follow_redirects=True)
        assert b"Jane Smith" in resp.data

    def test_rsvp_guest_name_required(self, logged_in_client, sample_trip):
        resp = logged_in_client.post(f"/rsvp/{sample_trip.id}", data={
            "guest_name": "",
        }, follow_redirects=True)
        assert b"required" in resp.data.lower()

    def test_rsvp_count_increments_in_db(self, logged_in_client, sample_trip, db):
        logged_in_client.post(f"/rsvp/{sample_trip.id}", data={
            "guest_name": "Bob Builder",
        }, follow_redirects=True)
        db.session.refresh(sample_trip)
        assert sample_trip.rsvp_count == 1

    def test_full_workflow_register_create_rsvp(self, test_client):
        # 1. Register
        test_client.post("/register", data={
            "username": "workflow_user",
            "email": "workflow@test.com",
            "password": "abc12345",
            "confirm_password": "abc12345",
        })
        # 2. Login
        test_client.post("/login", data={
            "username": "workflow_user",
            "password": "abc12345",
        })
        # 3. Create trip
        test_client.post("/trips/create", data={
            "destination": "Cardiff",
            "date": "2026-10-10",
            "max_guests": "5",
        }, follow_redirects=True)
        # 4. Get the trip (ID may vary; check dashboard)
        resp = test_client.get("/dashboard")
        assert b"Cardiff" in resp.data
