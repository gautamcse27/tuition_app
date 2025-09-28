import os
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL','postgresql://tuition25:Dtuition@localhost:5432/tuitiondb')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'ff8740764e0833b0b849259bb981b70d9c5da1c8eef39d82'
