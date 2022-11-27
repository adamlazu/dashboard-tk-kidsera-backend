import os
from flask import *
from . import db
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from datetime import timedelta
from flask_cors import CORS


def create_app():
    app = Flask(__name__,instance_relative_config= True)
    app.config.from_pyfile('settings.cfg',silent=False)
    jwt = JWTManager(app)
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    CORS(app, supports_credentials=True)


    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
        jti = jwt_payload["jti"]
        token = db.get_blockedtoken({'jti':jti})

        return token is not None

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    db.init_app(app)
    
    from . import auth, student
    app.register_blueprint(auth.bp) 
    app.register_blueprint(student.bp) 
    
    return app