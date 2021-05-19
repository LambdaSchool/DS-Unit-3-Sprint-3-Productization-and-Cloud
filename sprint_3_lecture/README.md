# twitoff-14
## Installation
TODO: clone the repo
## Usage
```sh
# mac version:
FLASK_APP=twitoff_app flask run
# windows version:
set FLASK_APP=twitoff_app
flask run
```

# database creation
```
# Windows users can omit the "FLASK_APP=twitoff_app" part...

FLASK_APP=twitoff_app flask db init #> generates app/migrations dir

# run both when changing the schema:
FLASK_APP=twitoff_app flask db migrate #> creates the db (with "alembic_version" table)
FLASK_APP=twitoff_app flask db upgrade #> creates the specified tables
```