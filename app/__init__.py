from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate  

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()  

def create_app():
    from flask import Flask
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)  
    return app