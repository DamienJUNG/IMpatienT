from database.models import Image
from database.db import db_session 
from database import modules

def create_image(image_name,expert_id,patient_id,biopsy_id,age_at_biopsy,image_path,report_id):
    try:
        if not db_session.query(Image).filter_by(image_name=image_name).one_or_none():
            db_session.add(Image(
                image_name,
                expert_id,
                patient_id,
                biopsy_id,
                age_at_biopsy,
                image_path,
                report_id
            ))
            db_session.commit()
            return True
    except Exception as ex:
        print(ex)
        return False
    
def delete_image(image_id):
    try:
        image = db_session.query(Image).filter_by(id=image_id).one_or_none()
        if image:
            db_session.delete(image)
            db_session.commit()
            return True
    except Exception as ex:
        print(ex)
        return False

def get_all_image():
    images = []
    try:
        images = db_session.query(Image).all()
    except Exception as ex:
        print(ex)
    finally:
        return [image for image in images]