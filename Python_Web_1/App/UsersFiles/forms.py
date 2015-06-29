#######################
####### imports #######
#######################
from App.models import Users
from flask.ext.wtf import Form
from wtforms import TextField, validators, PasswordField
from wtforms.validators import Length, EqualTo, Email
from flask.ext.login import login_user, current_user
from werkzeug import generate_password_hash

class SignupForm(Form):
	
	user_name = TextField('user_name', [validators.Required("Please enter your email."), Email(message=None), Length(min=3, max=50)])
	user_password1 = PasswordField('user_password1', [validators.Required("Please enter password."), Length(min=3, max=30)])	
	user_password2 = PasswordField('user_password2', [validators.Required("Please enter password."), EqualTo('user_password1', message="Passwords must match!")])

	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)

	def validate(self):
		if not Form.validate(self):
			return False

		userExist = Users.query.filter_by(user_name = self.user_name.data.lower()).first()
		if userExist:
			self.user_name.errors.append("This username is already in use.")
			return False
		else:
			return True

class LoginForm(Form):
	
	user_name = TextField('user_name', [validators.Required("Please enter username."), Email(message=None), Length(min=3, max=50)])
	user_password = PasswordField('user_password', [validators.Required("Please enter password.")])

	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)

	def validate(self):

		if not Form.validate(self):
			return False
			
		user = Users.query.filter_by(user_name = self.user_name.data.lower()).first()
		if user and user.check_password(self.user_password.data):
			login_user(user)
			return True
		else:
			return False


class ChangingPasswordForm(Form):
	
	old_password = PasswordField('old_password', [validators.Required("Please your old password."), Length(min=3, max=30)])
	user_password1 = PasswordField('user_password1', [validators.Required("Please enter password."), Length(min=3, max=30)])
	user_password2 = PasswordField('user_password2', [validators.Required("Please enter password."), EqualTo('user_password1', message="Passwords must match!")])
	
	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)

	def set_password(self, user_password):
		return generate_password_hash(user_password)

	def validate(self):
		if not Form.validate(self):
			return False

		user = current_user
		if user.check_password(self.old_password.data):
			return True
		else:
			self.old_password.errors.append("Incorrect password.")
			return False


		