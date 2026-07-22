from flask import Blueprint, render_template
from flask_app import models

main = Blueprint("main", __name__, template_folder="templates", static_folder="static")


@main.route("/", methods=["GET", "POST"])
def home():
    all_trips = models.Trip.query.all()
    return render_template("main/main.html", all_trips=all_trips)


@main.route("/about")
def about():
    return render_template("main/about.html")
