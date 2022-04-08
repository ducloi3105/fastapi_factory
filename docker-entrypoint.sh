#!/bin/bash

PYTHONPATH=.

poetry run alembic upgrade head

exec $@


