from flask import Blueprint, render_template, request, redirect, url_for, flash

errors = Blueprint(
    "errors", __name__, template_folder="templates", static_folder="static"
)


@errors.app_errorhandler(404)
def page_not_found(e):
    return render_template("errors/404.html"), 404


@errors.app_errorhandler(500)
def internal_server_error(e):
    return render_template("errors/500.html"), 500


@errors.app_errorhandler(403)
def forbidden(e):
    return render_template("errors/403.html"), 403
