
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# use Flask as a server to connect to MySQL database
server = Flask(__name__)

# Database connection settings
host = 'db'
user = 'root'
password = 'password'
database = 'team21_v1'
port=3306
host = 'db'

# database URI
server.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{user}:{password}@{host}:{port}/{database}'
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# database
db = SQLAlchemy(server)
