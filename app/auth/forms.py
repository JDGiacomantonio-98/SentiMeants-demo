import re

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError

from app.dbModels import User


class AccessDoorForm(FlaskForm):

	email = StringField('', validators=[DataRequired(), Email()], render_kw={'placeholder': 'email address'})
	password = PasswordField('', validators=[DataRequired(), Length(min=8, max=128)], render_kw={'placeholder': 'choose this carefully'})

	submit = SubmitField('')

	def __init__(self, login=True, *args, **kwargs):

		super(AccessDoorForm, self).__init__(*args, **kwargs)
		self.login = login

		if self.login:
			self.email.label.text = 'Signed email address :'
			self.password.label.text = 'Password : '
			self.submit.label.text = 'Log into Seantimeants!'
		else:
			self.email.label.text = 'Sign up with your email address :'
			self.password.label.text = 'A strong password : '
			self.submit.label.text = 'Sign up and start search with super-powers!'

	def validate_email(self, email):

		if not self.login:
			if self.email.data == User.query.filter_by(email=self.email.data).first():
				raise ValidationError('An existing account is already registred under this email address. Please use another one!')

	def validate_password(self, password):

		if re.search('[0-9]', self.password.data) is None or not((any(c.isupper() for c in  self.password.data))):
			raise ValidationError('a valid password contains at least one digit character and one capital letter. Please correct your input.')
