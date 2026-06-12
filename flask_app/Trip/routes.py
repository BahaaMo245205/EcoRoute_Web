from flask import Blueprint, render_template, request, redirect, url_for, flash ,abort
from flask_app.Trip.forms import AddTripForm, UpdateTripForm
from flask_app.models import Car
from flask_app import models
from flask_app import db
from flask_login import login_required, current_user
from datetime import datetime


trip_routes = Blueprint(
    "trip_routes", __name__, template_folder="templates", static_folder="static"
)


@trip_routes.route("/Trip")
@login_required
def Trip():
    AllTrips = models.Trip.query.all()
    start_way = request.args.get("start_way")
    end_way = request.args.get("end_way")
    if start_way:
        AllTrips = models.Trip.query.filter_by(start_way=start_way).all()
    elif end_way:
        AllTrips = models.Trip.query.filter_by(end_way=end_way).all()
    elif start_way and end_way:
        AllTrips = models.Trip.query.filter_by(
            start_way=start_way, end_way=end_way
        ).all()
    else:
        AllTrips = models.Trip.query.all()
        
    return render_template("Trip/Trips.html", AllTrips=AllTrips, title="Trips")



@trip_routes.route("/AddTrip", methods=["GET", "POST"])
@login_required
def AddTrip():
    if current_user.type_user != "Riders":
        abort(403)
    
    form = AddTripForm()

    user_cars = Car.query.filter_by(user_id=current_user.user_id).all()
    form.ChooiceCar.choices = [
        (c.Car_id, f"{c.Car_name} {c.model_car} {c.color}") for c in user_cars
    ]

    if form.validate_on_submit():
        id_car = form.ChooiceCar.data
        selected_car = Car.query.get_or_404(id_car)

        new_trip = models.Trip(
            user_id=current_user.user_id,
            car_id=id_car,
            name_car=f"{selected_car.Car_name} {selected_car.model_car}",
            car_color=selected_car.color,
            car_image=selected_car.Car_image,
            user_image=current_user.image,
            start_way=form.StartWay.data,
            end_way=form.EndWay.data,
            time=str(form.Time.data),
            chair=int(form.ChairCar.data),
            price=float(form.Price.data),
        )

        try:
            db.session.add(new_trip)
            db.session.commit()
            flash("تم إضافة الرحلة بنجاح", "success")
            return redirect(url_for("trip_routes.Trip"))
        except Exception as e:
            db.session.rollback()
            flash(f"حدث خطأ أثناء الحفظ: {e}", "danger")

    if request.method == "GET":

        form.Time.data = datetime.now()

    return render_template("Trip/Add_Trips.html", form=form, title="Add Trip")


@trip_routes.route("/Trip/<int:trip_id>/delete", methods=["GET", "POST"])
@login_required
def DeleteTrip(trip_id):
    if current_user.type_user != "Riders":
        abort(403)
    delete_trip = models.Trip.query.get_or_404(trip_id)
    delete_booking = models.Bookings.query.filter_by(Trip_id=trip_id).all()
    for booking in delete_booking:
        db.session.delete(booking)
    db.session.delete(delete_trip)
    db.session.commit()
    flash("تم حذف الرحلة بنجاح", "success")
    return redirect(url_for("trip_routes.Trip"))




@trip_routes.route("/Trip/<int:trip_id>/Update", methods=["GET", "POST"])
@login_required
def UpdateTrip(trip_id):
    form = UpdateTripForm()
    Update_trip = models.Trip.query.get_or_404(trip_id)

    if Update_trip.user_id != current_user.user_id:
        abort(403)

    form.ChooiceCar.choices = [
        (c.Car_id, f"{c.Car_name} {c.model_car}")
        for c in Car.query.filter_by(user_id=current_user.user_id).all()
    ]
    if form.validate_on_submit():
        Update_trip.car_id = form.ChooiceCar.data
        Update_trip.start_way = form.StartWay.data
        Update_trip.end_way = form.EndWay.data
        Update_trip.time = str(form.Time.data)
        Update_trip.chair = int(form.ChairCar.data)
        Update_trip.price = float(form.Price.data)

        db.session.commit()
        flash("تم تحديث بيانات الرحلة بنجاح", "success")
        return redirect(url_for("trip_routes.Trip"))

    elif request.method == "GET":
        form.ChooiceCar.data = Update_trip.car_id
        form.StartWay.data = Update_trip.start_way
        form.EndWay.data = Update_trip.end_way
        formatted_time = datetime.strptime(Update_trip.time, "%H:%M:%S").time()
        form.Time.data = formatted_time
        form.ChairCar.data = int(Update_trip.chair)
        form.Price.data = float(Update_trip.price)

    return render_template("Trip/Update_Trips.html", form=form, title="Update Trip")


@trip_routes.route("/Trip/<int:trip_id>/DetailsTrips", methods=["GET", "POST"])
@login_required
def details_Trips(trip_id):
    trips = models.Trip.query.get_or_404(trip_id)
    all_bookings = models.Bookings.query.filter_by(Trip_id=trip_id).all()
    if request.method == "POST":
        Chear = request.form["requested_chairs"]
        if int(Chear) <= 0:
            flash("رجاء إدخال الرقم صحيح", "danger")
            return redirect(url_for("trip.Trip"))
        elif Chear.isdigit() == False:
            flash("رجاء إدخال الرقم صحيح", "danger")
            return redirect(url_for("trip.Trip"))
        elif int(Chear) > int(trips.chair):
            flash("للأسف العدد اللي طلبته أكتر من الكراسي المتاحة حالياً", "warning")
            return redirect(url_for('trip_routes.details_Trips', trip_id=trip_id)) 
        else:
            trips.chair = int(trips.chair) - int(Chear)
            AddBooking = models.Bookings(
                user_id=current_user.user_id,
                Trip_id=trips.trip_id,
                requested_chairs=Chear,
            )
            db.session.add(AddBooking)
            db.session.commit()
            flash(f"تم حجز {Chear} مقاعد بنجاح! رحلة سعيدة.", "success")
            return redirect(url_for("trip_routes.Trip"))

    return render_template("Trip/details_Trips.html", trips=trips, title="Details Trip",all_bookings=all_bookings)


# @trip_bp.route('/Trip/<int:trip_id>/Booking', methods=['GET', 'POST'])
# @login_required
# def Booking (trip_id):
#     trips = models.Trip.query.get_or_404(trip_id)
#     return render_template('Trip/Booking_trip.html', title="Booking", trips=trips)
