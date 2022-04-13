from src.databases import Postgres
from src.bases.api.factory import Factory
from src.api import resources

from config import (POSTGRES_URI, ApiConfig)


class APIFactory(Factory):
    def install_resource(self, app):
        from src.api.resources.health_check.methods import router
        from src.api.resources.test.methods import trouter
        app.include_router(router)
        app.include_router(trouter)


def trigger_auto_sync(session):
    pass


sql_db = Postgres(POSTGRES_URI)
sql_session_factory = sql_db.create_session_factory(
    disable_autoflush=True,
    callback_events={
        'after_commit': trigger_auto_sync
    }
)
# sql_async_session = sql_db.create_async_engine
factory = APIFactory(
    sql_session_factory=sql_session_factory,
    resource_module=resources,
)

app = factory.create_app()
