from flask_app import db, create_app
from flask_app import login_manager
from flask_login import UserMixin
from datetime import datetime
from itsdangerous import URLSafeSerializer
from config import Config as C


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image = db.Column(db.String(120), unique=False, nullable=False, default="user.png")
    first_name = db.Column(db.String(120), unique=False, nullable=False)
    last_name = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(120), unique=True, nullable=False)
    type_user = db.Column(db.String(120), unique=False, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    Cars = db.relationship("Car", backref="author", lazy=True)
    Trips = db.relationship("Trip", backref="Trip_user", lazy=True)
    trips_booked = db.relationship("Bookings", backref="passenger", lazy=True)

    def get_reset_token(self):
        s = URLSafeSerializer(C.SECRET_KEY, salt="pw-reset")
        return s.dumps({"user_id": self.user_id})

    @staticmethod
    def verify_reset_token(token):
        s = URLSafeSerializer(C.SECRET_KEY, salt="pw-reset")
        try:
            data = s.loads(token, salt="pw-reset", max_age=3600)
            user_id = data["user_id"]
        except:
            return None

        return User.query.get(user_id)

    def get_id(self):
        return str(self.user_id)

    def __repr__(self):
        return f"{self.first_name} {self.last_name} {self.email} {self.phone} {self.password}"


class Car(db.Model):
    Car_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Car_image = db.Column(
        db.String(120), unique=False, nullable=True, default="car.png"
    )
    Car_name = db.Column(db.String(120), unique=False, nullable=False)
    model_car = db.Column(db.String(120), unique=False, nullable=False)
    color = db.Column(db.String(120), unique=False, nullable=False)
    year = db.Column(db.String(120), unique=False, nullable=False)

    CarNumber_words = db.Column(db.String(120),  nullable=False)
    CarNumber_num = db.Column(db.String(120),  nullable=False)
    Trips = db.relationship("Trip", backref="Trip_car", lazy=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)

    def __repr__(self):
        return f"{self.Car_name} {self.model_car} {self.color} {self.year} {self.CarNumber_words} {self.CarNumber_num}"


class Bookings(db.Model):
    __tablename__ = "Bookings"
    Booking_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(
        "user_id", db.Integer, db.ForeignKey("user.user_id"), nullable=False
    )
    Trip_id = db.Column(
        "Trip_id", db.Integer, db.ForeignKey("trip.trip_id"), nullable=False
    )
    Time = db.Column(
        "Time", db.String(120), unique=False, nullable=False, default=datetime.utcnow
    )
    requested_chairs = db.Column("requested_chairs", db.Integer, nullable=False)


class Trip(db.Model):
    trip_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey("car.Car_id"), nullable=False)
    car_image = db.Column(
        db.String(120), unique=False, nullable=True, default="car.png"
    )
    user_image = db.Column(
        db.String(120), unique=False, nullable=True, default="user.png"
    )
    name_car = db.Column(db.String(120), unique=False, nullable=False)
    car_color = db.Column(db.String(120), unique=False, nullable=False)
    start_way = db.Column(db.String(120), unique=False, nullable=False)
    end_way = db.Column(db.String(120), unique=False, nullable=False)
    time = db.Column(db.String(120), unique=False, nullable=False)
    price = db.Column(db.String(120), unique=False, nullable=False)
    chair = db.Column(db.String(120), unique=False, nullable=False)
    bookings = db.relationship("Bookings", backref="trip", lazy=True)
