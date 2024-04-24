
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
server = Flask(__name__)

# Database connection settings
host = 'localhost'
user = 'root'
password = 'password'
database = 'trial_schema'
port = 3306

server.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{user}:{password}@{host}:{port}/{database}'
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(server)
