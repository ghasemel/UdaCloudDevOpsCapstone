import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from models import app, db, Goods

# add models here
# from models import Goods

migrate = Migrate(app, db)
manager = Manager(app)

# set up a manager command to initialize a Manager instance for our app
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
