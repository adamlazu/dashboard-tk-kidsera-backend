import json
from bson.json_util import dumps
from flask import Blueprint, request
from flask_restful import Api, Resource
from flask_jwt_extended import *
from bson.objectid import ObjectId
from .db import *

bp = Blueprint('rombel', __name__)
api = Api(bp)

class Rombel(Resource):
    @jwt_required()
    def get(self, rombel_id):
        id = ObjectId(rombel_id)
        rombel = get_rombel(id)

        tahun_ajaran = rombel['tahun_ajaran']
        kelas = rombel['kelas']
        ruangan = rombel['ruangan']

        filter_siswa = {"tahun_ajaran" : tahun_ajaran, "tingkat_kelas" : kelas}
        filter_tendik = {"tahun_ajaran" : tahun_ajaran, "kelas_mengajar" : kelas}

        list_siswa = json.loads(dumps(getAll_student(filter_siswa)))
        wali_kelas = json.loads(dumps(get_tendik(filter_tendik)))

        data = {"list_siswa" : list_siswa, "wali_kelas" : wali_kelas, "ruangan" : ruangan}
        return data

    @jwt_required()
    def put(self, rombel_id):
        email = get_jwt_identity()
        userDetail = get_user({"email":email})
        if userDetail['is_admin']:
            id = ObjectId(rombel_id)
            filter = {"_id":id}

            if get_rombel(filter) is None: 
                return {"Success" : False, "msg" : "Id not valid"}
            else:
                req = request.form
                new_val = {
                    "$set":{
                        "tahun_ajaran" : req['tahun_ajaran'],
                        "kelas" : req['kelas'],
                        "ruangan" : req['ruangan'],
                    }
                }
                update_rombel(filter, new_val)
                return {"Success" : True, "msg" : "Data has been updated"}
        else:
            return {"Success" : False, "msg" : "Only admin can perform this action"}

api.add_resource(Rombel, "/API/rombel/<rombel_id>")

class Rombels(Resource):
    @jwt_required()
    def post(self):
        email = get_jwt_identity()
        userDetail = get_user({"email":email})
        if userDetail['is_admin']:
            req = request.form
            data = {
                "tahun_ajaran" : req['tahun_ajaran'],
                "kelas" : req['kelas'],
                "ruangan" : req['ruangan']
            }
            insert_rombel(data)
            return {"Success" : True, "msg" : "New rombel successfully added"}
        else:
            return {"Success" : False, "msg" : "Only admin can perform this action"}

api.add_resource(Rombels, "/API/rombel")