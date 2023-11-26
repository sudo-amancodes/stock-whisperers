# import os
from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import Bcrypt
# from flask_login import LoginManager
# from flask_mail import Mail

app = Flask(__name__)
# # # app.config['SECRET_KEY'] = 'potato'
# # # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# # # db = SQLAlchemy(app)
# # # bcrypt = Bcrypt(app)
# # # login_manager = LoginManager(app)
# # # app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
# # # app.config['MAIL_PORT'] = 587
# # # app.config['MAIL_USE_TLS'] = True
# # # app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
# # # app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
# # # mail = Mail(app)