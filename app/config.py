import os
from dotenv import load_dotenv


os.environ.pop('SQLALCHEMY_DATABASE_URI', None)
os.environ.pop('JWT_SECRET_KEY', None)

load_dotenv()
class Config:
    SQLALCHEMY_DATABASE_URI=os.environ.get('SQLALCHEMY_DATABASE_URI')
    JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES=1800