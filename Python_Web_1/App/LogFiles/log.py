#######################
####### imports #######
#######################
from flask import Blueprint
from App.models import ActivityLog
from App import db

######################
####### config #######
######################
log_blueprint = Blueprint(
	'LogFiles', __name__,
	template_folder='templates'
)

######################
####### routes #######
######################

########################################
###### Trigger for Users logging #######
########################################
def userLog(action, **kwargs): 

    if kwargs.get('userID') is not None and kwargs.get('username') is not None:
        try: 
            log = ActivityLog(
                log_userID=kwargs.get('userID', 0),
                log_username=kwargs.get('username', "NULL"),
                log_action=action
            )
            db.session.add(log)
            db.session.commit()
        except:
            print 'error in userLog()'
            db.session.rollback()
    else:
        try: 
            log = ActivityLog(
                log_action=action
            )
            db.session.add(log)
            db.session.commit()
        except:
            print 'fail userLog()'
            db.session.rollback()

########################################
####### Trigger for Post logging #######
########################################
def postLog(action, **kwargs): 

    if kwargs.get('userID') is not None \
        and kwargs.get('username') is not None \
        and kwargs.get('postID') is not None \
        and kwargs.get('postType') is not None \
        and kwargs.get('postTitle') is not None \
        and kwargs.get('postPrivacy') is not None \
        and kwargs.get('postContent') is not None:
        try: 
            log = ActivityLog(
                log_userID=kwargs.get('userID'),
                log_username=kwargs.get('username'),
                log_action=action,
                log_postID=kwargs.get('postID'),
                log_postType = kwargs.get('postType'),
                log_postTitle = kwargs.get('postTitle'),
                log_postPrivacy = kwargs.get('postPrivacy'),
                log_content = kwargs.get('postContent')
            )
            db.session.add(log)
            db.session.commit()
        except:
            print 'error in userLog()'
            db.session.rollback()
    elif kwargs.get('userID') is not None \
        and kwargs.get('username') is not None: # for delete
        try: 
            log = ActivityLog(
                log_userID=kwargs.get('userID', 0),
                log_username=kwargs.get('username', "NULL"),
                log_postID=kwargs.get('postID', "NULL"),
                log_action=action
            )
            db.session.add(log)
            db.session.commit()
        except:
            print 'only have username and action'
            db.session.rollback()
    else:
        try: 
            log = ActivityLog(
                log_action='FAIL IN POSTLOG'
            )
            db.session.add(log)
            db.session.commit()
        except:
            print 'error in postLog() with no action'
            db.session.rollback()

##########################################
###### Trigger for Comment logging #######
##########################################
def commentLog(action, postID, userID, username, content): 

    try: 
        log = ActivityLog(
            log_postID=postID,
            log_userID=userID,
            log_username=username,
            log_action=action,
            log_content=content
        )
        db.session.add(log)
        db.session.commit()
    except:
        print 'error in commentLog()'
        db.session.rollback()
    
