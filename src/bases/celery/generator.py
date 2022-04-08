import inspect

from celery import Celery as _Celery

from .task import Task


class Celery(_Celery):
    def __init__(self,
                 sql_session_factory=None,
                 redis=None,
                 mongo=None,
                 *args,
                 **kwargs):
        super().__init__(*args, **kwargs)

        self.sql_session_factory = sql_session_factory
        self.redis = redis
        self.mongo = mongo


class CeleryWorkerGenerator(object):
    def __init__(self,
                 name: str,
                 config: object,
                 task_module=None,
                 sql_session_factory=None,
                 redis=None,
                 mongo=None,
                 task_queues=None):
        self.name = name
        self.config = config
        self.sql_session_factory = sql_session_factory
        self.redis = redis
        self.mongo = mongo
        self.task_module = task_module
        self.task_queues = task_queues

    def _register_task(self, worker):
        classes = inspect.getmembers(self.task_module,
                                     inspect.isclass)
        for cls_name, cls in classes:
            if not issubclass(cls, Task):
                continue

            worker.register_task(cls())

    def _declare_queues(self, worker):
        worker.conf.task_queues = self.task_queues

    def run(self) -> Celery:
        worker = Celery(main=self.name,
                        redis=self.redis,
                        mongo=self.mongo,
                        sql_session_factory=self.sql_session_factory)

        worker.config_from_object(self.config)

        if self.task_module:
            self._register_task(worker)

        if self.task_queues:
            self._declare_queues(worker)

        return worker
