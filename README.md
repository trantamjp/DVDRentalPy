# DVDRentalPy

Sample Python

## Preparing database

Download sample data from https://www.postgresqltutorial.com/postgresql-sample-database/

## Installation

```
  git clone https://github.com/trantamjp/DVDRentalPy.git
  cd DVDRentalPy

  python3 -m venv env
  source env/bin/activate
  pip install -r requirements.txt
```

## Run

```
  source env/bin/activate
  DATABASE_URL='<database_url>' FLASK_APP='app.webapp' python3 -m flask run --port=5001

  # example DATABASE_URL='postgresql://tatran:@localhost:5432/dvdrental' FLASK_APP='app.webapp' python3 -m flask run --port=5001
```

Goto http://localhost:5001/

## Demo

http://34.94.42.251:5001/
