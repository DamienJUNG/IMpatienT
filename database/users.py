from database.models import User
from database.db import db_session

from werkzeug.security import generate_password_hash, check_password_hash

def add_user(username,password,role):
    try:
        user = User(username=username,password=generate_password_hash(password),roles_id=role)
        db_session.add(user)
        db_session.commit()
            
    except Exception as ex:
        print(ex)
        return False
    finally:
        return True
    
def get_user(username):
    try:
        user = db_session.query(User).filter_by(username=username).first()
    except Exception as ex:
        print(ex)
    finally:
        print(username,user)
        return user
    
def get_user_by_id(id):
    try:
        user = db_session.query(User).filter_by(id=id).first()
    except Exception as ex:
        print(ex)
    finally:
        # print(id,user)
        return user
    
def get_all_users():
    users = []
    try:
        users = db_session.query(User).all()
    except Exception as ex:
        print(ex)
    finally:
        return [user.as_dict() for user in users]
    
def verify_user(username,password):
    try:
        user = db_session.query(User).filter_by(username=username).first()
        if user == None:
            return False
        # print(password,user.password,check_password_hash(user.password,password))
        return check_password_hash(user.password,password)
    except Exception as ex:
        print(ex)
        return False