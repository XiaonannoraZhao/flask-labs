from ensurepip import bootstrap
#import imp
from pickle import APPEND
from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap


app = Flask(__name__)

app.config["SECRET_KEY"]='413ce59d52111b1693a15cf2809c8c4e260780d59c788154'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = 'mysql+pymysql://c1894986:Password2022@csmysql.cs.cf.ac.uk:3306/c1894986_my_db' 


db=SQLAlchemy(app)
bootstrap=Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


from flask_app import routes 