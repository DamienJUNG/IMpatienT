from database.models import Role,roles_access,Module,Table
from database.db import db_session 
from database import modules

def create_role(role_name):
    try:
        if not db_session.query(Role).filter_by(name=role_name).one_or_none():
            db_session.add(Role(name=role_name))
            db_session.commit()
            return True
    except Exception as ex:
        print(ex)
        return False
    
def delete_role(role_name):
    try:
        role = db_session.query(Role).filter_by(name=role_name).one_or_none()
        if role:
            db_session.delete(role)
            db_session.commit()
            return True
    except Exception as ex:
        print(ex)
        return False

def get_all_roles():
    roles = []
    try:
        roles = db_session.query(Role).all()
    except Exception as ex:
        print(ex)
    finally:
        return [role.as_dict() for role in roles]
    
def get_role_accessible_pages(roleName):
    try:
        role = db_session.query(Role).filter_by(name=roleName).one_or_none()
        if role:
            pages = []
            for access in db_session.query(roles_access).filter_by(role_id=role.id).all():
                module = modules.get_module(access.module_id)
                for page in module.pages : 
                    pages.append("/"+page.name)
        return pages
    except Exception as ex:
        print("ex",ex)
        return None
    
def get_role_access(roleName):
    try:
        role = db_session.query(Role).filter_by(name=roleName).one_or_none()
        if role:
            role_modules = []
            for access in db_session.query(roles_access).filter_by(role_id=role.id).all():
                role_modules.append(modules.get_module(access.module_id).name)
        return role_modules
    except Exception as ex:
        print("ex",ex)
        return None

def update_role_access(role_name,roleAccess):
    try:
        role = db_session.query(Role).filter_by(name=role_name).one_or_none()
        new_accessible_modules_ids = [db_session.query(Module).filter_by(name=module_name).one_or_none().id for module_name in roleAccess]
        if role:
            assoc = db_session.query(roles_access).filter_by(role_id=role.id).all()
            # print("assoc",assoc)
            for access in assoc:
                if access[0] not in new_accessible_modules_ids:
                    db_session.query(roles_access).filter_by(module_id=access[0],role_id=access[1]).delete()
            modules_ids = [module.module_id for module in assoc]
            for id in new_accessible_modules_ids:
                if id not in modules_ids:
                    statement = roles_access.insert().values(module_id=id,role_id=role.id)
                    db_session.execute(statement)
            db_session.commit()
        return True
    except Exception as ex:
        print("ex",ex)
        return False