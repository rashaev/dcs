import os
basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = '_hardcf7v46hvk037ccjBgd'
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres@192.168.10.99/dcs'
SQLALCHEMY_TRACK_MODIFICATIONS = False