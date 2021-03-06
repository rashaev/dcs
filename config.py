import os
basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = '_hardcf7v46hvk037ccjBgd'

SQLALCHEMY_DATABASE_URI = 'postgresql://postgres@10.10.1.15/dcs'
SQLALCHEMY_TRACK_MODIFICATIONS = False

FLASKY_POSTS_PER_PAGE = 25

CELERY_BROKER_URL = 'amqp://dcs:dcs@10.10.1.15:5672/myvhost'
CELERY_RESULT_BACKEND = 'file:///Users/roman/Programming/celery/results'
CELERY_ENABLE_UTC = False
CELERY_TIMEZONE = 'Europe/Moscow'

MAIN_KEYS_DIR = '/Users/roman/Programming/keys-vpn/'
EVC_KEYS_DIR = '/Users/roman/Programming/evc-keys/'