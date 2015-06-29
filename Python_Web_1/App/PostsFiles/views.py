#######################
####### imports #######
#######################
from flask import render_template, request, redirect, url_for, flash, Blueprint
from App import db
from forms import AddPostForm, EditPostForm, AddCommentForm
from App.models import Posts, Users, Comments
from flask.ext.login import login_required, current_user
from sqlalchemy import desc
from flask.ext.paginate import Pagination
from App.LogFiles.log import postLog, commentLog
from App.share import getPER_PAGE

######################
####### config #######
######################
posts_blueprint = Blueprint(
	'PostsFiles', __name__,
	template_folder='templates'
)
PER_PAGE = getPER_PAGE() # default is 5

# a number that represents an admin user, mostly I use it to compare with current_user.get_id() which 
# returns unicode. Thus, I decode it to unicode(utf-8)
ADMINID = '1'.decode('utf-8') 
ADMIN = 1 # a number that represents an admin user, just for trigger some methods
USER = 0 # a number that represents a regular user, just for trigger some methods

######################
####### routes #######
######################
##############################
####### Show All Posts #######
##############################
@posts_blueprint.route('/showAllPosts', defaults={'page': 1})
@posts_blueprint.route('/showAllPosts<int:page>')
@login_required
def showAllPosts(page): # for admin

    if current_user.get_id() == ADMINID:
        posts = Posts.query.add_columns(Users.user_name, Posts.post_id, Posts.post_title, \
                            Posts.post_type, Posts.post_time, Posts.post_privacy) \
                .filter(Posts.post_authorID == Users.user_id).order_by(desc(Posts.post_time)) \
                .paginate(page, PER_PAGE, False)
        count = db.session.query(Users.user_name, Posts.post_title, Posts.post_type, Posts.post_time, Posts.post_privacy)\
                .filter(Posts.post_authorID == Users.user_id).count()

        pagination = Pagination(page=page, total=count, per_page=PER_PAGE, record_name='posts')

        return render_template('showAllPosts.html', posts=posts, pagination=pagination)

#################################
####### Show All My Posts #######
#################################
@posts_blueprint.route('/showAllMyPosts', defaults={'page': 1})
@posts_blueprint.route('/showAllMyPosts<int:page>')
@login_required
def showAllMyPosts(page):
    
    posts = Posts.query.join(Users).add_columns(Users.user_name, Posts.post_id, Posts.post_title, \
                            Posts.post_type, Posts.post_time, Posts.post_privacy) \
                .filter(Posts.post_authorID == Users.user_id) \
                .filter(Users.user_name == current_user) \
                .order_by(desc(Posts.post_time)).paginate(page, PER_PAGE, False)

    count = Posts.query.join(Users).add_columns(Users.user_name, Posts.post_id, Posts.post_title, \
                            Posts.post_type, Posts.post_time, Posts.post_privacy) \
                .filter(Posts.post_authorID == Users.user_id) \
                .filter(Users.user_name == current_user).count()
    pagination = Pagination(page=page, total=count, per_page=PER_PAGE, record_name='posts')

    return render_template('showAllMyPosts.html', posts=posts, pagination=pagination)

########################
####### ADD Post #######
########################
@posts_blueprint.route('/addPost', methods=['GET', 'POST'])
@login_required
def addPost():
    form = AddPostForm()

    if request.method == 'POST':
        if request.form.get('submit') == 'Cancel':
            return redirect(url_for('PostsFiles.showAllMyPosts'))
        
        elif form.validate_on_submit():
            postType = form.post_type.data.encode('utf-8')
            postTitle = form.post_title.data.encode('utf-8')
            postPrivacy = form.post_privacy.data.encode('utf-8')
            postContent = form.post_content.data.encode('utf-8')
            addPosts(postType, postTitle, postPrivacy, postContent)  
            return redirect(url_for('PostsFiles.showAllMyPosts'))
    return render_template('addPost.html', form = form) 

def addPosts(postType, postTitle, postPrivacy, postContent): 
            try:

                user = current_user.get_id()
                post = Posts(
                    post_type=postType,
                    post_title=postTitle,
                    post_privacy=postPrivacy,
                    post_content=postContent,
                    post_authorID=user
                )
                db.create_all()
                db.session.add(post)
                db.session.commit()

                # get post_id for trigger
                postID = db.session.query(Posts.post_id)\
                .filter(Posts.post_type == postType)\
                .filter(Posts.post_title == postTitle)\
                .filter(Posts.post_privacy == postPrivacy)\
                .filter(Posts.post_content == postContent)\
                .filter(Posts.post_authorID == user).first()

                Log(action='ADD', 
                postID=postID[0],
                postTitle=postTitle,  
                postType=postType,
                postPrivacy=postPrivacy,
                postContent=postContent)

            except:
                Log("ADD FAIL")
                db.session.rollback()
                flash('Fail to add post!')

#################################
####### Show Post Content #######
#################################
@posts_blueprint.route('/showPost<int:postID>', methods=['GET', 'POST'], defaults={'page': 1})
@posts_blueprint.route('/showPost<int:postID>-<int:page>', methods=['GET', 'POST'])
@login_required
def showPost(postID, page):

    posts = db.session.query(Posts).filter(Posts.post_id == postID).all()
    # for deleting log
    if current_user.get_id() == ADMIN:
        who = ADMIN
    else: 
        who = USER

    # check if the post is yours, then you can edit and delete
    owner = db.session.query(Posts).filter(Posts.post_id == postID) \
                .filter(Posts.post_authorID == current_user.get_id()).first()
    if owner:
        editable = True
    else:
        editable = False

    # show comments
    comments = Comments.query.add_columns(Users.user_name, \
                Comments.comment_time, Comments.comment_content) \
                .filter(Users.user_id == Comments.comment_owner) \
                .filter(Posts.post_id == Comments.comment_postID) \
                .filter(Comments.comment_postID == postID) \
                .order_by(desc(Comments.comment_time)).paginate(page, PER_PAGE, False)
   
    count = Comments.query.add_columns(Users.user_name, \
                Comments.comment_time, Comments.comment_content) \
                .filter(Users.user_id == Comments.comment_owner) \
                .filter(Posts.post_id == Comments.comment_postID) \
                .filter(Comments.comment_postID == postID).count()

    pagination = Pagination(page=page, total=count, per_page=PER_PAGE, record_name='comments')

    # comment section
    form = AddCommentForm()
    if request.method == 'POST':
        comment_content = form.comment_content.data
        addComment(postID, comment_content)  
        return redirect(url_for('PostsFiles.showPost', postID=postID, page=page) )
        
    return render_template('showPost.html', posts=posts, who=who, editable=editable, form=form, pagination=pagination, comments=comments, page=page)

###########################
####### ADD Comment #######
###########################
def addComment(comment_postID, comment_content):   
    try:
        comment = Comments(
            comment_postID=comment_postID,
            comment_owner=current_user.get_id(),
            comment_content=comment_content
        )
        db.create_all()
        db.session.add(comment)
        db.session.commit()

        # Log
        commentLog('COMMENT', comment_postID, current_user.get_id(), current_user, comment_content)

    except:
        print 'addComment fail'
        db.session.rollback()
        flash('Fail to add comment!')


#####################################
####### DELETE Post for Admin #######
#####################################
@posts_blueprint.route('/delPost', methods=['GET'], defaults={'page': 1})
@posts_blueprint.route('/delPost<int:page>')
@login_required
def delPost(page): # for admin
    if current_user.get_id() == ADMINID:
        posts = Posts.query.add_columns(Users.user_name, Posts.post_id, Posts.post_title, \
                    Posts.post_type, Posts.post_time, Posts.post_privacy)\
                    .filter(Posts.post_authorID == Users.user_id).order_by(desc(Posts.post_time)).paginate(page, PER_PAGE, False)
        count = Posts.query.add_columns(Users.user_name, Posts.post_id, Posts.post_title, \
                    Posts.post_type, Posts.post_time, Posts.post_privacy)\
                    .filter(Posts.post_authorID == Users.user_id).count()

        pagination = Pagination(page=page, total=count, perpage=PER_PAGE, record_name='posts')
         # trigger for showing it's from admin delete page
        who = ADMIN
        return render_template('delPost.html', posts=posts, who=who, pagination=pagination)

##############################
####### DELETE My Post #######
##############################
@posts_blueprint.route('/delMyPost', methods=['GET'], defaults={'page': 1})
@posts_blueprint.route('/delMyPost<int:page>')
@login_required
def delMyPost(page):
    posts = Posts.query.join(Users).add_columns(Users.user_name, Posts.post_id, Posts.post_title, \
                Posts.post_type, Posts.post_time, Posts.post_privacy)\
                .filter(Posts.post_authorID == Users.user_id)\
                .filter(Users.user_name == current_user)\
                .order_by(desc(Posts.post_time)).paginate(page, PER_PAGE, False)
    count = Posts.query.join(Users).add_columns(Users.user_name, Posts.post_id, Posts.post_title, \
                Posts.post_type, Posts.post_time, Posts.post_privacy)\
                .filter(Posts.post_authorID == Users.user_id)\
                .filter(Users.user_name == current_user).count()

    pagination = Pagination(page=page, total=count, perpage=PER_PAGE, record_name='posts')
    # trigger for showing it's from the regular user
    who = USER
    return render_template('delPost.html', posts=posts, who=who, pagination=pagination)

###################################
####### Confirm Delete Post #######
###################################
@posts_blueprint.route('/confirmDelPost<int:delPost><int:who>', methods=['GET', 'POST'])
@login_required
def confirmDelPost(delPost, who):
    
    post = Posts.query.filter_by(post_id=delPost).first()
    
    if request.method == 'POST':
        if request.form.get('submit') == 'Cancel':
            return redirect(url_for('PostsFiles.showAllMyPosts'))

        else: 
            
            try:
                db.session.delete(post)
                db.session.commit()
                
                flash('Post has been deleted!')

                if who == ADMIN:
                    action = "DELETE BY ADMIN"
                    Log(action=action, postID=delPost)
                    return redirect(url_for('PostsFiles.delPost'))
                else: 
                    action = "DELETE"
                    Log(action=action, postID=delPost)
                    return redirect(url_for('PostsFiles.delMyPost'))     
            except:
                Log("DELETE FAIL")
                db.session.rollback()
                flash('Fail to delete post!')
            
    return render_template('confirmDelPost.html', post=post, who=who) 

#########################
####### EDIT post #######
#########################
@posts_blueprint.route('/editPost<int:postID>', methods=['GET', 'POST'])
@login_required
def editPost(postID):

    form = EditPostForm()

    if request.method == 'POST':
        if request.form.get('submit') == 'Cancel':
            return redirect(url_for('PostsFiles.showAllMyPosts'))
        
        else:
            user = current_user.get_id()
            postType = form.post_type.data
            postTitle = form.post_title.data
            postPrivacy = form.post_privacy.data
            postContent = request.form.get('textArea')

            try:
                db.session.query(Posts).filter(Posts.post_id == postID).update({ 
                                'post_title':postTitle,
                                'post_type':postType,
                                'post_privacy': postPrivacy,
                                'post_content':postContent,
                                'post_authorID':user})
                db.session.commit()

                Log(action='EDIT', 
                    postID=postID,
                    postTitle=postTitle,  
                    postType=postType,
                    postPrivacy=postPrivacy,
                    postContent=postContent)

                flash('You post has been updated!')
            except:
                Log("EDIT FAIL")
                db.session.rollback()
                flash('Error during edit post!')

        return redirect(url_for('PostsFiles.showAllMyPosts'))    

    posts = db.session.query(Posts).filter(Posts.post_id == postID).all()
    return render_template('editPost.html', posts=posts, form=form)

###################
####### LOG #######
###################
def Log(action, **kwargs):
    user = current_user

    if kwargs.get('postID') is not None \
        and kwargs.get('postTitle') is not None \
        and kwargs.get('postType')is not None \
        and kwargs.get('postPrivacy') is not None \
        and kwargs.get('postContent') is not None: 
        postLog(action=action, userID=user.get_id(), username=user, postID=kwargs.get('postID'), \
                postTitle=kwargs.get('postTitle'), postType=kwargs.get('postType'), \
                postPrivacy=kwargs.get('postPrivacy'), postContent=kwargs.get('postContent'))

    elif kwargs.get('postID') is not None: # for delete
        postLog(userID=user.get_id(), username=user, action=action, postID=kwargs.get('postID'))
    else: 
        print 'error in Log()'
        postLog(action=action)
