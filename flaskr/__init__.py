import os
from flask import Flask

from . import db
from .auth import bp as auth_bp
from .car import bp as car_bp
from dotenv import load_dotenv

def create_app(test_config=None):
    load_dotenv()
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY'),
        DATABASE_URL = os.getenv('DATABASE_URL')
    )

    if app.config["DATABASE_URL"] is None:
        raise RuntimeError("DATABASE_URL is not set")

    if test_config is None:
        app.config.from_pyfile('config.py',silent=True)
    else:
        app.config.from_mapping(test_config)
    
    db.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(car_bp)

    @app.route('/health')
    def health():
        return '<h1>Welcom to car registery</h1>'    
    
    

    return app