import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    #DB
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'cards.db')
    #Swagger
    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.json'