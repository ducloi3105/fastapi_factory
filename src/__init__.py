import click
import sys
import uvicorn

from config import POSTGRES_URI, MONGO_URI, REDIS, ENVIRONMENT, POSTGRES_ASYNC_URI

from src.common.logging import log, ContextFilter


def execute_command(command):
    import subprocess
    return subprocess.check_call(command)


@click.group()
def cli():
    pass


@cli.command(short_help='Runs a shell in the app context.')
@click.argument('ipython_args', nargs=-1, type=click.UNPROCESSED)
def shell(ipython_args):
    import sys
    import IPython
    from IPython.terminal.ipapp import load_default_config

    from src.databases import Postgres, Redis, PostgresAsync
    # from src.databases import Postgres, Mongo, Redis

    ip_config = load_default_config()

    postgres_db = Postgres(POSTGRES_URI)

    session_factory = postgres_db.create_session_factory(
        disable_autoflush=True)
    session = session_factory()

    sql_async_db = PostgresAsync(POSTGRES_ASYNC_URI)
    sql_async_session_factory = sql_async_db.create_session_factory(
        disable_autoflush=True
    )
    async_session = sql_async_session_factory()
    ctx = dict(
        session=session,
        async_session=async_session,
        # mongo=Mongo(MONGO_URI),
        reids=Redis(**REDIS, db=0)
    )

    banner = 'Python %s on %s\n' % (sys.version, sys.platform)
    if ctx:
        banner += 'Objects created:'
    for k, v in ctx.items():
        banner += '\n    {0}: {1}'.format(k, v)
    ip_config.TerminalInteractiveShell.banner1 = banner
    IPython.start_ipython(argv=ipython_args, user_ns=ctx, config=ip_config)


@cli.command(short_help='Run an api.')
@click.option('--host', default='127.0.0.1')
@click.option('--port', default='5000')
@click.option('--log_level', default='info')
@click.option('--workers', default='1')
@click.option('--reload', default='1')
@click.option('--buffer-size', default='65535')
@click.option('--host')
def api(**kwargs):
    from src.api.base import app

    host = kwargs.get('host')
    try:
        port = int(kwargs['port'])
    except Exception as e:
        raise e

    log_level = kwargs.get('log_level')
    debug = False
    if log_level == 'info':
        debug = True

    params = dict(
        port=port,
        workers=int(kwargs.get('workers')),
        log_level=log_level,
        debug=debug,
        reload=True
    )
    if host:
        params['host'] = host

    return uvicorn.run(
        'src.api.base:app', **params

    )


@cli.command(short_help='Run celery')
@click.option('--concurrency', default=50)
@click.option('--queue', default='CommonTasks')
@click.option('--pool', default='eventlet')
@click.option('--loglevel')
def celery(**kwargs):

    loglevel = kwargs.get('loglevel')
    if not loglevel:
        loglevel = 'info' if ENVIRONMENT == 'production' else 'debug'
    concurrency = int(kwargs.get('concurrency'))
    queue = kwargs.get('queue')
    pool = kwargs.get('pool')

    return execute_command([
        'celery',
        '-A',
        'src.workers.__init__:worker',
        'worker',
        f'--loglevel={loglevel}',
        f'--queues={queue}',
        f'--concurrency={concurrency}',
        f'--pool={pool}',
    ])
