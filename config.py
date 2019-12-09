from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import desc        
from flask_migrate import Migrate 
from flask_bcrypt import Bcrypt


app = Flask(__name__)

app.secret_key = "it's a secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///band_underground.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
migrate= Migrate(app,db)