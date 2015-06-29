#######################
####### imports #######
#######################
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

######################
####### config #######
######################
app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config.from_object('config.LocalConfig')
db = SQLAlchemy(app)

from App.UsersFiles.views import users_blueprint
from App.HomeFiles.views import home_blueprint
from App.PostsFiles.views import posts_blueprint
from App.LogFiles.log import log_blueprint
from App.LogFiles.views import logView_blueprint
# from App.LogFiles.hash import hash_blueprint
from App.share import share_blueprint

# register blueprints
app.register_blueprint(users_blueprint)
app.register_blueprint(home_blueprint)
app.register_blueprint(posts_blueprint)
app.register_blueprint(log_blueprint)
app.register_blueprint(logView_blueprint)
# app.register_blueprint(hash_blueprint)
app.register_blueprint(share_blueprint)

# config, it will decide which environment to use
# in shell write " export APP_SETTINGS="config.LocalConfig" ""
# to set which environment you want to pretend
# and check in ipython from app import app -> print app.config
# import os
# app.config.from_object(os.environ['APP_SETTINGS'])

from models import Users

# defining the login view
login_manager.login_view = "UsersFiles.login"

@login_manager.user_loader
def load_user(user_id):
	return Users.query.filter(Users.user_id == int(user_id)).first()

#####################################
####### Timeout Login Session #######
########################3############
from datetime import timedelta

app.permanent_session_lifetime = timedelta(minutes=15)


