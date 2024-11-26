from flask import Flask
from flask_security import Security, SQLAlchemyUserDatastore
from flask_cors import CORS
from src.model import db, User, Role
from config import LocalDevelopmentConfig


def createApp():
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)

    # allowing cors 
    CORS(app, origins='http://127.0.0.1:5173')

    db.init_app(app)

    # flask security init
    datastore = SQLAlchemyUserDatastore(db, User, Role)

    app.security = Security(app, datastore=datastore, register_blueprint=False)
    app.app_context().push()


    from src.resources import api

    api.init_app(app)

    return app

app = createApp()

import src.routes
import src.create_initial_data

if (__name__ == "__main__"):
    app.run(debug = True)