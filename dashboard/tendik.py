from flask import Blueprint, request
from flask_restful import Api, Resource
from bson.json_util import dumps
from bson.objectid import ObjectId
from .db import get_tendiks, insert_tendik, get_user, get_tendik,update_tendik,delete_tendik
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_jwt
import json

bp = Blueprint('tendik', __name__)
api = Api(bp)

class Tendik_list(Resource):
    def get(self):
        data = get_tendiks()
        return json.loads(dumps(data))
    
    @jwt_required()
    def post(self):
        user = get_jwt_identity()
        userDetail = get_user({"username":user})
        if userDetail['is_admin']:
            req = request.form
            data = {
                'nama':req.get('nama'),
                'jenis_kelamin':req.get('jenis_kelamin'),
                'ttl':req.get('ttl'),
                'alamat':req.get('alamat'),
                'no_hp':req.get('no_hp'),
                'email':req.get('email'),
                'pendidikan_terakhir':req.get('pendidikan_terakhir')
            }
            insert_tendik(data)
            return{"success":True}
        else:
            return{"success":False, "msg":"only admin can perform this action"}




api.add_resource(Tendik_list,'/API/tendik')

class Tendik(Resource):
    def get(self, tendik_id):
        ObjInstance = ObjectId(tendik_id)
        filter = {'_id':ObjInstance}
        data = get_tendik(filter)
        return json.loads(dumps(data))
