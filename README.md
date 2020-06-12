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
  DATABASE_URL='<database_url>' FLASK_APP='app.webapp' python3 -m flask run --port=<port> --host=<ip_address>

  # example DATABASE_URL='postgresql://tatran:@localhost:5432/dvdrental' FLASK_APP='app.webapp' python3 -m flask run --port=5001 --host=0.0.0.0
```

Goto http://localhost:5001/

## Demo

http://35.215.111.93:5001/
