from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, InputRequired, Email, EqualTo
from app.models import User

class LoginForm(FlaskForm):
	username = StringField('Username', validators = [InputRequired()])
	password = PasswordField('Password', validators = [InputRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
	username = StringField('Username', validators = [InputRequired()])
	email = StringField('Email', validators = [InputRequired(), Email()])
	password = PasswordField('Password', validators = [InputRequired()])
	password_confirm = PasswordField(
		'Confirm Password',
		validators = [
			InputRequired(),
			EqualTo('password')
		]
	)
	submit = SubmitField('Register')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('That username is already taken, please try another.')
	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('That email is already in use with an account.')