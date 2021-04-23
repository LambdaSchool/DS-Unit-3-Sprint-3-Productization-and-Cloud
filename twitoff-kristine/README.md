# twitoff-kristine

## Installation

```sh
git clone https://github.com/KristineYW/twitoff-kristine.git
cd twitoff-kristine/
```

## Setup

Setup and activate virtual encvironment:

```sh
pipenv install
pipenv shell
```

Setup the database:

```sh
# Windows users can omit the "FLASK_APP=web_app" part...

FLASK_APP=web_app flask db init #> generates app/migrations dir

# run both when changing the schema:
FLASK_APP=web_app flask db migrate #> creates the db (with "alembic_version" table)
FLASK_APP=web_app flask db upgrade #> creates the specified tables
```

## Usage

Run the web app:

```sh
FLASK_APP=web_app flask run
```

