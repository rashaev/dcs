import os
basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = '_hardcf7v46hvk037ccjBgd'
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres@192.168.10.99/dcs'
SQLALCHEMY_TRACK_MODIFICATIONS = False
FLASKY_POSTS_PER_PAGE = 25
CELERY_BROKER_URL = 'amqp://dcs:dcs@192.168.10.99:5672/myvhost'

MAIN_KEYS_DIR = '/Users/roman/Programming/keys-vpn/'