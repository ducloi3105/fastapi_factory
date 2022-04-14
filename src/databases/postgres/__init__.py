from sqlalchemy import create_engine, event, inspect
from sqlalchemy.orm import sessionmaker, scoped_session, Session as BaseSession
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from src.bases.model import Query


class CachedEventSession(BaseSession):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, query_cls=Query)
        self._cached_events = []

    def close(self):
        self._cached_events = []
        return super(CachedEventSession, self).close()

    def commit(self):

        action_map = {
            'new': 'create',
            'dirty': 'update',
            'deleted': 'delete'
        }

        for key in action_map:
            objects = getattr(self, key, [])
            for obj in objects:
                if key == 'dirty':
                    state = inspect(obj)

                    has_changes = False

                    for attr in state.attrs:
                        history = attr.load_history()
                        if not history.has_changes():
                            continue
                        has_changes = True
                        break

                else:
                    has_changes = True

                if has_changes:
                    self._cached_events.append(dict(
                        action=action_map[key],
                        obj=obj
                    ))
        return super(CachedEventSession, self).commit()

    @property
    def cached_events(self):
        return self._cached_events


class Postgres(object):
    def __init__(self,
                 uri,
                 pool_size=50,
                 max_overflow=0):
        self.uri = uri

        self.engine = None

        self._setup_engine(
            pool_size=pool_size,
            max_overflow=max_overflow
        )

    def _setup_engine(self, pool_size=50, max_overflow=0):
        self.engine = create_engine(
            self.uri,
            client_encoding='utf8',
            pool_recycle=7200,
            pool_pre_ping=True,
            pool_size=pool_size,
            max_overflow=max_overflow
        )

    def create_session_factory(self,
                               disable_autoflush: bool = False,
                               callback_events: dict = None,
                               ) -> scoped_session:
        params = dict(
            bind=self.engine,
            class_=CachedEventSession
        )
        if disable_autoflush:
            params['autoflush'] = False

        session_factory = sessionmaker(**params)
        session_class = scoped_session(session_factory)

        if callback_events:
            for key, callback_func in callback_events.items():
                event.listen(session_class,
                             key,
                             callback_func)

        return session_class


class PostgresAsync(object):
    def __init__(self,
                 uri,
                 pool_size=50,
                 max_overflow=0):
        self.uri = uri

        self.engine = None

        self._setup_engine(
            pool_size=pool_size,
            max_overflow=max_overflow
        )

    def _setup_engine(self, pool_size=50, max_overflow=0):
        self.engine = create_async_engine(
            self.uri
            # client_encoding='utf8',
            # pool_recycle=7200,
            # pool_pre_ping=True,
            # pool_size=pool_size,
            # max_overflow=max_overflow
        )

    def create_session_factory(self,
                               disable_autoflush: bool = False,
                               callback_events: dict = None,
                               ) -> scoped_session:
        params = dict(
            bind=self.engine,
            class_=AsyncSession
        )
        if disable_autoflush:
            params['autoflush'] = False

        session_factory = sessionmaker(**params)
        session_class = scoped_session(session_factory)

        # if callback_events:
        #     for key, callback_func in callback_events.items():
        #         event.listen(session_class,
        #                      key,
        #                      callback_func)

        return session_class
