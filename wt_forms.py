from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField
from wtforms.validators import InputRequired,Length,EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('usename_label',validators=[InputRequired(message="Username Required"),Length(min=4,max=25,message="4 to 25 char")])

    password = PasswordField('password_field',validators=[InputRequired(message="Pwd Required"),Length(min=4,max=25,message="4 to 25 char")])
    confirm_password  = PasswordField('confirm_pswd_field',validators=[InputRequired(message="Confirm Pwd"),Length(min=4,max=25,message="4 to 25 char")])

