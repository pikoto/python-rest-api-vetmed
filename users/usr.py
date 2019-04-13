# coding=utf-8
from marshmallow import Schema, fields
from sqlalchemy import Column, String, UniqueConstraint, DateTime
from datetime import datetime

from src.entities.entity import Base, Entity, EntityBiz

from sqlalchemy.sql.sqltypes import INTEGER
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Boolean
from sqlalchemy.sql import expression
from marshmallow.fields import Nested
from flask_bcrypt import generate_password_hash, check_password_hash

class Role(EntityBiz, Base):
    __tablename__ = 'usr_role'
    __table_args__ = (UniqueConstraint('name', 'deleted', name='uix_usr_role_name_deleted'),)
    name = Column(String)
    description = Column(String)
    is_team = Column(Boolean, server_default=u'false', nullable=False)
    
    @property
    def serializable(self):
        return {'id': self.id, 'name': self.name, 'description' : self.description, 'is_team' : self.is_team }  

    def __init__(self, name, description, created_by, is_team):
        EntityBiz.__init__(self, created_by)
        self.name = name
        self.description = description
        self.is_team = bool(int(is_team))

    
    def update(self, name, description, update_by, is_team):
        EntityBiz.update_entity(self, update_by)
        self.name = name
        self.description = description
        self.is_team = bool(int(is_team))

    def update_del(self, deleted_by):
        EntityBiz.update_del_entity(self, deleted_by)
    
class RoleSchema(Schema):
    id = fields.Number()
    name = fields.Str()
    description = fields.Str()
    is_team = fields.Str()

class RoleFullSchema(Schema):
    id = fields.Number()
    name = fields.Str()
    description = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    last_updated_by = fields.Str()
    deleted = fields.Str()
    deleted_by = fields.Str()
    is_team = fields.Str()
    
class RoleTeamSchema(Schema):
    id = fields.Number()
    name = fields.Str()
    description = fields.Str()    


    
class User(EntityBiz, Base):
    __tablename__ = 'usr_user'
    __table_args__ = (UniqueConstraint('login', 'deleted', name='uix_usr_user_login_deleted'),)
    
    login = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    
    science_degree = Column(String)
    
    role_id = Column(INTEGER, ForeignKey('usr_role.id'), nullable=False)

    role = relationship('Role', backref='Role', lazy='joined', primaryjoin='Role.id == User.role_id')

    
    def __init__(self, login, password, first_name, last_name, science_degree, created_by, role_id):
        EntityBiz.__init__(self, created_by)
        self.login = login
        self.password = generate_password_hash(password, 12).decode('utf-8')
        self.first_name = first_name
        self.last_name = last_name
        self.science_degree = science_degree
        self.role_id = role_id
        
    def update(self, first_name, last_name, science_degree, update_by):
        EntityBiz.update_entity(self, update_by)
        self.first_name = first_name
        self.last_name = last_name
        self.science_degree = science_degree
        
    def update_del(self, deleted_by):
        EntityBiz.update_del_entity(self, deleted_by)
    
    def update_role(self, role_id, update_by):
        EntityBiz.update_entity(self, update_by)
        self.role_id = role_id
         
        
    def check_password(self, value):
        if not value and not self.password:
            return False
        return check_password_hash(self.password.encode('utf-8'), value.encode('utf-8'))
                        
class UserSchema(Schema):
    id = fields.Number()
    role_id = fields.Number()
    login = fields.Str()
    password = fields.Str()
    first_name = fields.Str()
    last_name = fields.Str()
    science_degree = fields.Str()
    deleted = fields.Bool()

class UserFullSchema(Schema):
    id = fields.Number()
    role_id = fields.Number()
    role = Nested(RoleFullSchema())
    login = fields.Str()
    password = fields.Str()
    first_name = fields.Str()
    last_name = fields.Str()
    science_degree = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    last_updated_by = fields.Str()
    deleted = fields.Str()
    deleted_by = fields.Str()    


class UserInfo(EntityBiz, Base):
    __tablename__ = 'usr_info'
    __table_args__ = (UniqueConstraint('user_id', 'user_id', name='uix_usr_info_user_id_deleted'),)

    user_id = Column(INTEGER, ForeignKey('usr_user.id'), nullable=False)

    description = Column(String)
    description2 = Column(String)
    
    user = relationship('User', backref='User', lazy='joined', primaryjoin='User.id == UserInfo.user_id')    
    
    
    @property
    def serializable(self):
        return {'id': self.id, 'description': self.description, 'description2' : self.description2, 'user_id' : self.user_id }    

    def __init__(self, created_by, description, description2, user_id):
        EntityBiz.__init__(self, created_by)
        self.description = description
        self.description2 = description2
        self.user_id = user_id
        
    def update(self, update_by, description, description2):
        EntityBiz.update_entity(self, update_by)
        self.description = description
        self.description2 = description2
        
    def update_del(self, deleted_by):
        EntityBiz.update_del_entity(self, deleted_by)

class UsersInfoSchema(Schema):
    id = fields.Number()
    user_id = fields.Number()
    description = fields.Str()
    descriptio2 = fields.Str()
 
class UserInfoFullSchema(Schema):
    id = fields.Number()
    user_id = fields.Number()
    user = Nested(UserFullSchema())
    description = fields.Str()
    descriptio2 = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    last_updated_by = fields.Str()
    deleted = fields.Str()
    deleted_by = fields.Str()    
    deleted_at = fields.Str()        

class UsersInfoTeamSchema(Schema):
    description = fields.Str()
    description2 = fields.Str() 
    user = Nested(UserSchema())

class UsersTeamSchema(Schema):
    first_name = fields.Str()
    id = fields.Number()
    login = fields.Str()
    last_name = fields.Str()
    role = Nested(RoleSchema())
    science_degree = fields.Str() 

class UsersInfoTeamRoleSchema(Schema):
    description = fields.Str()
    description2 = fields.Str() 
    user = Nested(UsersTeamSchema())
 
    
class UserInfoRoleTeamSchema(Schema):
    first_name = fields.Str()
    login = fields.Str()
    last_name = fields.Str()
    #role = Nested(RoleTeamSchema())
    science_degree = fields.Str()  
    id = fields.Number()
    info = Nested(UsersInfoTeamSchema)

                
class Sess(Entity, Base):
    __tablename__ = 'usr_sessions'
    sess_key = Column(String)
    expiration_date = Column(DateTime)
    user_id = Column(INTEGER, ForeignKey('usr_user.id'), nullable=False)
    user = relationship('User', lazy='joined', primaryjoin='User.id == Sess.user_id')
   
    def __init__(self, sess_key, user_id, created_by):
        Entity.__init__(self, created_by)
        self.sess_key = sess_key
        self.user_id = user_id
        self.expiration_date = datetime.now()
    
    def update(self, sess_key, user_id, update_by):
        Entity.update_entity(self, update_by)
        self.sess_key = sess_key
        self.user_id = user_id
        
    def update_expiration(self, expiration_date, update_by):
        Entity.update_entity(self, update_by)
        self.expiration_date = expiration_date
        
class SessSchema(Schema):  
    id = fields.Number()
    user_id = fields.Number()
    user = Nested(UserSchema())
    sess_key = fields.Str()
    expiration_date = fields.DateTime()  
 
        
