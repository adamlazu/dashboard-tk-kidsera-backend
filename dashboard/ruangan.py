from flask import Blueprint, request
from flask_restful import Api, Resource
from bson.json_util import dumps
from bson.objectid import ObjectId
from .db import get_ruangans, get_user, insert_ruangan
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_jwt
import json

bp = Blueprint("ruangan",__name__)
api = Api(bp)

class RuanganList(Resource):
    def get(self):
        data = get_ruangans()
        return json.loads(dumps(data))

    @jwt_required()
    def post(self):
        user = get_jwt_identity()
        userDetail = get_user({"username":user})
        if userDetail['is_admin']:
            req = request.form
            data = {
                "nama_ruangan":req.get('nama_ruangan')
            }
            insert_ruangan(data)
            return{"success":True}
        else:
            return{"success":False, "msg":"only admin can perform this action"}


api.add_resource(RuanganList, "/API/ruangan")

