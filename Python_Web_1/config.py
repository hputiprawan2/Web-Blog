#######################
####### imports #######
#######################
import os
import base64

class  BaseConfig(object):

	DEBUG = False
	# SECRET_KEY is used for session to work properly
	# it uses for protect the session from being accessed in the client side
	SECRET_KEY = os.urandom(24)#'\xe3N>\\=2\xa7\xdb\x16]\xb8S\xc9\xaak1T]\xa0N\xcd\xb4\xf1\x12'
	# print SECRET_KEY

	# make the config to search for the db in a specific env
	# and set the env in ipython " export DATABASE_URL='sqlite:///posts.db' "
	# SQLALCHEMY_DATABASE_URI = 'sqlite:///posts.db'
	# SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
	udb = base64.b64decode('cm9vdA==')
	pdb = base64.b64decode('cHJhbmdwcmFuZw==')
	ndb = base64.b64decode('V2ViREI=')
	SQLALCHEMY_DATABASE_URI = 'mysql://'+udb+':'+pdb+'@localhost/'+ndb

# override the parent class, for running the app within this computer 
class LocalConfig(BaseConfig):
	DEBUG = True # override just to make sure

# override the parent class, for deployed server environment 
class ProductionConfig(BaseConfig):
	DEBUG = False # override just to make sure

# for testing purpose
class TestConfig(BaseConfig):
	DEBUG = True
	TESTING = True
	WTF_CSRF_ENABLE = False
	SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# # override the parent class, for deploy at loyola server environment
class LoyolaConfig(BaseConfig):
	DEBUG = False
	udb = base64.b64decode('aHB1dGlwcmF3YW4=')
	pdb = base64.b64decode('MTY4NzkwNA==')
	ndb = base64.b64decode('aHB1dGlwcmF3YW4=')
	SQLALCHEMY_DATABASE_URI = 'mysql://'+udb+':'+pdb+'@cs-database:3306/'+ndb

