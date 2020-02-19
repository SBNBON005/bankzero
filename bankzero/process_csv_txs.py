import csv

from bankzero.models import Transaction, TransactionAudit, TransactionStatus
from bankzero.utils import db_session
from bankzero.controller import process_tx, generate_report


#  This script process transaction given through a csv file then generates a csv report


def process_csv_file():
    with open("transactions.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for count, row in enumerate(csv_reader):
            # skip headers
            if count == 0:
                continue

            account_id = row[0]
            created_at = row[1]
            tx_type = row[2]
            description = row[3]
            amount = row[4]
            with db_session() as session:

                if tx_type == "DRAW_AND_PURCHASE":
                    for tx_type in ["DRAW_CASH", "PURCHASE"]:
                        tx = Transaction(account_id=account_id,
                                         created_at=created_at,
                                         type=tx_type,
                                         description=description,
                                         amount=amount,
                                         status=TransactionStatus.PENDING)
                        session.add(tx)
                        session.flush()
                        tx_id = tx.id
                        process_tx(session, tx_id, account_id, tx_type, amount)
                else:
                    tx = Transaction(account_id=account_id,
                                     created_at=created_at,
                                     type=tx_type,
                                     description=description,
                                     amount=amount,
                                     status=TransactionStatus.PENDING)
                    session.add(tx)
                    session.flush()
                    process_tx(session, tx.id, account_id, tx_type, amount)


if __name__ == "__main__":
    process_csv_file()
    generate_report()
