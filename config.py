import os
basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = '_hardcf7v46hvk037ccjBgd'
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres@10.10.1.15/dcs'
SQLALCHEMY_TRACK_MODIFICATIONS = False
FLASKY_POSTS_PER_PAGE = 25
CELERY_BROKER_URL = 'amqp://dcs:dcs@10.10.1.15:5672/myvhost'

MAIN_KEYS_DIR = '/Users/roman/Programming/keys-vpn/'