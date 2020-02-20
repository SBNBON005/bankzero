## Prerequisites
- python 3.8
- Install `Docker`
- Clone and change directory to bankzero `git@github.com:SBNBON005/bankzero.git`

## Functionality
- Processing transactions from a csv file
- Processing unprocessed transactions in the transaction tbl
- Generate a csv report of processed transactions

There's 3 separate scripts for each functionality

## Setup
Run the command to bring up docker postgres db

```
$ docker run --rm  -p 5432:5432 --name some-postgres -e POSTGRES_PASSWORD=test -e POSTGRES_USER=proxyuser -e POSTGRES_DB=bankzero postgres:alpine
```

Install requirements and building module
```
$ pip install -e .
```

Create and initialize tables:

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

## How to interact with the database

Run docker ps on your terminal to get the container id for your postgres db container.
My output
```
$ docker ps
CONTAINER ID        IMAGE                         COMMAND                  CREATED             STATUS              PORTS                               NAMES
7feb3a98cbc9        postgres:alpine               "docker-entrypoint.s…"   7 seconds ago       Up 6 seconds        0.0.0.0:5432->5432/tcp              some-postgres
```

Jump into the container
```
$ docker exec -it 7feb3a98cbc9 bash
bash-5.0#
```

Login to Database
```
bash-5.0# psql -U proxyuser -d bankzero
psql (12.1)
Type "help" for help.

bankzero=#
```

Running a sql query
```
bankzero=# select * from transaction;
 id |     created_at      |         updated_at         |  description   |   type    |  status   |          amount           | account_id
----+---------------------+----------------------------+----------------+-----------+-----------+---------------------------+-------------
  1 | 2020-01-02 10:00:00 | 2020-01-02 10:00:00        | transafer      | DEPOSIT   | PENDING   | 100000.000000000000000000 | 11111111111
  2 | 2020-01-02 10:01:00 | 2020-01-02 10:01:00        | Computer Mania | PURCHASE  | PENDING   |     10.430000000000000000 | 11111111111
  3 | 2020-01-02 10:01:00 | 2020-01-02 10:01:00        | Computer Mania | DRAW_CASH | PENDING   |     20.000000000000000000 | 11111111111
  4 | 2020-01-02 10:01:00 | 2020-01-02 10:01:00        | Computer Mania | PURCHASE  | PENDING   |     20.000000000000000000 | 11111111111
  5 | 2020-01-02 10:00:00 | 2020-02-20 10:38:27.948621 | transafer      | DEPOSIT   | PROCESSED | 100000.000000000000000000 | 11111111111
  6 | 2020-01-02 10:01:00 | 2020-02-20 10:38:27.970594 | Computer Mania | PURCHASE  | PROCESSED |     10.430000000000000000 | 11111111111
  7 | 2020-01-02 10:01:00 | 2020-02-20 10:38:27.993417 | Computer Mania | DRAW_CASH | PROCESSED |     20.000000000000000000 | 11111111111
  8 | 2020-01-02 10:01:00 | 2020-02-20 10:38:28.01382  | Computer Mania | PURCHASE  | PROCESSED |     20.000000000000000000 | 11111111111
(8 rows)

bankzero=#
```



## Approach
- Have 3 tables Transaction, TransactionAudit and Account (defined in model.py)
- Transaction tbl should have a status column to indicate if it has been processed or not
- Store transaction in TransactionAudit once processed and mark it as processed
- Commit after successfully processing a transaction or rollback