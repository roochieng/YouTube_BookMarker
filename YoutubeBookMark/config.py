import os
from flask_mysqldb import MySQL
from sqlalchemy import create_engine
from sqlalchemy import URL
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask import Flask, request
from dotenv import load_dotenv
from flask_login import LoginManager



app = Flask(__name__, '/static')

app.secret_key = os.urandom(24)


load_dotenv()

# Access the DATABASE_URL environment variable
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
#migrate = Migrate(app, db)
 