from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
#from flask_user import  UserManager

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Пожалуйста авторизуйтесь"


from webapp import views, models
from webapp.models import User
#user_manager = UserManager(app, db, User)

#db.create_all()

