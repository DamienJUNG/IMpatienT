from typing import List,Optional
from sqlalchemy import Column, Integer, String, Float, ForeignKey,DateTime,Boolean, Table,Enum
from sqlalchemy.orm import relationship,backref,Mapped,mapped_column
from sqlalchemy.ext.mutable import MutableList
from database.db import Base
import datetime
import enum

roles_access = Table('roleAccess',
    Base.metadata,
    Column('module_id', Integer, ForeignKey('module.id'), primary_key=True),
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True)
)

class Role(Base):
    __tablename__ = 'roles'
    id: Mapped[int] = mapped_column(primary_key=True)
    name = Column(String,unique=True)
    def as_dict(self):
       return {'name':self.name,'id':self.id}
    
modules_access = Table('modules',
    Base.metadata,
    Column('module_id', Integer, ForeignKey('module.id'), primary_key=True),
    Column('page_id', Integer, ForeignKey('page.id'), primary_key=True)
)

class Page(Base):
    __tablename__ = "page"
    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    name = Column(String,unique=True)

    def as_dict(self):
       return {'id':self.id,'name':self.name}


class Module(Base):
    __tablename__ = "module"
    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    name = Column(String,unique=True)
    pages = relationship('Page',secondary=modules_access,backref='module',lazy='subquery')

    def as_dict(self):
       return {'id':self.id,'name':self.name}
    
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True,autoincrement=True,unique=True)
    username = Column(String(255), unique=True)
    password = Column(String(255), nullable=False)
    is_active = Column(Boolean)
    is_authenticated = Column(Boolean)
    roles_id: Mapped[int] = mapped_column(ForeignKey("roles.id")) 
    # Pour une raison que j'ignore à la place de mettre l'id comme demandé sqlalchemy a placé le nom du rôle
    roles: Mapped["Role"] = relationship()

    def get_role(self):
        return self.roles_id

    def as_dict(self):
       return {'username':self.username,'role':self.roles_id}
    
    def to_json(self):        
        return {"username": self.username}       

    def is_authenticated(self):
        return self.is_authenticated

    def is_active(self):   
        return self.is_active           
    
    def get_id(self):         
        return str(self.id)


class Project(Base):
    """Database table for projects"""
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True,autoincrement=True)
    name=Column(String(140), nullable=False)
    director_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    archived=Column(String(10), nullable=False)
    reports:Mapped[List["Report"]] = relationship(back_populates="project")

    def set_status(self,status):
        self.archived = status

    def as_dict(self):
       return {'id':self.id,'name':self.name,'director_id':self.director_id,'archived':self.archived}

class Report(Base):
    """Database table for medical reports"""
    __tablename__ = 'reports'
    id = Column(Integer, primary_key=True,autoincrement=True)
    name=Column(String(140), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    patient_id = Column(String(100), index=True, nullable=False)
    report_path = Column(String(4096), unique=True, nullable=True)

    images:Mapped[List["Image"]] = relationship(back_populates="report")

    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    project: Mapped["Project"] = relationship(back_populates="reports")

    present_terms=Column(String,nullable=True)
    absent_terms=Column(String,nullable=True)

class Image(Base):
    """Database table for Image & annotations"""
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True,autoincrement=True)
    image_name = Column(String(140), nullable=False)
    expert_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    patient_id = Column(String(100), index=True, nullable=False)
    biopsy_id = Column(String(100), index=True)
    type_coloration = Column(String(140))
    age_at_biopsy = Column(Integer, default=-1)
    image_path = Column(String(4096), unique=True, nullable=False)
    sigma_range_min = Column(Float())
    sigma_range_max = Column(Float())
    diagnostic = Column(String(140), index=True)
    seg_matrix_path = Column(String(4096), unique=True)
    mask_image_path = Column(String(4096), unique=True)
    blend_image_path = Column(String(4096), unique=True)
    classifier_path = Column(String(4096), unique=True)
    mask_annot_path = Column(String(4096), unique=True)
    class_info_path = Column(String(4096), unique=True)

    report_id: Mapped[int] = mapped_column(ForeignKey("reports.id"))
    report: Mapped["Report"] = relationship(back_populates="images")

    datetime = Column(
        DateTime(),
        onupdate=datetime.date.today(),
        default=datetime.date.today(),
    )

    def __repr__(self):
        return "<Image Name {} Patient {}>".format(self.image_name, self.patient_id)

    def isduplicated(self):
        """Method to check if the image is already in the
        database (same name and patient ID)

        Returns:
            bool: True if the image is already in the database, False otherwise
        """
        if (
            Image.query.filter_by(
                image_name=self.image_name, patient_id=self.patient_id
            ).first()
            is None
        ):
            return False
        else:
            return True