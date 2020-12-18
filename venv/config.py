import os
basedir=os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY=os.environ.get('SECRET_KEY') or 'no!!! not allowed'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or "postgresql://postgres:shivi562@localhost/expenditure" 
    SQLALCHEMY_TRACK_MODIFICATIONS=False