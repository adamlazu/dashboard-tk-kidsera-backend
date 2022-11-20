from flask import Blueprint,current_app,request,jsonify
from.db import insert_user, get_user, block_token
from flask_restful import Api, Resource
from hashlib import md5
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_jwt
import datetime

bp = Blueprint('auth', name)
api = Api(bp)

class Register(Resource):
    def post(self):
        email = request.form['email']
        username = request.form['username']
        if get_user({'email':email}) == None and get_user({'username': username}) == None:
            data = {'email' : email,
            'username' : username,
            'password' : md5(request.form['password'].encode('utf-8')).hexdigest(),
            'first_name' : request.form['fname'],
            'last_name' : request.form['lname'],
            'is_admin': False}
            insert_user(data)
            access_token = create_access_token(identity=email)
            return {'success':True,'access_token': access_token}
        elif get_user({'email':email}) == None:
            return{'success':False,'message': 'email is already used'}
        else:
            return{'success':False,'message': 'username is already used'}


api.add_resource(Register,'/API/auth/register')

class Login(Resource):
    def post(self):
        email = request.form['email']
        password = md5(request.form['password'].encode('utf-8')).hexdigest()
        data = get_user({'email':email})
        if data['password']==password:
            access_token = create_access_token(identity=email)
            return {'success':True,'access_token': access_token}
        else:
            return {'success':False, 'message':'wrong password or email'}


api.add_resource(Login,'/API/auth/login')
