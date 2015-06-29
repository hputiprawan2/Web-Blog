#######################
####### imports #######
#######################
from flask import render_template, Blueprint
from App.models import Posts, Users
from flask.ext.login import login_required, current_user
from sqlalchemy import desc
from App.PostsFiles.views import addPosts
from App.PostsFiles.forms import AddPostForm
from flask.ext.paginate import Pagination
from App.share import getPER_PAGE

######################
####### config #######
######################
home_blueprint = Blueprint(
    'HomeFiles', __name__,
    template_folder='templates'
)
PER_PAGE = getPER_PAGE()

######################
####### routes #######
######################
# use decorators to link the function to a url
@home_blueprint.route('/', methods=['GET', 'POST'], defaults={'page': 1})
@home_blueprint.route('/<int:page>')
@login_required
def home(page):

    form = AddPostForm()
    
    if form.validate_on_submit():
            postType = form.post_type.data
            postTitle = form.post_title.data
            postPrivacy = form.post_privacy.data
            postContent = form.post_content.data
            addPosts(postType, postTitle, postPrivacy, postContent) 

    posts = Posts.query.join(Users).add_columns(Users.user_name, Posts.post_id, Posts.post_title, \
                    Posts.post_type, Posts.post_time, Posts.post_privacy)\
                .filter(Posts.post_authorID == Users.user_id) \
                .filter(Posts.post_privacy == 'Public') \
                .order_by(desc(Posts.post_time)).paginate(page, PER_PAGE, False)

    count = Posts.query.join(Users).add_columns(Users.user_name, Posts.post_id, Posts.post_title, \
                            Posts.post_type, Posts.post_time) \
                .filter(Posts.post_authorID == Users.user_id) \
                .filter(Posts.post_privacy == 'Public').count()
    pagination = Pagination(page=page, total=count, per_page=PER_PAGE, record_name='posts')

    return render_template('index.html', posts=posts, form=form, pagination=pagination)

######################
####### Welcome ######
######################
@home_blueprint.route('/welcome')
def welcome():
    return render_template("welcome.html")

######################
####### Welcome ######
######################
@home_blueprint.route('/profile')
@login_required
def profile():
    username = current_user
    return render_template("profile.html", username=username)

#####################
####### About #######
#####################
@home_blueprint.route('/about')
def about():
    return render_template("about.html")

#####################
####### About #######
#####################
@home_blueprint.route('/references')
def references():
    return render_template("references.html")

