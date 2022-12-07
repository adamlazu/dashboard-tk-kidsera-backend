from flask import Blueprint, request
from flask_restful import Api, Resource
from bson.json_util import dumps
from bson.objectid import ObjectId
from .db import get_ruangan, get_allsarpras, insert_sarpras, get_user, get_sarpras, update_sarpras, delete_sarpras
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_jwt
import json

bp = Blueprint("sarpras", __name__)
api = Api(bp)

class Sarpras(Resource):
    def get(self, ruangan_id):
        ObjInstance = ObjectId(ruangan_id)
        ruang = get_ruangan({'_id':ObjInstance})
        filter = {'id_ruang':ObjInstance}
        data = get_allsarpras(filter)
        return {"nama_ruangan": ruang['nama_ruangan'],
                "sarpras": json.loads(dumps(data))}
    
    @jwt_required()
    def post(self, ruangan_id):
        user = get_jwt_identity()
        userDetail = get_user({"username":user})
        if userDetail['is_admin']:
            ObjInstance = ObjectId(ruangan_id)
            req = request.form
            data = {
                'nama':req.get('nama'),
                'jenis':req.get('jenis'),
                'jumlah':int(req.get('jumlah')),
                'id_ruang':ObjInstance
            }
            insert_sarpras(data)
            return{"success":True}
        else:
            return{"success":False, "msg":"only admin can perform this action"}




api.add_resource(Sarpras,"/API/sarpras/<ruangan_id>")

class SarprasDetail(Resource):
    def get(self, sarpras_id):
        ObjInstance = ObjectId(sarpras_id)
        filter = {"_id":ObjInstance}
        data = get_sarpras(filter)
        return json.loads(dumps(data))

    @jwt_required()
    def put(self, sarpras_id):
        user = get_jwt_identity()
        userDetail = get_user({"username":user})
        if userDetail['is_admin']:
            ObjInstance = ObjectId(sarpras_id)
            filter = {"_id":ObjInstance}
            req = request.form
            newvalues ={"$set":{
                'nama':req.get('nama'),
                'jenis':req.get('jenis'),
                'jumlah':int(req.get('jumlah')),
            }}
            update_sarpras(filter,newvalues)
            return{"success":True}
        else:
            return{"success":False, "msg":"only admin can perform this action"}

    @jwt_required()
    def delete(self, sarpras_id):
        user = get_jwt_identity()
        userDetail = get_user({"username":user})
        if userDetail['is_admin']:
            ObjInstance = ObjectId(sarpras_id)
            filter = {"_id":ObjInstance}
            delete_sarpras(filter)
            return{"success":True}
        else:
            return{"success":False, "msg":"only admin can perform this action"}

api.add_resource(SarprasDetail,"/API/sarpras/<sarpras_id>")
