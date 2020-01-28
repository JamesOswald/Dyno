import os
basedir = os.path.abspath(os.path.dirname(__file__))
from dotenv import load_dotenv
load_dotenv()

class Config(object):
    SEED_DATA_LOCATION = os.environ.get('SEED_DATA_LOCATION') or os.path.join(basedir, 'seed_data.txt')
    SQLALCHEMY_DATABASE_NAME=os.getenv('sequence')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret'