import os
from flask import *


def create_app():
    app = Flask(__name__,instance_relative_config= True)
    app.config.from_pyfile('settings.cfg',silent=False)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    return app