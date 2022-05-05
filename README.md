WEBMAIL

## Setup
# install python 3.8.10
- using pyenv: install pyenv
``` 
eval "$(pyenv init --path)"
pyenv install 3.10.0
pyenv global 3.10.0
```
- install dependencies
```
poetry install
```

# PSQL
- Usually you can run the following command to enter into psql:

 ```psql DBNAME USERNAME```
- For example, psql template1 postgres

One situation you might have is: suppose you login as root, and you don't remember the database name. You can just enter first into Psql by running:

sudo -u postgres psql
In some systems, sudo command is not available, you can instead run either command below:

psql -U postgres
psql --username=postgres
2. Show tables

Now in Psql you could run commands such as:

```
\? list all the commands
\l list databases
\conninfo display information about current connection
\c [DBNAME] connect to new database, e.g., \c template1
\dt list tables of the public schema
\dt <schema-name>.* list tables of certain schema, e.g., \dt public.*
\dt *.* list tables of all schemas

Then you can run SQL statements, e.g., SELECT * FROM my_table;(Note: a statement must be terminated with semicolon ;)
\q quit psql

```

set password
```
ALTER USER user_name WITH PASSWORD 'new_password';

```

add index jsonb
```
create index messages_folder_id on thread (
    (CAST((messages -> 'folder') AS TEXT)),
    (CAST((messages -> 'id') AS TEXT))
)
```
