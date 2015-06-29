#######################
####### imports #######
#######################
from flask import render_template, Blueprint
from App.models import ActivityLog, Posts
from flask.ext.login import login_required, current_user
from sqlalchemy import desc
from flask.ext.paginate import Pagination

######################
####### config #######
######################
logView_blueprint = Blueprint(
	'LogViewFiles', __name__,
	template_folder='templates'
)
PER_PAGE = 25 
ADMIN = '1'.decode('utf-8')
######################
####### routes #######
######################
########################
####### Show Log #######
########################
@logView_blueprint.route('/showLog', defaults={'page': 1})
@logView_blueprint.route('/showLog<int:page>')
@login_required
def showLog(page): # for admin
    if current_user.get_id() == ADMIN:

        logs = ActivityLog.query.order_by(desc(ActivityLog.log_id)).paginate(page, PER_PAGE, False)
        count = ActivityLog.query.count()
        pagination = Pagination(page=page, total=count, per_page=PER_PAGE, record_name='logs')
        posts = Posts.query.all()

        return render_template('showLog.html', logs=logs, pagination=pagination, posts=posts)


