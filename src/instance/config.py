import os


def db(current=None):
    if current is None:
        current = 'sqlite'

    dbase = {
        "sqlite": {
            'test': 'sqlite:///testing_db',
            'develop': 'sqlite:///washing_db'
        },

        "postgres": {
            'test': 'postgresql://@localhost/testing_db',
            'develop': 'sqlite:///washing_db'
        }

    }
    return dbase[current]


class MainConfiguration(object):
    DEBUG = False
    WTF_CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)


class TestingEnvironment(MainConfiguration):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = db()['test']


class DevelopmentEnvironment(MainConfiguration):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = db()['develop']


class ProductionEnvironment(MainConfiguration):
    DEBUG = False
    TESTING = False


# Dictionary with keys mapping to the different configuration environments
application_configuration = {
    'MainConfiguration': MainConfiguration,
    'TestingEnvironment': TestingEnvironment,
    'DevelopmentEnvironment': DevelopmentEnvironment,
    'ProductionEnvironment': ProductionEnvironment
}
