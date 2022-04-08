from celery import Task as _Task


class TaskHandler(object):
    def __init__(self, session, redis, mongo):
        self.session = session
        self.redis = redis
        self.mongo = mongo

    def run(self, *args, **kwargs):
        raise NotImplementedError


class Task(_Task):
    handler = TaskHandler

    def run(self, *args, **kwargs):
        session = self.app.sql_session_factory()

        handler = self.handler(
            session=session,
            redis=self.app.redis,
            mongo=self.app.mongo
        )
        handler.run(*args, **kwargs)

        session.close()
        self.app.sql_session_factory.remove()
