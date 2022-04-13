import logging
import click
import sys
import uvicorn

from config import POSTGRES_URI, MONGO_URI, REDIS, ENVIRONMENT

from src.common.utils import log


def execute_command(command):
    import subprocess
    return subprocess.check_call(command)


def setup_logging():
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(logging.Formatter(
        "%(asctime)s --  %(levelname)s  -- %(message)s")
    )
    log.setLevel(logging.INFO)
    log.addHandler(ch)


@click.group()
def cli():
    pass


@cli.command(short_help='Runs a shell in the app context.')
@click.argument('ipython_args', nargs=-1, type=click.UNPROCESSED)
def shell(ipython_args):
    import sys
    import IPython
    from IPython.terminal.ipapp import load_default_config

    from src.databases import Postgres, Mongo, Redis

    setup_logging()

    ip_config = load_default_config()

    postgres_db = Postgres(POSTGRES_URI)

    session_factory = postgres_db.create_session_factory(
        disable_autoflush=True)
    session = session_factory()

    ctx = dict(
        session=session,
        session_factory=session_factory,
        mongo=Mongo(MONGO_URI),
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
@click.option('--port', default='5000')
@click.option('--log_level', default='info')
@click.option('--workers', default='1')
@click.option('--reload', default='1')
@click.option('--buffer-size', default='65535')
@click.option('--host')
def api(**kwargs):
    from src.api.base import app

    setup_logging()

    host = kwargs.get('host')
    try:
        port = int(kwargs['port'])
    except Exception as e:
        raise e

    params = dict(port=port, debug=True)
    if host:
        params['host'] = host
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

#
# @cli.command(short_help='Run a cron job.')
# @click.argument('job_name')
# @click.option('--interval')
# def cronjob(job_name, **kwargs):
#     from src.cronjobs import JOBS
#     from src.databases import Redis, Mongo
#
#     setup_logging()
#
#     redis = Redis(**REDIS)
#     mongo = Mongo(MONGO_URI)
#     try:
#         job_class = JOBS[job_name]
#     except KeyError:
#         raise Exception('Job %s not found.' % job_name)
#
#     log.info('Running %s job ...' % job_name)
#
#     interval = kwargs.get('interval')
#
#     init_params = dict(
#         mongo_db=mongo.get_db(), redis=redis
#     )
#     if interval:
#         init_params['interval'] = interval
#
#     job_handler = job_class(**init_params)
#     job_handler.run()

#
# @cli.command(short_help='db initialization')
# def init_db():
#     from src.services.database import DatabaseService
#     from src.databases import Redis, Mongo
#
#     setup_logging()
#
#     mongo = Mongo(MONGO_URI)
#     mongo_db = mongo.get_db()
#     db_service = DatabaseService(mongo_db=mongo_db)
#     db_service.init_db()
