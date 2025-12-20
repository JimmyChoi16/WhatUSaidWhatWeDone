from flask import Blueprint

errors_bp = Blueprint("errors", __name__)


@errors_bp.app_errorhandler(404)
def not_found(_e):
    return {"error": "Not Found"}, 404


@errors_bp.app_errorhandler(405)
def method_not_allowed(_e):
    return {"error": "Method Not Allowed"}, 405


@errors_bp.app_errorhandler(500)
def internal_error(_e):
    return {"error": "Internal Server Error"}, 500
