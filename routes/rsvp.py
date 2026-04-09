from flask import Blueprint, request, redirect, url_for, flash
from flask_login import login_required
from flask_babel import gettext as _
from sqlalchemy.exc import IntegrityError
from extensions import db
from models import Trip, RSVP

rsvp_bp = Blueprint("rsvp", __name__)


@rsvp_bp.route("/rsvp/<int:trip_id>", methods=["POST"])
@login_required
def add_rsvp(trip_id: int):
    trip = db.get_or_404(Trip, trip_id)
    guest_name = request.form.get("guest_name", "").strip()
    guest_email = request.form.get("guest_email", "").strip()

    if not guest_name:
        flash(_("Guest name is required."), "danger")
        return redirect(url_for("trips.trip_detail", trip_id=trip_id))

    if trip.spots_left == 0:
        flash(_("This trip is fully booked."), "danger")
        return redirect(url_for("trips.trip_detail", trip_id=trip_id))

    rsvp = RSVP(guest_name=guest_name, guest_email=guest_email, trip_id=trip_id)
    db.session.add(rsvp)
    try:
        db.session.commit()
        flash(_("%(name)s has been added to the trip!", name=guest_name), "success")
    except IntegrityError:
        db.session.rollback()
        flash(_("Error: Guest is already registered for this trip."), "danger")

    return redirect(url_for("trips.trip_detail", trip_id=trip_id))


@rsvp_bp.route("/rsvp/<int:rsvp_id>/remove", methods=["POST"])
@login_required
def remove_rsvp(rsvp_id: int):
    rsvp = db.get_or_404(RSVP, rsvp_id)
    trip_id = rsvp.trip_id
    db.session.delete(rsvp)
    db.session.commit()
    flash(_("RSVP removed."), "info")
    return redirect(url_for("trips.trip_detail", trip_id=trip_id))
