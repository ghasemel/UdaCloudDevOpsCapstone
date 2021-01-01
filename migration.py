import os
import sys

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app, db
from models import Goods

migrate = Migrate(app, db)
manager = Manager(app)

# set up a manager command to initialize a Manager instance for our app
manager.add_command(sys.argv[1], MigrateCommand)


if __name__ == '__main__':
    manager.run()
