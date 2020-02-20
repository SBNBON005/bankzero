import csv
from decimal import Decimal
from datetime import datetime

from bankzero.models import Transaction, TransactionAudit, TransactionStatus
from bankzero.models import Account
from bankzero.utils import db_session


def update_account_balance(session, account_id, tx_type, amount):
    account = session.query(Account).filter(Account.id == account_id).first()
    if account:
        if tx_type in ["DEPOSIT", "REFUND"]:
            account.balance = Account.balance + Decimal(amount)
        elif tx_type in ["PURCHASE", "DRAW_CASH"]:
            account.balance = Account.balance - Decimal(amount)


def process_tx(session, tx_id, account_id, tx_type, amount):
    account = session.query(Account).filter(Account.id == account_id).first()
    account_balance_before = account.balance

    tx = session.query(Transaction).filter(Transaction.id == tx_id).first()
    update_account_balance(session, account_id, tx_type, amount)
    tx.status = TransactionStatus.PROCESSED
    session.flush()
    account_balance_after = tx.account.balance

    # Audit
    session.add(TransactionAudit(
        transaction_id=tx_id,
        account_balances={"before": str(account_balance_before), "after": str(account_balance_after)}
    ))


def add_account_balance_to_report(file_writer, accounts):
    file_writer.writerow(['Account ID', 'Closing Balance'])
    for account in accounts:
        file_writer.writerow([account.id, account.balance])


def add_txs_to_report(file_writer, txs):
    file_writer.writerow([f"Total Processed Txs: {len(txs)}"])

    file_writer.writerow(['Account ID', 'Transaction Type', 'Transaction Amount',
                          'Account Balance Before', 'Account Balance After'])

    for c, tx in enumerate(txs):
        file_writer.writerow([tx.transaction.account.id,
                              tx.transaction.type.name,
                              tx.transaction.amount,
                              tx.account_balances['before'],
                              tx.account_balances['after']])


def generate_report():
    with db_session() as session:
        file_name = f'tx_report_{str(datetime.now()).replace(" ", "_").replace(":", "_")}.csv'
        with open(file_name, mode='w') as file:
            file_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            accounts = session.query(Account).all()
            if accounts:
                add_account_balance_to_report(file_writer, accounts)

            txs = session.query(TransactionAudit).all()
            if txs:
                file_writer.writerow([])
                add_txs_to_report(file_writer, txs)
