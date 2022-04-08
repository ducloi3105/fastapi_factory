from kombu import Queue

from src.bases.celery.generator import CeleryWorkerGenerator
from src.databases import Postgres, Redis, Mongo

from config import CeleryConfig, REDIS, POSTGRES_URI, MONGO_URI

from . import tasks

redis = Redis(**REDIS)
postgres = Postgres(uri=POSTGRES_URI)
mongo = Mongo(MONGO_URI)
generator = CeleryWorkerGenerator(
    name='MailWorker',
    redis=redis,
    mongo=mongo,
    sql_session_factory=postgres.create_session_factory(),
    config=CeleryConfig,
    task_module=tasks,
    task_queues=(
        Queue('CommonTasks'),
    )
)

worker = generator.run()
