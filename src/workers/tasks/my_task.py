from src.bases.celery.task import Task, TaskHandler


class Handler(TaskHandler):
    def run(self):
        raise Exception('ImplementTask')


class MyTask(Task):
    name = 'MyTask'
    handler = Handler
