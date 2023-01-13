<div align="center">
  <h1 align="center">Test Project</h1>
</div>

<summary id="navigation">Table of Contents</summary>
<ol>
<li>
    <a href="#about-the-project">About The Project</a>
    <ul>
    <li><a href="#built-with">Built With</a></li>
    <li><a href="#description">Description</a></li>
    </ul>
</li>
<li><a href="#quick-start">Quick start</a></li>
<li><a href="#specifications">Specifications</a>
    <ul>
    <li><a href="#code-style">Code style</a></li>
    <li><a href="#project-structure">Project structure</a></li>
    </ul>
</li>
<li>
    <a href="#how-to">How to</a>
    <ul>
    <li><a href="#env-variables">Env variables</a></li>
    <li><a href="#database">Database</a></li>
    <li><a href="#deploy">Deploy</a></li>
    <li><a href="#use-alembic">Use alembic</a></li>
    </ul>
</li>
</ol>

<div id="about-the-project"></div>

## About The Project

### Description

<div id="description"></div>
This is test project with auth and post crud

### Built with

<div id="built-with"></div>
Main stack:

* [Python 3.10](https://www.python.org/downloads/release/python-3106/)
* [Gunicorn with Uvicorn](https://fastapi.tiangolo.com/deployment/server-workers/)
* [Fastapi](https://fastapi.tiangolo.com/)
* [SQLAlchemy](https://www.sqlalchemy.org/)
* [Alembic](https://alembic.sqlalchemy.org/en/latest/)
* [PostgreSQL](https://www.postgresql.org/)
* [Docker + Docker Compose](https://www.docker.com/)

## Quick start

<div id="quick-start"></div>

### Windows/Ubuntu

1. Copy the contents of the .env.example file to the .env file in the root folder of the repository.
2. We specify the value of the BACKEND_PORT variable in the .env file at our discretion, for example 8001
3. Run the command from the root folder of the repository:
    ```shell
    docker-compose up -d
    ```

## Specifications

<div id="specifications"></div>

### Code style

<div id="code-style"></div>

The project code is written in accordance with PEP8.
In the future you can add pre-commit hooks

### Project structure

<div id="project-structure"></div>

The root directory contains all the files necessary for the configuration and assembly of the project:

* `.env` - Contains environment variables that are required for the application to work. The file is not stored in GIT.
* `.env.example` - Contains default example of variables that should be in .env
* `alembic.ini` - Configuration needed for Alembic to work
* `docker-compose.yml` - Configuration for building and running the application with one command
* `Dockerfile` - Docker configuration to specify project build steps
* `entrypoint.sh` - Script that is run when the application starts via docker-compose. Waiting for DB to start and
  applying migrations

The `alembic` directory contains migrations and configuration files

* `versions/` - Directory where all applied database migrations are saved
* `env.py` - Standard Alembic file that does all migrations under the hood
* `README` - Documentation file for migrations in the project
* `script.py.mako` - Alembic configuration file

The application itself is located in the `app` directory

* `constants/` - Contains values to populate database lookup tables
* `core/` - Contains tools that are used throughout the project (Env variables, Security config).
* `crud/` - Base class and classes inherited from it for CRUD operations on database models.
* `db/` - Database base class configuration, database session initialization, etc.
* `enums/` - Contains classes for convenient getting entities from database lookup tables.
* `models/` - DB table models, each model in a separate file.
* `routes/` - Methods that will hang out in the API
* `schemas/` - Schemas for working with DB and API models, each schema is in a separate file.
* `services/` - Helper classes containing business logic
* `dependencies/` - Methods that are used as dependencies for routes
* `main.py` - The entry point for the application
* `initial_data.py` - Initialize the database with primary data

## How to

<div id="how-to"></div>

### Env variables

<div id="env-variables"></div>

To work, you need to create an .env file and fill in the values for the following variables:
Also you need to add the following variables into `./app/config.Settings`

*APP_PORT* - port for your application, ex: 8001
*POSTGRES_DATA* – path to the database data folder relative to the repository folder, example: **./data/postgres**
*POSTGRES_HOST* – base address, example: **127.0.0.1**
*POSTGRES_PORT* – port, example: **15432**
*POSTGRES_USER* is the user in the database, almost always: **postgres**
*POSTGRES_PASSWORD* – user password, example: **postgres**
*POSTGRES_DB* – database name: **test**
*SECRET_KEY* - secret key for generating jwt, example: *qawsedfrgtyhujikolpzsxdcfvghbnjkm*
*ALGORITHM* - algorithm for generating jwt, example **HS256**
*ACCESS_TOKEN_EXPIRE_MINUTES* - expire time for jwt, in minutes, ex: **30**

### Database

<div id="database"></div>

The database can be configured in several ways:

1. Connecting to a remote postgres database
2. Connecting to the local postgres service
3. Connecting to a locally running docker container with postgres

**Remote connection to postgres**

You must specify the host address, port, login, password and database name in the appropriate environment variables, for
example:

```
POSTGRES_HOST=xx.xx.xx.xx
POSTGRES_PORT=yyyy
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=test
```

**Connecting to local postgres**

If postgres is installed locally and running, then the connection is performed in the same way as a remote connection,
as a rule, the following variables are specified in the .env file:

```
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=test
```

If the priority2030 database has not yet been created, then see the paragraph on creating the priority2030 database

**Connect to local postgres via docker-compose**

To raise the base in docker-compose, it is enough to specify only the following variables:

```
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=tets
```

All parameters, except for the name of the base, can be changed arbitrarily.
Then from the root folder of the repository run the command:

```shell
docker-compose up db
```

How to run migrations:
<div id="migrations"></div>

```shell
pip install alembic;
alembic upgrade head;
```

<div align="right">
<a href="#navigation">To the menu</a>
</div>

### Deploy

<div id="deploy"></div>

Before deployment, you need to run <a href="#database">database</a>, run [migrations](#migrations) and fill the file
with environment variables according to <a href="#env-variables">points above</a>.

**Run without docker-compose**

```shell
pip install -r requirements.txt
uvicorn main:app --port 8001 --host 0.0.0.0
```

**Run via docker-compose**

In this configuration, the backend running in docker only works with the base in the same docker. Accordingly, to run
through docker, you must specify in the .env file:

```
POSTGRES_HOST=db
```

And run the command:

```shell
docker-compose-up
```

<div id="use-alembic"></div>

### Use alembic

1. To create a new migration, you need to run the command:

```shell
alembic revision --autogenerate -m "message"
```

2. To apply the migration, you need to run the command:

```shell
alembic upgrade head
```

3. To roll back the migration, you need to run the command:

```shell
alembic downgrade <migration_name>
```

4. Rollback all migrations, run the command:

```shell
alembic downgrade base
```

<div align="right">
<a href="#navigation">To the menu</a>
</div>
