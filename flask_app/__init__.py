import redis.asyncio as redis
from flask import Flask
from flask_admin import Admin
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

login_manager = LoginManager()
admin_dashboard = Admin()
migrate = Migrate()
db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()

login_manager.login_message = "يرجى تسجيل الدخول للوصول إلى هذه الصفحة"
login_manager.login_message_category = "info"
login_manager.login_view = "auth.login"


def create_app(config_calss=Config):
    app = Flask(__name__)
    app.config.from_object(config_calss)
    from flask_app.admin.routes import MyAdminIndexView

    login_manager.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    admin_dashboard.init_app(app, index_view=MyAdminIndexView())
    with app.app_context():
        from flask_app import models

    from flask_app.admin.routes import adminbp
    from flask_app.auth.routes import auth
    from flask_app.Car.routes import car_routes
    from flask_app.Errors.routes import errors
    from flask_app.main.routes import main
    from flask_app.Trip.routes import trip_routes
    from flask_app.User.routes import user_routes

    # (variable) app: Flask
    app.register_blueprint(user_routes)
    app.register_blueprint(trip_routes)
    app.register_blueprint(car_routes)
    app.register_blueprint(adminbp)
    app.register_blueprint(errors)
    app.register_blueprint(auth)
    app.register_blueprint(main)

    return app
