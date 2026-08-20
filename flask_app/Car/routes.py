from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_app.Car.forms import AddCarForm, UpdateCar
from flask_login import login_required, current_user
from flask_app.Car.helpr import save_picture
from flask_app.models import Car
from flask_app import db
import os

car_routes = Blueprint(
    "car_routes", __name__, template_folder="templates", static_folder="static"
)


@car_routes.route("/Car", methods=["GET", "POST"])
@login_required
def AddCar():
    if current_user.type_user != "Riders":
        abort(403)

    form = AddCarForm()
    if request.method == "POST":
        if form.validate_on_submit():
            if form.Car_image.data:
                
                picture_file = save_picture(form.Car_image.data)
                Car_image = picture_file
            else:
                Car_image = "car.png"

            CarName = form.CarName.data
            ModelCar = form.ModelCar.data
            Color = form.Color.data
            Year = form.Year.data
            CarNumber_num = form.CarNumber_num.data
            CarNumber_words = form.CarNumber_words.data
            car = Car(
                Car_image=Car_image,
                Car_name=CarName,
                model_car=ModelCar,
                color=Color,
                year=Year,
                CarNumber_words=CarNumber_words,
                CarNumber_num=CarNumber_num,
                user_id=current_user.user_id,
            )
            db.session.add(car)
            db.session.commit()
            flash("تم الاضافة بنجاح", "success")
            return redirect(url_for("car_routes.AddCar"))

    cars = Car.query.filter_by(user_id=current_user.user_id).all()

    return render_template("car_html/AddCar.html", form=form, cars=cars)


@car_routes.route("/UpdateCar/<car_id>", methods=["POST", "GET"])
@login_required
def UpdateCarData(car_id):
    if current_user.type_user != "Riders":
        abort(403)
    form = UpdateCar()
    user_car = Car.query.get_or_404(car_id)
    if request.method == "POST":
        if form.validate_on_submit():
            if form.up_Car_image.data:
                if user_car.Car_image and user_car.Car_image != "car.png":
                    is_found = os.path.exists("./flask_app/static/images/Car_images/{}".format(user_car.Car_image))
                    if is_found :
                        os.remove("./flask_app/static/images/Car_images/{}".format(user_car.Car_image))
                    picture_file = save_picture(form.up_Car_image.data)
                    Car_image = picture_file
            else:
                Car_image = "car.png"
            user_car.Car_image = Car_image
            user_car.Car_name = form.up_CarName.data
            user_car.model_car = form.up_ModelCar.data
            user_car.color = form.up_Color.data
            user_car.year = form.up_Year.data
            user_car.CarNumber_words = form.up_CarNumber_words.data
            user_car.CarNumber_num = form.up_CarNumber_num.data
            db.session.commit()
            flash("تم التعديل بنجاح", "success")
            return redirect(url_for("car_routes.AddCar"))

    form.up_Car_image.data = user_car.Car_image
    form.up_CarName.data = user_car.Car_name
    form.up_ModelCar.data = user_car.model_car
    form.up_Color.data = user_car.color
    form.up_Year.data = user_car.year
    form.up_CarNumber_words.data = user_car.CarNumber_words
    form.up_CarNumber_num.data = user_car.CarNumber_num

    return render_template("car_html/UpdateCar.html", form=form)


@car_routes.route("/car/<int:car_id>/delete", methods=["GET", "POST"])
@login_required
def delete_car(car_id):
    car = Car.query.get_or_404(car_id)

    if car.user_id != current_user.user_id:
        abort(403)

    if request.method == "POST":
        db.session.delete(car)
        db.session.commit()
        flash("تم حذف السيارة بنجاح", "success")
        return redirect(url_for("user_routes.profile"))

    return render_template("car_html/delete_car.html", car=car)
