import requests
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server

from app.app import app, db, controller


migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('runserver', Server(host='0.0.0.0', port=9000))
manager.add_command('db', MigrateCommand)


@manager.command
def create_db():
    db.create_all()


@manager.option('-h', '--host', dest='host', default='0.0.0.0')
@manager.option('-p', '--port', dest='port', type=int, default=9000)
@manager.option('-w', '--workers', dest='workers', type=int, default=2)
def rununicorn(host, port, workers):
    from gunicorn.app.base import Application

    class Flask(Application):
        def __init__(self, **kwargs):
            super(Flask, self).__init__(**kwargs)

        def init(self, parser, opts, args):
            return {
                'bind': '{0}:{1}'.format(host, port),
                'workers': workers
            }

        def load(self):
            return app

    application = Flask()
    return application.run()


@manager.command
def create_fake_users(amount):
    response = requests.get('https://randomuser.me/api/?results={amount}'.format(
        amount=amount
    )).json()
    for user_data in response.get('results'):
        controller.create_user(user_data)
    return 'Created {amount} users'.format(amount=amount)


if __name__ == '__main__':
    manager.run()
