from flask import Flask
from flask_spp.config import DevelopmentConfig
from flask_session import Session


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    Session(app)

    ctx = app.app_context()
    ctx.push()

    from flask_spp.routes.index_bp import index
    from flask_spp.routes.users_bp import users
    from flask_spp.routes.services_bp import services

    app.register_blueprint(index)
    app.register_blueprint(users)
    app.register_blueprint(services)

    return app
