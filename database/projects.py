from database.models import Project
from database.db import db_session 

def create_project(project_name,director_id):
    try:
        if not db_session.query(Project).filter_by(name=project_name).one_or_none():
            db_session.add(Project(name=project_name,director_id=director_id,archived="ACTIVE"))
            db_session.commit()
            return True
    except Exception as ex:
        print(ex)
        return False
    
def set_project_status(project_id,status):
    try:
        project = db_session.query(Project).filter_by(name=project_id).one_or_none()
        if project:
            project.set_status(status)
            db_session.commit()
            return True
    except Exception as ex:
        print(ex)
        return False

def get_all_project():
    projects = []
    try:
        projects = db_session.query(Project).all()
    except Exception as ex:
        print(ex)
    finally:
        return [project.as_dict() for project in projects]
    
def get_project(project_id):
    project = None
    try:
        project = db_session.query(Project).filter_by(id=project_id).first()
        return project
    except Exception as ex:
        print(ex)
        return None
    
def delete_project(project_id):
    try:
        project = db_session.query(Project).filter_by(id=project_id).one_or_none()
        if project:
            db_session.delete(project)
            db_session.commit()
            return True
    except Exception as ex:
        print(ex)
        return False