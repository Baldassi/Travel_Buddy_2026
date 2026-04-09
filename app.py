"""
TravelBuddy – app factory
"""
import os
from flask import Flask, session
from extensions import db, login_manager, babel

SUPPORTED_LANGUAGES = {"en_GB": "English (UK)", "pt_BR": "Português (BR)"}


def get_locale():
    return session.get("lang", "en_GB")


def create_app(testing: bool = False) -> Flask:
    app = Flask(__name__)

    # ── Configuration ────────────────────────────────────────────────────────
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "travelbuddy-dev-secret-2026")
    if testing:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///travelbuddy.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["BABEL_DEFAULT_LOCALE"] = "en_GB"
    app.config["BABEL_SUPPORTED_LOCALES"] = list(SUPPORTED_LANGUAGES.keys())

    # ── Extensions ───────────────────────────────────────────────────────────
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page."
    babel.init_app(app, locale_selector=get_locale)

    # ── User loader ───────────────────────────────────────────────────────────
    @login_manager.user_loader
    def load_user(user_id: str):
        from models import User
        return db.session.get(User, int(user_id))

    # ── Blueprints ───────────────────────────────────────────────────────────
    from routes.auth import auth_bp
    from routes.trips import trips_bp
    from routes.rsvp import rsvp_bp
    from routes.lang import lang_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(trips_bp)
    app.register_blueprint(rsvp_bp)
    app.register_blueprint(lang_bp)

    # ── Create tables ────────────────────────────────────────────────────────
    with app.app_context():
        db.create_all()

    # ── Context processor ────────────────────────────────────────────────────
    @app.context_processor
    def inject_globals():
        return {
            "supported_languages": SUPPORTED_LANGUAGES,
            "current_lang": session.get("lang", "en_GB"),
        }

    return app


if __name__ == "__main__":
    flask_app = create_app()
    print("\n  ✈  TravelBuddy is running →  http://127.0.0.1:5000\n")
    flask_app.run(debug=True)
