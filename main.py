# coding=utf-8

from datetime import datetime

from flask_cors import CORS, cross_origin
from flask import Flask, jsonify
from flask_bcrypt import Bcrypt
#from wtforms.csrf.core import CSRF 
#, CsrfProtect

from src.entities.entity import Base, engine 
from src.users.view import RoleView, UserView, SessView, TeamView


# creating the Flask application
app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
bcrypt = Bcrypt(app)
#CsrfProtect(app)

# if needed, generate database schema
Base.metadata.create_all(engine)

#comment
#comment2

role = RoleView()
user = UserView()
sess = SessView()
team = TeamView()

@app.errorhandler(404)
def page_not_found(error):
    return jsonify({"error" : "page_not_found"}), 404    


@app.route('/api/role')
@cross_origin()
def get_role():
    try:
        return role.get_role()
    except Exception as e:
        return jsonify(error = str(e)), 500     
    
@app.route('/api/role_full')
def get_role_full():
    try:
        return role.get_role_full()
    except Exception as e:
        return jsonify(error = str(e)), 500   

@app.route('/api/role', methods=['POST'])
def add_role():
    try:
        return role.add_role()
    except Exception as e:
        return jsonify(error = str(e)), 500   

@app.route('/api/role_update', methods=['POST'])
def update_role():
    try:
        return role.update_role()
    except Exception as e:
        return jsonify(error = str(e)), 500  

@app.route('/api/role_update_del', methods=['POST'])
def update_del_role():
    try:
        return role.update_del_role()
    except Exception as e:
        return jsonify(error = str(e)), 500  


@app.route('/api/user')
def get_user():
    try:
        return user.get_user()
    except Exception as e:
        return jsonify(error = str(e)), 500 

@app.route('/api/user_full')
def get_user_full():
    try:
        return user.get_user_full()
    except Exception as e:
        return jsonify(error = str(e)), 500

@app.route('/api/team')
def get_users_team():
    try:
        return team.get_users_team()
    except Exception as e:
        return jsonify(error = str(e)), 500
    
@app.route('/api/team_role')
def get_role_team():
    try:
        return team.get_role_team()
    except Exception as e:
        return jsonify(error = str(e)), 500

@app.route('/api/team_info')
def get_info_user():          
    try:
        return team.get_info_user()
    except Exception as e:
        return jsonify(error = str(e)), 500
    
@app.route('/api/team_role_user_info')
def get_info_user_role_team():
    try:
        return team.get_info_user_role_team()
    except Exception as e:
        return jsonify(error = str(e)), 500


    
@app.route('/api/user', methods=['POST'])
def add_user():
    try:
        return user.add_user()
    except Exception as e:
        return jsonify(error = str(e)), 500

@app.route('/api/user_check_password', methods=['POST'])
def password_check_user():
    try:
        return user.password_check_user()
    except Exception as e:
        return jsonify(error = str(e)), 500

@app.route('/api/user_update', methods=['POST'])
def update_user():
    try:
        return user.update_user()
    except Exception as e:
        return jsonify(error = str(e)), 500

@app.route('/api/user_update_del', methods=['POST'])
def update_del_user():
    try:
        return user.update_del_user()
    except Exception as e:
        return jsonify(error = str(e)), 500

@app.route('/api/user_info')
def get_user_info():
    try:
        return user.get_user_info()
    except Exception as e:
        return jsonify(error = str(e)), 500

@app.route('/api/user_info', methods=['POST'])
def add_user_info():
    try:
        return user.add_user_info()
    except Exception as e:
        return jsonify(error = str(e)), 500
    
@app.route('/api/user_info_update', methods=['POST'])
def update_user_info():
    try:
        return user.update_user_info()
    except Exception as e:
        return jsonify(error = str(e)), 500

@app.route('/api/user__info_update_del', methods=['POST'])
def update_del_user_info():
    try:
        return user.update_del_user_info()
    except Exception as e:
        return jsonify(error = str(e)), 500

@app.route('/api/user_info_full')
def get_user_info_full():
    try:
        return user.get_user_info_full()
    except Exception as e:
        return jsonify(error = str(e)), 500
    
@app.route('/api/sessions')
def get_sessions():
    try:
        return sess.get_sessions()
    except Exception as e:
        return jsonify(error = str(e)), 500
