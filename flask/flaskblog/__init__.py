from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import secrets

app = Flask(__name__)  # __name__ is special variable of python, name of the module
app.config['SECRET_KEY'] = secrets.token_hex(16)  # secret key for our application
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/flaskblog'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

login_manager.login_view = 'login'
# if user is not loged in and if login require comes in picture then login manager will redirect to login method of
# routes
login_manager.login_message_category = 'info'  # beautifies the message generated by above code
app.config['MAIL_SERVER']='smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '69ff35d8dbdbbe'
app.config['MAIL_PASSWORD'] = 'c7912165915eb5'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

from flaskblog import routes