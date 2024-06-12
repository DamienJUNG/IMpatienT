from typing import List,Optional
from sqlalchemy import Column, Integer, String, Float, ForeignKey,DateTime,Boolean, Table
from sqlalchemy.orm import relationship,backref,Mapped,mapped_column
from sqlalchemy.ext.mutable import MutableList
from database.db import Base

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
    # Pour une raison que j'ignore à la place de mettre l'id comme demandé sqlalchemy a placé le rôle
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