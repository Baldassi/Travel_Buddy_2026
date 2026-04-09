from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from flask_babel import gettext as _
from extensions import db
from models import Trip

trips_bp = Blueprint("trips", __name__)


@trips_bp.route("/dashboard")
@login_required
def dashboard():
    all_trips = Trip.query.order_by(Trip.date.asc()).all()
    my_trips = Trip.query.filter_by(user_id=current_user.id).order_by(Trip.date.asc()).all()
    return render_template("dashboard.html", all_trips=all_trips, my_trips=my_trips)


@trips_bp.route("/trips/create", methods=["GET", "POST"])
@login_required
def create_trip():
    if request.method == "POST":
        destination = request.form.get("destination", "").strip()
        description = request.form.get("description", "").strip()
        date = request.form.get("date", "").strip()
        max_guests = request.form.get("max_guests", "10").strip()

        if not destination or not date:
            flash(_("Destination and date are required."), "danger")
        else:
            try:
                max_guests = int(max_guests)
            except ValueError:
                max_guests = 10

            trip = Trip(
                destination=destination,
                description=description,
                date=date,
                max_guests=max_guests,
                user_id=current_user.id,
            )
            db.session.add(trip)
            db.session.commit()
            flash(_("Trip created successfully!"), "success")
            return redirect(url_for("trips.dashboard"))

    return render_template("create_trip.html")


@trips_bp.route("/trips/<int:trip_id>")
@login_required
def trip_detail(trip_id: int):
    trip = db.get_or_404(Trip, trip_id)
    return render_template("trip_detail.html", trip=trip)


@trips_bp.route("/trips/<int:trip_id>/delete", methods=["POST"])
@login_required
def delete_trip(trip_id: int):
    trip = db.get_or_404(Trip, trip_id)
    if trip.user_id != current_user.id:
        flash(_("You can only delete your own trips."), "danger")
        return redirect(url_for("trips.dashboard"))
    db.session.delete(trip)
    db.session.commit()
    flash(_("Trip deleted."), "info")
    return redirect(url_for("trips.dashboard"))
