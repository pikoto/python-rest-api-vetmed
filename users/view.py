# coding=utf-8
from flask import jsonify, request, make_response 

from src.entities.entity import Session

from src.users.usr import Role, UserInfo, User, Sess
from src.users.usr import RoleSchema, RoleFullSchema, RoleTeamSchema
from src.users.usr import UsersInfoSchema, UsersTeamSchema, UserInfoFullSchema, UsersInfoTeamSchema, UserInfoRoleTeamSchema, UsersInfoTeamRoleSchema
from src.users.usr import UserSchema, UserFullSchema
from src.users.usr import SessSchema

class RoleView():

    def get_role(self):
        session = Session()
        role_objects = session.query(Role).filter(Role.deleted.is_(False)).all()
        schema = RoleSchema(many=True)
        roles = schema.dump(role_objects)
        session.close()
        return jsonify(roles.data)
        #resp = make_response(jsonify(roles.data))
        #resp.set_cookie('session_id', 'I am cookie')
        #return resp 
    
    def get_role_full(self):
        session = Session()
        role_objects = session.query(Role).all()
    
        schema = RoleFullSchema(many=True)
        roles = schema.dump(role_objects)
    
        session.close()
        return jsonify(roles.data)

    def add_role(self):
        posted_role = RoleSchema(only=('name', 'description', 'is_team'))\
            .load(request.get_json())
    
        role = Role(**posted_role.data, created_by="HTTP post request")
    
        session = Session()
        session.add(role)
        session.commit()
    
        new_role = RoleSchema().dump(role).data
        session.close()
        return jsonify(new_role), 201

    def update_role(self):
        posted_role = RoleSchema(only=('id', 'name', 'description', 'update_by', 'is_team'))\
            .load(request.get_json())
    
        session = Session()
    
        role = session.query(Role).filter(Role.id == posted_role.data['id']).one()
        
        role.update(posted_role.data['name'], posted_role.data['description'], posted_role.data['update_by'], posted_role.data['is_team']) 
    
        session.commit()
    
        update_role = session.query(Role).filter(Role.id == posted_role.data['id'], Role.deleted == False).one()
    
        update_role = RoleSchema().dump(role).data
        session.close()
        
        return jsonify(update_role), 201

    def update_del_role(self):
        posted_role = RoleSchema(only=('id_del', 'deleted_by'))\
            .load(request.get_json())
    
        session = Session()
    
        role = session.query(Role).filter(Role.id == posted_role.data['id_del'], Role.deleted == False).one()
        
        role.update_del(posted_role.data['deleted_by'])
    
        session.commit()
    
        update_role = session.query(Role).filter(Role.id == posted_role.data['id_del'], Role.deleted == True).one()
    
        update_role = RoleSchema().dump(role).data
        session.close()
        
        return jsonify(update_role), 201

class UserView():
    
    def get_user(self):
        session = Session()
        user_objects = session.query(User).filter(User.deleted == False)    
        schema = UserSchema(many=True)
        users = schema.dump(user_objects)
    
        session.close()
        return jsonify(users.data)
    
    def get_user_full(self):
        session = Session()
        user_objects = session.query(User).all()
        schema = UserFullSchema(many=True)
        users = schema.dump(user_objects)
    
        session.close()
        return jsonify(users.data)
    
    def add_user(self):
        posted_user = UserSchema(only=('login', 'password', 'first_name', 'last_name', 'science_degree', 'role_id'))\
            .load(request.get_json())
    
        user = User(**posted_user.data, created_by="HTTP post request")
    
        session = Session()
        
        session.add(user)
        session.commit()
    
        new_user = UserSchema().dump(user).data
        session.close()
        return jsonify(new_user), 201
    
    def password_check_user(self):
        posted_user = UserSchema(only=('login', 'password'))\
            .load(request.get_json())
    
        session = Session()
    
        users = session.query(User).filter(User.login == posted_user.data['login']).one()
    
        session.close()
        
        passw = users.check_password(posted_user.data['password'])
        
        return jsonify(passw), 201
    
    def update_user(self):
        posted_user = UserSchema(only=('id', 'first_name', 'last_name', 'science_degree', 'update_by', 'role_id'))\
            .load(request.get_json())
    
        session = Session()
    
        user = session.query(User).filter(User.id == posted_user.data['id'], User.deleted.is_(False)).one()
        
        user.update(posted_user.data['first_name'], posted_user.data['last_name'],
                    posted_user.data['science_degree'], posted_user.data['update_by'])
        
        #if posted_user.data['role_id'] != None:
        user.update_role(posted_user.data['role_id'], posted_user.data['update_by'])
            
        session.commit()
    
        update_user = session.query(User).filter(User.id == posted_user.data['id']).one()
    
        update_user = RoleSchema().dump(user).data
        session.close()
        
        return jsonify(update_user), 201
    
    def update_del_user(self):
        posted_user = UserSchema(only=('id_del', 'deleted_by'))\
            .load(request.get_json())
    
        session = Session()
    
        user = session.query(User).filter(User.id == posted_user.data['id_del'], User.deleted.is_(False)).one()
        
        user.update_del(posted_user.data['deleted_by'])
    
        session.commit()
    
        update_user = session.query(User).filter(User.id == posted_user.data['id_del'], User.deleted.is_(True)).one()
    
        update_user = UserSchema().dump(user).data
        session.close()
        
        return jsonify(update_user), 201
    
    
    def get_user_info(self):
        session = Session()
        user_objects = session.query(UserInfo).filter(User.deleted.is_(False)).all()
        schema = UsersInfoSchema(many=True)
        users = schema.dump(user_objects)
        session.close()
        return jsonify(users.data)
    
    def get_user_info_full(self):
        session = Session()
        user_objects = session.query(UserInfo).all()
        schema = UserInfoFullSchema(many=True)
        users = schema.dump(user_objects)
        session.close()
        return jsonify(users.data)
        
    def add_user_info(self):
        posted_user = UsersInfoSchema(only=('user_id', 'description', 'description2' ))\
            .load(request.get_json())
    
        user = UserInfo(**posted_user.data, created_by="HTTP post request")
    
        session = Session()
        
        session.add(user)
        session.commit()
    
        new_user = UsersInfoSchema().dump(user).data
        session.close()
        return jsonify(new_user), 201    
    
    def update_user_info(self):
        posted_user = UsersInfoSchema(only=('id', 'description', 'description2', 'update_by'))\
            .load(request.get_json())
    
        session = Session()
    
        user = session.query(UserInfo).filter(UserInfo.id == posted_user.data['id'], UserInfo.deleted.is_(False)).one()
        
        user.update(posted_user.data['description'], posted_user.data['description2'], posted_user.data['update_by'])
        
        session.commit()
    
        update_user = session.query(UserInfo).filter(UserInfo.id == posted_user.data['id']).one()
    
        update_user = UsersInfoSchema().dump(user).data
        session.close()
        
        return jsonify(update_user), 201    
    
    def update_del_user_info(self):  
        posted_user = UsersInfoSchema(only=('id_del', 'deleted_by'))\
            .load(request.get_json())
    
        session = Session()
    
        user = session.query(UserInfo).filter(UserInfo.id == posted_user.data['id_del'], UserInfo.deleted.is_(False)).one()
        
        user.update_del(posted_user.data['deleted_by'])
    
        session.commit()
    
        update_user = session.query(UserInfo).filter(UserInfo.id == posted_user.data['id_del'], UserInfo.deleted.is_(True)).one()
    
        update_user = UserInfo().dump(user).data
        session.close()
        
        return jsonify(update_user), 201        
    
class TeamView():
    def get_users_team(self):
        session = Session()
        user_objects = session.query(User).join(Role).filter(User.deleted.is_( False ), Role.is_team.is_( True ))
        schema = UsersTeamSchema(many=True)
        users = schema.dump(user_objects)
        session.close()
        return jsonify(users.data)    
   
    def get_role_team(self):
        session = Session()
        user_objects = session.query(Role).filter(Role.is_team.is_(True ))
        schema = RoleSchema(many=True)
        users = schema.dump(user_objects)
        session.close()
        return jsonify(users.data)       

    def get_info_user(self):
        session = Session()
        print( session.query(UserInfo).join(User).all() )
        user_objects =  session.query(UserInfo).join(User).filter(User.deleted.is_( False )).all()
        schema = UsersInfoTeamSchema(many=True)
        users = schema.dump(user_objects)
        session.close()
        return jsonify(users.data)   
   
    def get_info_user_role_team(self):
        session = Session()
        print( session.query(UserInfo).join(User).all() )
        user_objects =  session.query(UserInfo).join(User).join(Role).filter(Role.is_team.is_( True ), User.deleted.is_( False ) ).all()
        schema = UsersInfoTeamRoleSchema(many=True)
        users = schema.dump(user_objects)
        session.close()
        return jsonify(users.data)     
    
                          
class SessView():
    def get_sessions(self):
        session = Session()
        sess_objects = session.query(Sess).all()
    
        schema = SessSchema(many=True)
        sess = schema.dump(sess_objects)
    
        session.close()
        return jsonify(sess.data)        
