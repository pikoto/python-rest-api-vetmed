# coding=utf-8

from datetime import datetime
from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.sqltypes import Boolean


db_url = 'localhost:5432'
db_name = 'vetmed'
db_user = 'vetmed'
db_password = 'vetmed'

engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_url}/{db_name}')
Session = sessionmaker(bind=engine)

Base = declarative_base()

class Entity():
    id = Column(Integer, nullable=False, unique=True, primary_key=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    class Meta:
        ordered = True

    def __init__(self):
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def update_entity(self):
        self.updated_at = datetime.now()      

class EntityBiz(Entity):
    created_by = Column(String, nullable=True)
    last_updated_by = Column(String, nullable=True)
    deleted = Column(Boolean)
    deleted_at = Column(DateTime, nullable=True)
    deleted_by = Column(String)

    class Meta:
        ordered = True

    def __init__(self, created_by):
        Entity.__init__(self)
        self.last_updated_by = created_by
        self.deleted = False
        self.deleted_at = None
        self.deleted_by = None
    
    def update_entity(self, update_by):
        self.last_updated_by = update_by
        self.updated_at = datetime.now()  
        
    def update_del_entity(self, deleted_by):
        self.deleted = True
        self.deleted_by = deleted_by
        self.deleted_at = datetime.now()


