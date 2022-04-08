from src.bases.celery.task import Task, TaskHandler


class Handler(TaskHandler):
    def run(self):
        raise Exception('ImplementTask')


class CrawlingCurrencyConversions(Task):
    name = 'MyTask'
    handler = Handler
