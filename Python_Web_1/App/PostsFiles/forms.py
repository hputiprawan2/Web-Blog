#######################
####### imports #######
#######################
from App.models import Posts, Users
from flask.ext.wtf import Form
from wtforms import TextField, validators
from wtforms.fields import StringField, TextAreaField, SelectField
from wtforms.widgets import TextArea
from wtforms.validators import Length
from flask.ext.login import current_user

class AddPostForm(Form):
	
	post_type = TextField([validators.Required("You must have a type of title."), Length(min=3, max=50)])
	post_title = TextField([validators.Required("You must have topic.")])
	post_privacy = SelectField([validators.Required("*")], choices=[('Public', 'Public'), ('Private', 'Private')])
	post_content = StringField(widget=TextArea())	

	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)

	def validate(self):
		if not Form.validate(self):
			return False

		sameTopic = Posts.query.filter_by(post_title = self.post_title.data)\
								.filter(Users.user_name == current_user.get_id()).first()
		if sameTopic:
			self.post_title.errors.append("The topic is already exist.")
			return False
		else:
			return True


class EditPostForm(Form):
	
	post_type = TextField([validators.Required("You must have a type of title."), Length(min=3, max=50)])
	post_title = TextField([validators.Required("You must have topic.")])
	post_privacy = SelectField([validators.Required("*")], choices=[('Public', 'Public'), ('Private', 'Private')])
	post_content = TextAreaField()

	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)

	def validate(self):
		if not Form.validate(self):
			return False


class AddCommentForm(Form):
	
	comment_content = StringField(widget=TextArea())

	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)





