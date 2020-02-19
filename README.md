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


## Approach
- Have 3 tables Transaction, TransactionAudit and Account (defined in model.py)
- Transaction tbl should have a status column to indicate if it has been processed or not
- Store transaction in TransactionAudit once processed and mark it as processed