from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, InputRequired, Email, EqualTo, Length
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

class EditProfileForm(FlaskForm):
	username = StringField('Username', validators=[InputRequired()])
	about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
	submit = SubmitField('Submit')

	def __init__(self, original_username, *args, **kwargs):
		super(EditProfileForm, self).__init__(*args, **kwargs)
		self.original_username = original_username

	def validate_username(self, username):
		if username.data != self.original_username:
			user = User.query.filter_by(username=self.username.data).first()
			if user is not None:
				raise ValidationError('Please use a different username.')
