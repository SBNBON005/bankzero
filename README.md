## Prerequisites
- python 3.8
- Install `Docker`
- Clone and change directory to bankzero `git@github.com:SBNBON005/bankzero.git`

## Setup
Run the command to bring up docker postgres db

```
$ docker run --rm  -p 5432:5432 --name some-postgres -e POSTGRES_PASSWORD=test -e POSTGRES_USER=proxyuser -e POSTGRES_DB=bankzero postgres:alpine
```

Install requirements and building module
```
$ pip install -e .
```

Create tables and an account in the database:

```
$ python3.8 bootstrap.py
```

### Processing transactions from a csv file

```
$ python3.8 bankzero/process_csv_txs.py
```


### Processing transactions from a database table
```
$ python3.8 bankzero/process_pending_txs.py
```

### Generate Report
```
$ python3.8 bankzero/generate_report.py
```
