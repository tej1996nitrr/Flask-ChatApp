from flask_wtf  import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import InputRequired,Length,EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('username_label',validators=[InputRequired(message='Username Required'),Length(min=1,max=20,message="Username must be between 1 to 20 chars")])
    password = PasswordField('pwd_field',validators=[InputRequired(message='Password Required'),Length(min=1,max=10,message="Password must be between 1 to 10 chars")])
    confirm_password = PasswordField('conf_pwd_label',validators=[InputRequired(message='Confirm Password'),EqualTo('password',message="Passwords Must match")])
    submit_button = SubmitField('Create')