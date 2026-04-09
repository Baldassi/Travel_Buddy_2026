from flask import Blueprint, request, redirect, session

lang_bp = Blueprint("lang", __name__)


@lang_bp.route("/set_language/<lang>")
def set_language(lang: str):
    from app import SUPPORTED_LANGUAGES
    if lang in SUPPORTED_LANGUAGES:
        session["lang"] = lang
    return redirect(request.referrer or "/")
