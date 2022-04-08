from celery.schedules import crontab

from src.bases.celery.generator import CeleryWorkerGenerator

from config import CeleryConfig

generator = CeleryWorkerGenerator(
    name='CoreEngineScheduler',
    config=CeleryConfig,
)
app = generator.run()

app.conf.beat_schedule = {
    'CurrencyConversionAutoUpdateSchedule': {
        'task': 'CurrencyConversionUpdate',
        'schedule': crontab(hour=0),
        'options': {'queue': 'CommonTasks'}
    }
}
