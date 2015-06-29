#######################
####### imports #######
#######################
from App.models import Users, Posts, Comments, HashLog
from App import db
import hashlib
import sha3
from datetime import datetime
from sqlalchemy import desc

##########################
###### Make A Hash #######
##########################
def makeHash(data):
    s = hashlib.sha3_512()
    s.update(data)
    return s.hexdigest()

######################################
###### First Hash After Logout #######
######################################
def addOrgHash(username):

        # get the data that you want to generate 
        data = getData(username)
        # data = getData()

        # make a hash
        hash_data = makeHash(data)
        
        try: 
            db.create_all()
            myHash = HashLog(
                    hash_name=username,
                    hash_org=hash_data
                ) 
            db.session.add(myHash)
            db.session.commit()
        except:
                print 'error in addOrgHash()'
                db.session.rollback()

###################################################
###### Second Hash for Comparing when Login #######
###################################################
def addCompHash(username):

        # get the data that you want to generate 
        data = getData(username)
        # data = getData()

        # make a hash
        hash_data = makeHash(data)

        try: 
            # first time login, so nothing to compare, just add the new org hash 
            exist_user = HashLog.query.filter(HashLog.hash_name == username).first()
            if exist_user is None:
                myHash = HashLog(
                    hash_name=username,
                    hash_org=hash_data
                ) 
                db.create_all()
                db.session.add(myHash)
                db.session.commit()
            else:
                db.create_all()
                # get the id of last login user to compare
                lastSeenID = db.session.query(HashLog).with_entities(HashLog.hash_id) \
                                .filter(HashLog.hash_name == username) \
                                .order_by(desc(HashLog.hash_id)).first()
                # Save the hash into db
                db.session.query(HashLog).filter(HashLog.hash_id == lastSeenID[0])\
                        .update({'hash_comp': hash_data, 'hash_time': datetime.now()})
                
                db.session.commit()
        except:
            print 'error in addCompHash()'
            db.session.rollback()

######################################
###### Compare Hash1 and Hash2 #######
######################################
def compHash(orgHash, compHash):    
    if orgHash == compHash:
        return True
    else:   
        return  False

##########################################
###### Check If both Hash Are Same #######
##########################################
def isHack(username):
    
    hash1 = HashLog.query.with_entities(HashLog.hash_org).filter(HashLog.hash_name == username)\
                    .order_by(desc(HashLog.hash_time)).first()
    hash2 = HashLog.query.with_entities(HashLog.hash_comp).filter(HashLog.hash_name == username)\
                    .order_by(desc(HashLog.hash_time)).first()

    # get the id of last login user to compare
    lastSeenID = db.session.query(HashLog).with_entities(HashLog.hash_id) \
                    .filter(HashLog.hash_name == username) \
                    .order_by(desc(HashLog.hash_time)).first()

    # if the hashes are the same, then it doesnt get hacked
    if compHash(hash1, hash2):
        return False
    else: # if not then there is some external modify, or might get hacked 
        try: 
            db.create_all()
            db.session.query(HashLog).filter(HashLog.hash_id == lastSeenID[0])\
                    .update({'hash_isHack': 'isHack'})
            db.session.commit()
            return True
        except:
            print 'error in update isHack()'
            db.session.rollback()
    
        return True

#######################################
###### Prepare Data for Hashing #######
#######################################
def getData(username):
    pwd = Users.query.with_entities(Users.user_password)\
            .filter(Users.user_name == username).first()
    # use pwd[0]

    # all post in each account
    posts = Posts.query.join(Users).add_columns(Users.user_name, Posts.post_id, Posts.post_title, \
                Posts.post_type, Posts.post_time, Posts.post_privacy) \
                .filter(Posts.post_authorID == Users.user_id) \
                .filter(Users.user_name == username).all()

    # all comments
    comments = Comments.query.all()

    data = ''
    for post in posts:
        for p in post:
            if p == u'\u2028':
                p.replace(u'\u2028', '')
            data = data+str(p)

    for comment in comments:
        data = data+str(comment)
    
    data = username + pwd[0] + data 

    return data.encode('utf-8')


#####################################
###### For Future Development #######
#####################################


#########################
###### Users Data #######
#########################
def getUsersData():
    users = Users.query.with_entities(Users.user_name).all()
    pwds = Users.query.with_entities(Users.user_password).all()
    data = ''
    for user in users:
        data += str(user)
    for pwd in pwds:
        data += str(pwd)
    return data.encode('utf-8')

#########################
###### Posts Data #######
#########################
def getPostsData():
    posts = Posts.query.with_entities(Posts.post_id, Posts.post_type, Posts.post_title, \
                    Posts.post_privacy, Posts.post_content, Posts.post_authorID).all()
    data = ''
    for post in posts:
        data += str(post)
    return data.encode('utf-8')

############################
###### Comments Data #######
############################
def getCommentsData():
    comments = Comments.query.with_entities(Comments.comment_id, Comments.comment_content, Comments.comment_time, \
                    Comments.comment_owner, Comments.comment_postID).all()
    data = ''
    for comment in comments:
        data += str(comment)
    return data.encode('utf-8')


# def getData():
#     data = db.session.query(Posts, Comments).all()
#     data = str(data)
#     return data.encode('utf-8') 




