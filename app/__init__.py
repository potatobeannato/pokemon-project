from flask import Flask
from config import Config
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


login = LoginManager()
login.login_view = 'auth.login'

# init the database
db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    # register plugins
    login.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # register our blueprints with the app
    from .blueprints.main import bp as main_bp
    app.register_blueprint(main_bp)

    from .blueprints.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    return app
