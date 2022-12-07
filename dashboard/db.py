import pymongo
import click
from flask import g, current_app
from flask.cli import with_appcontext

def get_db():
    mongocon = current_app.config['MONGO_URI']
    dbclient = pymongo.MongoClient(mongocon)
    g.db = dbclient[current_app.config['DATABASE']]
    return g.db

def get_collection(colname):
    if 'db' not in g:
        get_db()
    return g.db[colname]

# for user
def get_user(filter = {}):
    collection = get_collection('users')
    return collection.find_one(filter)

def delete_user(filter = {}):
    collection = get_collection('users')
    return collection.delete_one(filter)

def insert_user(data):
    collection = get_collection('users')
    row = collection.insert_one(data)
    return row

# for student
def getAll_student(filter = {}):
    collection = get_collection('students')
    return collection.find(filter)

def get_student(filter = {}):
    collection = get_collection('students')
    row = collection.find_one(filter)
    return row

def insert_student(data):
    collection = get_collection('students')
    row = collection.insert_one(data)
    return row

def update_student(filter, newvalues):
    collection = get_collection('students')
    return collection.update_one(filter, newvalues)

def delete_student(filter = {}):
    collection = get_collection('students')
    return collection.delete_one(filter)

# for tendik
def get_tendiks():
    collection = get_collection('tenaga_pendidik')
    return collection.find()

def insert_tendik(data):
    collection = get_collection('tenaga_pendidik')
    row = collection.insert_one(data)
    return row

def get_tendik(filter):
    collection = get_collection('tenaga_pendidik')
    return collection.find_one(filter)

def update_tendik(filter, newvalues):
    collection = get_collection('tenaga_pendidik')
    return collection.update_one(filter, newvalues)

def delete_tendik(data):
    collection = get_collection("tenaga_pendidik")
    collection.delete_one(data)
    
# for rombel
def get_rombels():
    collection = get_collection('rombel')
    return collection.find()

def get_rombel(filter = {}):
    collection = get_collection('rombel')
    row = collection.find_one(filter)
    return row

def update_rombel(filter, new_val):
    collection = get_collection('rombel')
    collection.update_one(filter, new_val)

def insert_rombel(data):
    collection = get_collection('rombel')
    collection.insert_one(data)

#for ruangan
def get_ruangans():
    collection = get_collection('ruangan')
    return collection.find()

def insert_ruangan(data):
    collection = get_collection('ruangan')
    row = collection.insert_one(data)
    return row

def get_ruangan(filter = {}):
    collection = get_collection('ruangan')
    return collection.find_one(filter)

#for sarpras
def get_allsarpras(filter={}):
    collection = get_collection('sarpras')
    return collection.find(filter)

def insert_sarpras(data):
    collection = get_collection('sarpras')
    row = collection.insert_one(data)
    return row

def update_sarpras(filter, newvalues):
    collection = get_collection('sarpras')
    return collection.update_one(filter, newvalues)

def delete_sarpras(filter):
    collection = get_collection("sarpras")
    collection.delete_one(filter)

def get_sarpras(filter):
    collection = get_collection('sarpras')
    return collection.find_one(filter)


# for token
def get_blockedtoken(filter = {}):
    collection = get_collection('token_block_list')
    return collection.find_one(filter)

def block_token(data):
    collection = get_collection('token_block_list')
    row = collection.insert_one(data)
    return row

def close_db(e=None):
    db = g.pop(current_app.config['DATABASE'], None)
    
    if db is not None:
        db.close() 
def init_db():
    """clear the existing data and create new tables."""    
    db = get_db()    
    db.client.drop_database(current_app.config['DATABASE'])
    
@click.command('init-db')
@with_appcontext
def init_db_command():    
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)