from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm


class AddCarForm(FlaskForm):
    Car_image = FileField("Car_image", validators=[FileAllowed(["jpg", "png", "jpeg"])])
    CarName = StringField("CarName", validators=[DataRequired()])
    ModelCar = StringField("ModelCar", validators=[DataRequired()])
    Color = StringField("Color", validators=[DataRequired()])
    Year = StringField("Year", validators=[DataRequired()])
    # Car Number
    CarNumber_num = StringField(
        "CarNumber_num", validators=[DataRequired(), Length(min=1, max=4)]
    )
    CarNumber_words = StringField(
        "CarNumber_words", validators=[DataRequired(), Length(min=1, max=5)]
    )
    submit = SubmitField("إضافة السياره")


class UpdateCar(FlaskForm):
    up_Car_image = FileField(
        "up_Car_image", validators=[FileAllowed(["jpg", "png", "jpeg"])]
    )
    up_CarName = StringField("up_CarName", validators=[DataRequired()])
    up_ModelCar = StringField("up_ModelCar", validators=[DataRequired()])
    up_Color = StringField("up_Color", validators=[DataRequired()])
    up_Year = StringField("up_Year", validators=[DataRequired()])
    # Car Number
    up_CarNumber_num = StringField(
        "up_CarNumber_num", validators=[DataRequired(), Length(min=1, max=4)]
    )
    up_CarNumber_words = StringField(
        "up_CarNumber_words", validators=[DataRequired(), Length(min=1, max=5)]
    )
    up_submit = SubmitField("تحديث البيانات السياره")
