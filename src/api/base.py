from src.databases import PostgresAsync, Postgres
from src.bases.api.factory import Factory
from src.api import resources

from config import (POSTGRES_URI, ApiConfig, POSTGRES_ASYNC_URI)


def trigger_auto_sync(session):
    pass

sql_db = Postgres(POSTGRES_URI)
sql_session_factory = sql_db.create_session_factory(
    disable_autoflush=True,
    callback_events={
        'after_commit': trigger_auto_sync
    }
)
sql_async_db = PostgresAsync(POSTGRES_ASYNC_URI)
sql_async_session_factory = sql_async_db.create_session_factory(
    disable_autoflush=True,
    callback_events={
        'after_commit': trigger_auto_sync
    }
)
factory = Factory(
    sql_session_factory=sql_session_factory,
    sql_async_session_factory=sql_async_session_factory,
    resource_module=resources,
)

app = factory.create_app(config=ApiConfig)
