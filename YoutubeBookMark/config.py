import os
from flask_mysqldb import MySQL
from sqlalchemy import create_engine
from sqlalchemy import URL
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask import Flask
from dotenv import load_dotenv


app = Flask(__name__, '/static')

app.secret_key = os.urandom(24)


load_dotenv()

# Access the DATABASE_URL environment variable
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
# migrate = Migrate(app, db)
 