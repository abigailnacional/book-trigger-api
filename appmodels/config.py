import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///login_user_information.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False