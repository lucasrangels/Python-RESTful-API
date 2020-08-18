import os
from src.app import create_app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


app = create_app('development')

migrate = Migrate(app=app, db=db)

manager = Manager(app=app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
  manager.run()