from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Initializing 
app = Flask(__name__)
app.config.from_object(Config)

# Register Plug-ins
login = LoginManager(app)

#init my Database manager
db = SQLAlchemy(app)
migrate = Migrate(app, db)


#Configure Some Settings
login.login_view = 'login'
login.login_message = 'Please login to check out our features '
login.login_message_category='success'


# import routes to initialized routes app#
from app import routes, models