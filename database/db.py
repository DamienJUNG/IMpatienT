from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,scoped_session
from sqlalchemy.ext.serializer import dumps, loads
from sqlalchemy.ext.declarative import declarative_base

db_path = 'sqlite:///database/sqlite.db'

engine = create_engine(db_path)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def try_connection():
    try:
        conn = engine.connect()
        return True
    except Exception as ex:
        print(ex)
        return False
    
def generate_all():
    try:
        Base.metadata.create_all(bind=engine)
        db_session.commit()
        return True
    except Exception as ex:
        print(ex)
        return False