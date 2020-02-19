from bankzero.models import Account
from bankzero.utils import db_session, create_tables
from sqlalchemy import sql


def create_accounts(accounts):
    for account in accounts:
        with db_session() as session:
            session.add(Account(id=account['id'], name=account['name']))


def init_tbls():
    accounts = [{"id": "11111111111", "name": "Daily"}]
    create_accounts(accounts)

    with db_session() as db:
        t = sql.text(
            """
                 insert into "transaction"("created_at","updated_at","description","type","status","amount", "account_id")
                values
                ('2020-01-02 10:00:00','2020-01-02 10:00:00','transafer','DEPOSIT', 'PENDING', '100000', '11111111111'),
                ('2020-01-02 10:01:00','2020-01-02 10:01:00','Computer Mania','PURCHASE', 'PENDING', '10.43', '11111111111'),
                ('2020-01-02 10:01:00','2020-01-02 10:01:00','Computer Mania','DRAW_CASH', 'PENDING', '20', '11111111111'),
                ('2020-01-02 10:01:00','2020-01-02 10:01:00','Computer Mania','PURCHASE', 'PENDING', '20', '11111111111');
            """
        )
        db.execute(t)


if __name__ == "__main__":
    create_tables()
    init_tbls()
