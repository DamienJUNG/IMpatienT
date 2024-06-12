from database.db import db_session
from database.models import Module,Page,modules_access

def create_module(module_name):
    try:
        if not db_session.query(Module).filter_by(name=module_name).one_or_none():
            db_session.add(Module(name=module_name))
            db_session.commit()
            return True
    except Exception as ex:
        print(ex)
        return False
    
def delete_module(module_name):
    try:
        module = db_session.query(Module).filter_by(name=module_name).one_or_none()
        if module:
            db_session.delete(module)
            db_session.commit()
            return True
    except Exception as ex:
        print(ex)
        return False
    
def add_page_to_module(module_id,page_id):
    try:
        module = db_session.get(Module,{'id':module_id})
        page = db_session.get(Page,{'id':page_id})
        # print(module,page)
        if module and page:
            module.pages.append(page)
            db_session.commit()
            # print(module.pages)
    except Exception as ex:
        print(ex)
        return False
    finally:
        return True
    
def get_all_modules():
    modules = []
    try:
        modules = db_session.query(Module).all()
    except Exception as ex:
        print(ex)
    finally:
        return [module.as_dict() for module in modules]
    
def get_module(module_id):
    try:
        return db_session.query(Module).filter_by(id=module_id).first()
    except Exception as ex:
        print(ex)
        return None
    
def get_pages_of_module(module_name):
    try:
        module = db_session.query(Module).filter_by(name=module_name).first() 
        if module :
            assoc = db_session.query(modules_access).filter_by(module_id=module.id)
            pages = [item.page_id for item in assoc]
            return pages 
        else : return None
    except Exception as ex:
        print(ex)
        return None
    
def update_module_access(module_name,moduleAccess):
    try:
        module = db_session.query(Module).filter_by(name=module_name).one_or_none()
        accessible_pages_ids = [db_session.query(Page).filter_by(name=page_name).one_or_none().id for page_name in moduleAccess]
        if module:
            assoc = db_session.query(modules_access).filter_by(module_id=module.id).all()
            # Pour chaque association, si il y en a une dans bdd qui n'a pas été cochée cette fois-ci alors on la supprimee
            for access in assoc:
                # C'est pas joli d'accéder comme ça à l'id de la page, mais avec sqlalchemy il ne donne que des tuples pour les associations...
                if access[1] not in accessible_pages_ids:
                    db_session.query(modules_access).filter_by(module_id=access[0],page_id=access[1]).delete()
            page_ids = [item.page_id for item in assoc]
            # Pour chaque page sélectionnée, si l'association n'existe pas déjà alors on la créé
            for id in accessible_pages_ids:
                if id not in page_ids:
                    statement = modules_access.insert().values(page_id=id,module_id=module.id)
                    db_session.execute(statement)
            db_session.commit()
        return True
    except Exception as ex:
        print("update module access",ex)
        return False
