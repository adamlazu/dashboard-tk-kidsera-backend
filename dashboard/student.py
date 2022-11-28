import json
from bson.json_util import dumps
from flask import Blueprint, request
from .db import insert_student, get_student
from bson.objectid import ObjectId
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required

bp = Blueprint('students',__name__)
api = Api(bp)

class Students(Resource):
    @jwt_required()
    def post(self):
        req = request.form
        data = {
            'nama' : req['nama'],
            'jenis_kelamin' : req['jenis_kelamin'], 
            'nisn' : req['nisn'], 
            'nik' : req['nik'], 
            'no_kk' : req['no_kk'], 
            'tingkat_kelas' : req['tingkat_kelas'], 
            'id_rombongan_belajar' : int(req['id_rombongan_belajar']), 
            'tanggal_masuk' :req['tanggal_masuk'],
            'tanggal_lulus' :req['tanggal_lulus'],
            'nomor_induk' : req['nomor_induk'],
            'status' : req['status'],
            'tinggi_badan' : int(req['tinggi_badan']),
            'berat_badan' : int(req['berat_badan']),
            'lingkar_kepala' : int(req['lingkar_kepala']),
            'alergi' : req['alergi'],
            'nama_ayah' : req['nama_ayah'],
            'nama_ibu' : req['nama_ibu'],
            'pekerjaan_ayah' : req['pekerjaan_ayah'],
            'pekerjaan_ibu' : req['pekerjaan_ibu']
        }
        insert_student(data)
        return {'Success': True}

api.add_resource(Students, '/API/students')

class Student(Resource):
    @jwt_required()
    def get(self, student_id):
        id = student_id
        ObjInstance = ObjectId(id)
        filter = {'_id' : ObjInstance}
        data = get_student(filter)
        return json.loads(dumps(data))

api.add_resource(Student, '/API/students/<student_id>')
