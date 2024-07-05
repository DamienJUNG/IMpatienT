from database.models import Report
from database.db import db_session 
from database import modules

def create_report(project_id,author_id,report_name,patient_id,present_terms=None,absent_terms=None):
    try:
        if not db_session.query(Report).filter_by(name=report_name).one_or_none():
            db_session.add(Report(
                name=report_name,
                project_id=project_id,
                author_id=author_id,
                patient_id=patient_id,
                present_terms=present_terms,
                absent_terms=absent_terms
            ))
            db_session.commit()
            return True
    except Exception as ex:
        print(ex)
        return False
    
def delete_report(report_id):
    try:
        report = db_session.query(Report).filter_by(id=report_id).one_or_none()
        if report:
            db_session.delete(report)
            db_session.commit()
            return True
    except Exception as ex:
        print(ex)
        return False

def get_all_report():
    reports = []
    try:
        reports = db_session.query(Report).all()
    except Exception as ex:
        print(ex)
    finally:
        return [report for report in reports]