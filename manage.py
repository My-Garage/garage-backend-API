#!/usr/bin/env python3
import os

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from api.__init__ import app, databases

migrate = Migrate(app, databases)
manager = Manager(app)
manager.add_command('databases', MigrateCommand)


@manager.command
def init_db():
    os.system('createdb washing_db')
    os.system('createdb testing_db')
    print('Databases created')


@manager.command
def drop_db():
    os.system(
        'psql -c "DROP DATABASE IF EXISTS testing_db"')
    os.system(
        'psql -c "DROP DATABASE IF EXISTS washing_db"')
    print('Databases dropped')


if __name__ == '__main__':
    manager.run()
