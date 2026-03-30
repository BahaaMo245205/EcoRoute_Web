from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField , SelectField , TimeField , DecimalField
from wtforms.validators import DataRequired, EqualTo , ValidationError

class AddTripForm (FlaskForm):
    ChooiceCar = SelectField('ChooiceCar',validators=[DataRequired()])
    StartWay = StringField('StartWay', validators=[DataRequired()])
    EndWay = StringField('EndWay', validators=[DataRequired()])
    Time = TimeField('Time', validators=[DataRequired()])
    ChairCar = DecimalField('ChairCar', validators=[DataRequired()])
    Price = DecimalField('Price', validators=[DataRequired()])
    Submit = SubmitField('Submit')
    
    def valition_Price (self, Price):
        if self.Price.isdigit() != True :
            raise ValidationError('رجاء أدخال رقمي فقط')
        
    def valition_ChairCar (self, ChairCar):
        if self.ChairCar.isdigit() != True :
            raise ValidationError('رجاء أدخال رقمي فقط')
        


class UpdateTripForm (FlaskForm):
    ChooiceCar = SelectField('ChooiceCar',validators=[DataRequired()])
    StartWay = StringField('StartWay', validators=[DataRequired()])
    EndWay = StringField('EndWay', validators=[DataRequired()])
    Time = TimeField('Time', validators=[DataRequired()])
    ChairCar = DecimalField('ChairCar', validators=[DataRequired()])
    Price = DecimalField('Price', validators=[DataRequired()])
    Submit = SubmitField('Submit')
    
    def valition_Price (self, Price):
        if self.Price.isdigit() != True :
            raise ValidationError('رجاء أدخال رقمي فقط')
        
    def valition_ChairCar (self, ChairCar):
        if self.ChairCar.isdigit() != True :
            raise ValidationError('رجاء أدخال رقمي فقط')

        