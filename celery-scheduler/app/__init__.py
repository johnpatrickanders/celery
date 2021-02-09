from os import environ
from flask import Flask
from celery import Celery


app = Flask(__name__)


# Configs
REDIS_HOST = "0.0.0.0"
REDIS_PORT = 6379
BROKER_URL = environ.get('REDIS_URL', "redis://{host}:{port}/0".format(
    host=REDIS_HOST, port=str(REDIS_PORT)))
CELERY_RESULT_BACKEND = BROKER_URL


def make_celery(app):
    # create context tasks in celery
    celery = Celery(
        app.import_name,
        broker=BROKER_URL
    )
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery


celery = make_celery(app)


@app.route('/')
def view():
    return "Hello, Flask is up and running!"


if __name__ == "__main__":
    app.run()
