from bankzero.models import Transaction, TransactionAudit, TransactionStatus
from bankzero.utils import db_session
from bankzero.controller import process_tx, generate_report

#  This script process pending transactions in the transaction table


def process_pending_txs():
    with db_session() as session:
        txs = session.query(Transaction).filter(Transaction.status == TransactionStatus.PENDING).all()
        if txs:
            for tx in txs:
                process_tx(session, tx.id, tx.account.id, tx.type.name, tx.amount)
                tx.status = TransactionStatus.PROCESSED


if __name__ == "__main__":
    process_pending_txs()
