# App configuration file
from datetime import timedelta

SECRET_KEY = '820b4ad02742e6630b554a48de7d2d9f'
CSRF_ENABLED = True
STATIC_FOLDER = 'static'

JWT_SECRET_KEY = '820b4ad02742e6630b554a48de7d2d9f'
# Jonny
JWT_EXPIRES = timedelta(hours=24)
JWT_IDENTITY_CLAIM = 'user'
JWT_HEADER_NAME = 'authorization'

