import os
from flask import *
from . import db


def create_app():
    app = Flask(__name__,instance_relative_config= True)
    app.config.from_pyfile('settings.cfg',silent=False)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    db.init_app(app)

    
    return app