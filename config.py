import os

uri = os.getenv('postgres://udckrcs745a6dk:p695bd087556dd6d38ff2bd6e7bd1eb087732a6049f74f31d22e9033d1458a9af@c7itisjfjj8ril.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d6ciuah5gg7vj3', 'postgresql://tuition25:Dtuition@localhost:5432/tuitiondb')

# Fix for Heroku deprecated 'postgres://' prefix
if uri.startswith('postgres://'):
    uri = uri.replace('postgres://', 'postgresql://', 1)

SQLALCHEMY_DATABASE_URI = uri
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'ff8740764e0833b0b849259bb981b70d9c5da1c8eef39d82'
