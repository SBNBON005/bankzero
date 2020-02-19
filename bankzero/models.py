from datetime import datetime
from enum import Enum as EnumType, auto

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    Numeric,
    Boolean,
    ForeignKey,
    Enum,
    Index,
    JSON,
)
from sqlalchemy.orm import relationship


DeclarativeBase = declarative_base()


class TransactionType(EnumType):
    DEPOSIT = auto()
    PURCHASE = auto()
    REFUND = auto()
    DRAW_CASH = auto()


class TransactionStatus(EnumType):
    PENDING = auto()
    PROCESSED = auto()


class Account(DeclarativeBase):
    __tablename__ = "account"

    id = Column(String(11), primary_key=True)
    date_opened = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    name = Column(String(100), nullable=False, index=True, unique=True)

    balance = Column(Numeric(36, 18), default=0)
    debits = Column(Numeric(36, 18), default=0)
    credits = Column(Numeric(36, 18), default=0)


class Transaction(DeclarativeBase):
    __tablename__ = "transaction"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    description = Column(String(500), nullable=True)
    type = Column(
        Enum(TransactionType, name="transaction_type_enum"),
        nullable=False,
    )
    status = Column(
        Enum(TransactionStatus, name="transaction_status_enum"),
        nullable=False,
    )
    amount = Column(Numeric(36, 18), default=0)
    account_id = Column(String(11), ForeignKey("account.id"), index=True, nullable=False)
    account = relationship("Account", backref="transaction", foreign_keys=[account_id])


class TransactionAudit(DeclarativeBase):
    """
    Saves all Processed transactions and their account balances
    """

    __tablename__ = "transaction_audit"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    account_balances = Column(JSON)
    transaction_id = Column(Integer, ForeignKey("transaction.id"), index=True, nullable=False)
    transaction = relationship("Transaction", backref="transaction_audit", foreign_keys=[transaction_id])
