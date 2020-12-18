from flask_wtf import FlaskForm
from wtforms import StringField,BooleanField,PasswordField,SubmitField,IntegerField
from wtforms.validators import DataRequired,Email,EqualTo,ValidationError,NumberRange
from app.models import User


class LoginForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired()])
    password=PasswordField('Password',validators=[DataRequired()])
    submit=SubmitField('Login')


class RegisterForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired()])
    email=StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    register=SubmitField('Register')

    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Username already exists")
    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Email already exists")


class DataForm(FlaskForm):
    date=StringField('Date',validators=[DataRequired()])
    amount_income=IntegerField('Amount_Income', validators=[NumberRange(min=0, max=100000)])
    amount_spent=IntegerField('Amount_Spent', validators=[NumberRange(min=0, max=100000)])
    submit=SubmitField('Submit')