from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

from app.routes import main, auth, member, admin
app.register_blueprint(main.bp)
app.register_blueprint(auth.bp)
app.register_blueprint(member.bp)
app.register_blueprint(admin.bp)

if __name__ == '__main__':
    app.run(debug=True)
