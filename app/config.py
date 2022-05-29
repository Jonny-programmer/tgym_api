# App configuration file
from datetime import timedelta

SQLALCHEMY_DATABASE_URI = 'sqlite:///db/reddit_db.db'

SECRET_KEY = '820b4ad02742e6630b554a48de7d2d9f'
CSRF_ENABLED = True
STATIC_FOLDER = 'static'
TEMPLATE_FOLDER = 'templates'
# EXPLAIN_TEMPLATE_LOADING = True

# DEBUG = True

JWT_SECRET_KEY = '820b4ad02742e6630b554a48de7d2d9f'
# Jonny
JWT_EXPIRES = timedelta(hours=10)
JWT_IDENTITY_CLAIM = 'user'
JWT_HEADER_NAME = 'authorization'

