import os

# Use the name of the environment variable, not the actual URL string
uri = os.getenv('DATABASE_URL')

# Fix for Heroku 'postgres://' prefix
if uri and uri.startswith('postgres://'):
    uri = uri.replace('postgres://', 'postgresql://', 1)

SQLALCHEMY_DATABASE_URI = uri
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'ff8740764e0833b0b849259bb981b70d9c5da1c8eef39d82'
