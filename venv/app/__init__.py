from flask import Flask 
# from config import Config
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
from flask_googlecharts import GoogleCharts,LineChart


app=Flask(__name__)
app.secret_key = "shivani18ME1A0562"
# app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:shivi562@localhost/expenditure"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db=SQLAlchemy(app)
migrate=Migrate(app,db)
login = LoginManager(app)
login.login_view = 'login'
charts = GoogleCharts(app)






from app import routes,models
