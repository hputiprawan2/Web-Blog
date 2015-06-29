#######################
####### imports #######
#######################
from App import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from werkzeug import generate_password_hash, check_password_hash
from datetime import datetime
from flask import request

class Users(db.Model):

	__tablename__ = "Users"
	__table_args__ = {'extend_existing': True}

	user_id = db.Column(db.Integer, primary_key=True)
	user_name = db.Column(db.String(50), nullable=False)
	user_password = db.Column(db.String(50), nullable=False)
	user_lastLogin = db.Column(db.DateTime, nullable=False)
	user_posts = relationship("Posts", backref="author")
	
	def __init__(self, user_name, user_password):
		self.user_name = user_name
		self.set_password(user_password)
		self.user_lastLogin = datetime.now()

	def set_password(self, user_password):
		self.user_password = generate_password_hash(user_password)

	def check_password(self, user_password):
		return check_password_hash(self.user_password, user_password)

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def  is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.user_id)

	def __repr__(self):
		return '{}'.format(self.user_name)#'<username: {}'.format(self.user_name)


class Posts(db.Model):

	__tablename__ = "Posts"
	__table_args__ = {'extend_existing': True}

	post_id = db.Column(db.Integer, primary_key=True)
	post_type = db.Column(db.String(100), nullable=False)
	post_title = db.Column(db.String(100), nullable=False)
	post_time = db.Column(db.DateTime, nullable=False)
	post_privacy = db.Column(db.String(100), nullable=False)
	post_content = db.Column(db.Text, nullable=False)
	post_authorID = db.Column(db.Integer, ForeignKey('Users.user_id'))
	
	def __init__(self,post_type, post_title, post_privacy, post_content, post_authorID):
		self.post_type = post_type
		self.post_title = post_title
		self.post_time = datetime.now()
		self.post_privacy = post_privacy
		self.post_content = post_content
		self.post_authorID = post_authorID

	# how the object get represented 
	def __repr__(self):
		return '{}: {}: {}: {}'.format(self.post_title, self.post_content, self.post_content, self.post_privacy)


class Comments(db.Model):

	__tablename__ = "Comments"
	__table_args__ = {'extend_existing': True}

	comment_id = db.Column(db.Integer, primary_key=True)
	comment_postID = db.Column(db.Integer, ForeignKey('Posts.post_id'))
	comment_owner = db.Column(db.Integer, ForeignKey('Users.user_id'))
	comment_time = db.Column(db.DateTime, nullable=False)	
	comment_content = db.Column(db.Text, nullable=False)

	def __init__(self, comment_postID, comment_owner, comment_content):
		self.comment_postID = comment_postID
		self.comment_owner = comment_owner
		self.comment_time = datetime.now()
		self.comment_content = comment_content

	def __repr__(self):
		return '{}: {}: {}: {}'.format(self.comment_content, self.comment_time, self.comment_owner, self.comment_postID)


class ActivityLog(db.Model):

	__tablename__ = "ActivityLog"
	__table_args__ = {'extend_existing': True}

	log_id = db.Column(db.Integer, primary_key=True)
	log_userID = db.Column(db.Integer, nullable=False)
	log_username = db.Column(db.String(50), nullable=False)
	log_ipAddr = db.Column(db.String(15), nullable=False)
	log_action = db.Column(db.String(50), nullable=False)
	log_time = db.Column(db.DateTime, nullable=False)
	log_postID = db.Column(db.Integer, nullable=False)
	log_postTitle = db.Column(db.String(100), nullable=False)
	log_postType = db.Column(db.String(100), nullable=False)
	log_postPrivacy = db.Column(db.String(10), nullable=False)
	log_content = db.Column(db.Text, nullable=False)
	

	def __init__(self, log_action, **kwargs):

		self.log_userID = kwargs.get('log_userID', 0)
		self.log_username = kwargs.get('log_username', "NULL")
		self.log_ipAddr = request.remote_addr
		self.log_action = log_action
		self.log_time = datetime.now()
		self.log_postID = kwargs.get('log_postID', 0)
		self.log_postTitle = kwargs.get('log_postTitle', "NULL")
		self.log_postType = kwargs.get('log_postType', "NULL")
		self.log_postPrivacy = kwargs.get('log_postPrivacy', "NULL")
		self.log_content = kwargs.get('log_content', "NULL")

	def __repr__(self):
		return '{}: {}: {}: {}: {}'.format(self.log_username, self.log_ipAddr, self.log_action, \
											self.log_content)


class HashLog(db.Model):

	__tablename__ = "HashLog"
	__table_args__ = {'extend_existing': True}

	hash_id = db.Column(db.Integer, primary_key=True)
	hash_name = db.Column(db.String(50), nullable=False)
	hash_time = db.Column(db.DateTime, nullable=False)
	hash_org = db.Column(db.Text)
	hash_comp = db.Column(db.Text)
	hash_isHack =db.Column(db.String(5))
	

	def __init__(self, hash_name, **kwargs):

		self.hash_name = hash_name
		self.hash_org = kwargs.get('hash_org')
		self.hash_comp = kwargs.get('hash_comp')
		self.hash_time = datetime.now()
		self.hash_isHack = kwargs.get('hash_isHack')

	def __repr__(self):
		return '{}: {}: {}'.format(self.hash_name, self.hash_org, self.hash_comp)

