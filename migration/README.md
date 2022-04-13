Generic single-database configuration.


# alembic
- export python path
```
export PYTHONPATH=$PWD
```

- add migration
```
alembic revision --autogenerate -m "<description>"
```
- migration db
```
alembic upgrade head
```
