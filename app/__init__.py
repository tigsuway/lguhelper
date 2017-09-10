from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)
app.config.from_object('config')
app.secret_key = 'S0l3mry$'
db = SQLAlchemy(app)
CSRFProtect(app)

from app import views
from app import models

