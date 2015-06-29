#######################
####### imports #######
#######################
from flask import render_template, request, \
					redirect, url_for, flash, Blueprint, session
from App import db
from forms import LoginForm, SignupForm, ChangingPasswordForm
from App.models import Users
from flask.ext.login import login_required, logout_user, login_user, current_user
from flask.ext.paginate import Pagination
from App.LogFiles.log import userLog
from App.LogFiles.hash import addCompHash, addOrgHash, isHack

######################
####### config #######
######################
users_blueprint = Blueprint(
	'UsersFiles', __name__,
	template_folder='templates'
)

######################
####### routes #######
######################
######################
####### Login ########
######################
@users_blueprint.route('/login', methods=['GET', 'POST'])
def login(): 

    error = None
    form = LoginForm()
    
    if request.method == 'POST':
        if request.form.get('submit') == 'Register':
            return redirect(url_for('UsersFiles.register'))
        
        elif form.validate_on_submit():
            session.permanent = True
            Log("LOGIN")
            # compare hash
            addCompHash(str(current_user))
            
            flash('You are just login!')
            
            try: 
                if isHack(str(current_user)):
                    flash('!!!!! YOU GOT HACK !!!!!!')
            except:
                flash('First time login')

            return redirect(url_for('HomeFiles.home'))
        
        else:
            error = 'Invalid username or password. Please try again.'
            Log("LOGIN FAIL")

            return render_template('login.html', form=form, error=error)

    elif request.method == 'GET':
        return render_template('login.html', form=form)

#########################
####### Register ########
#########################

@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    form = SignupForm()
    if request.method == 'POST':
        if request.form.get('submit') == 'Cancel':
            return redirect(url_for('UsersFiles.login'))
        
        elif form.validate_on_submit():
            try: 
                user = Users(
                    user_name=form.user_name.data,
                    user_password=form.user_password1.data 
                )
                db.create_all()
                db.session.add(user)
                db.session.commit()
                Log("SIGNUP")

                login_user(user)
                Log("LOGIN")
                # add hash
                addCompHash(str(current_user))
                flash('You are just login!')
                return redirect(url_for('HomeFiles.home'))

            except:
                error = 'Signup Fail'
                db.session.rollback()
                Log("SIGNUP FAIL")
            #     trace= get_current_traceback(skip=1, show_hidden_frames=True,
            # ignore_system_exceptions=False)
            # return redirect(url_for('ShareFiles.stack_trace', trace=trace))
            

    return render_template('register.html', form = form, error = error) 

######################
####### Logout #######
######################

@users_blueprint.route('/logout')
@login_required
def logout():
    
    Log("LOGOUT")
    addOrgHash(str(current_user))
    logout_user()

    
    flash('You are just logout!')
    return redirect(url_for('HomeFiles.welcome'))


######################################
####### Manage Users for Admin #######
######################################

@users_blueprint.route('/manageUsers', defaults={'page': 1})
@users_blueprint.route('/manageUsers<int:page>', methods=['GET'])
@login_required
def manageUsers(page):

    PER_PAGE = 5
    allUsers = Users.query.paginate(page, PER_PAGE, False)
    count = Users.query.count()
    pagination = Pagination(page=page, total=count, per_page=PER_PAGE, record_name='users')

    return render_template('showUsers.html', users=allUsers, pagination=pagination)

############################
####### Delete User ########
############################

@users_blueprint.route('/delUser<int:delUserID>', methods=['GET', 'POST'])
@login_required
def delUser(delUserID):
    error=None
    user = Users.query.filter_by(user_id=delUserID).first()
    
    if request.method == 'POST':
        if request.form.get('submit') == 'Cancel':
            return redirect(url_for('UsersFiles.manageUsers'))

        else: 
            try:
                db.session.delete(user)
                db.session.commit()

                # Logging 
                if current_user.get_id() == '1':
                    action = "DELETE USER BY ADMIN"
                else:
                    action = "DELETE USER"
                
                Log(action)

                flash('User has been deleted!')
            except:
                db.session.rollback()
                Log("DELETE USER FAIL")
                error='DELETE USER FAIL'

            return redirect(url_for('UsersFiles.manageUsers'))  

    return render_template('confirmDelUser.html', user=user, error=error)

##################################
####### Changing Password ########
##################################

@users_blueprint.route('/changingPassword', methods=['GET', 'POST'])
def changingPassword():
    error = None
    form = ChangingPasswordForm()
    if request.method == 'POST':
        if request.form.get('submit') == 'Cancel':
            return redirect(url_for('PostsFiles.showAllMyPosts'))
        
        elif form.validate_on_submit():

            # get the current user_id
            userID = current_user.get_id()
            pwd = form.user_password1.data
            # update user password in db
            try:
                db.session.query(Users).filter(Users.user_id == userID).update({
                'user_password': form.set_password(pwd)
                })
                db.session.commit()
                Log("CHANGING PASSWORD")
            except:
                db.session.rollback()
                Log("CHANGING PASSWORD FAIL")
                
            

            flash('Your password has been changed!')
            return redirect(url_for('PostsFiles.showAllMyPosts'))

    return render_template('changingPassword.html', form=form, error=error) 

###################
####### LOG #######
###################

def Log(action):
    try: 
        user = current_user
        userLog(userID=user.get_id(), username=user, action=action)
    except: 
        print 'error in Log()'
        userLog(action)

##################################
####### test db connecting #######
##################################

@users_blueprint.route('/testdbFromUser')
def testdba():
    if db.session.query("1").from_statement("SELECT 1").all():
        return 'It works.'
    else:
        return 'Something wrong!!!'

