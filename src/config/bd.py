from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow 
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234567890'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/banco_alimentos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = "claveSecreta"

db = SQLAlchemy(app)

ma = Marshmallow(app)

CORS(app)
