"""
TravelBuddy – Pytest fixtures
"""
import pytest
from app import create_app
from extensions import db as _db
from models import User, Trip, RSVP


@pytest.fixture(scope="session")
def app():
    """Create application for the test session."""
    flask_app = create_app(testing=True)
    with flask_app.app_context():
        _db.create_all()
        yield flask_app
        _db.drop_all()


@pytest.fixture(scope="function")
def db(app):
    """Provide a clean database for each test."""
    with app.app_context():
        _db.create_all()
        yield _db
        _db.session.remove()
        _db.drop_all()
        _db.create_all()


@pytest.fixture(scope="function")
def test_client(app, db):
    """Flask test client."""
    return app.test_client()


@pytest.fixture
def sample_user(db):
    """A pre-existing user in the database."""
    user = User(username="testuser", email="test@travelbuddy.com")
    user.set_password("password123")
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def sample_trip(db, sample_user):
    """A pre-existing trip owned by sample_user."""
    trip = Trip(
        destination="Edinburgh",
        description="Hogmanay celebrations",
        date="2026-12-31",
        max_guests=5,
        user_id=sample_user.id,
    )
    db.session.add(trip)
    db.session.commit()
    return trip


@pytest.fixture
def logged_in_client(test_client, sample_user):
    """A test client with sample_user already logged in."""
    test_client.post(
        "/login",
        data={"username": "testuser", "password": "password123"},
        follow_redirects=True,
    )
    return test_client
