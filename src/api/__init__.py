from api.v1.washing import *
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

from instance.config import application_configuration

app = Flask(__name__)


def EnvironmentName(environment):
    app.config.from_object(application_configuration[environment])


EnvironmentName('DevelopmentEnvironment')
databases = SQLAlchemy(app)