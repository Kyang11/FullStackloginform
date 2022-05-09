from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Initializing plug in



# Register Plug-ins
login = LoginManager()

#init my Database manager
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class = Config):
    #Configure Some Settings

    # Init the app

    app = Flask(__name__)
    app.config.from_object(config_class)

    login.init_app(app)
    db.init_app(app)
    migrate.init_app(app,db)

    # configure some setting
    login.login_view = 'auth.login'
    login.login_message = 'Please login to check out our features '
    login.login_message_category='success'

    from .blueprints.main import bp as main_bp
    app.register_blueprint(main_bp)


    from .blueprints.auth import bp as auth_bp
    app.register_blueprint(auth_bp)



    return app

