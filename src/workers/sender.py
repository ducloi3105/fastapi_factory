from src.bases.celery.generator import CeleryWorkerGenerator

from config import CeleryConfig

generator = CeleryWorkerGenerator(
    name='WebmailTaskSender',
    config=CeleryConfig,
)

sender = generator.run()
