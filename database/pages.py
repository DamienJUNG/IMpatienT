from database.db import db_session
from database.models import Page

def create_page(pageName):
    try:
        if not db_session.query(Page).filter_by(name=pageName).one_or_none():
            db_session.add(Page(name=pageName))
            db_session.commit()
    except Exception as ex:
        print(ex)
        return False
    finally:
        return True
    
def get_all_pages():
    pages = []
    try:
        pages = db_session.query(Page).all()
    except Exception as ex:
        print(ex)
    finally:
        return [page.as_dict() for page in pages]