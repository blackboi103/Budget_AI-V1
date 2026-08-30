from datetime import date
from decimal import Decimal

import pytest

from budget_ai.contracts import Transaction, TransactionType
from budget_ai.transactions import TransactionManager


def make_transaction(
    transaction_id: str = "txn_001",
) -> Transaction:
    return Transaction(
        transaction_id=transaction_id,
        transaction_date=date(2026, 8, 30),
        description="Publix",
        amount=Decimal("47.82"),
        transaction_type=TransactionType.EXPENSE,
        category="Food",
    )


def test_add_transaction():
    manager = TransactionManager()
    transaction = make_transaction()

    manager.add_transaction(transaction)

    assert manager.count() == 1


def test_get_transaction():
    manager = TransactionManager()
    transaction = make_transaction()

    manager.add_transaction(transaction)

    result = manager.get_transaction("txn_001")

    assert result == transaction


def test_list_transactions():
    manager = TransactionManager()

    manager.add_transaction(make_transaction("txn_001"))
    manager.add_transaction(make_transaction("txn_002"))

    transactions = manager.list_transactions()

    assert len(transactions) == 2


def test_duplicate_transaction_id_is_rejected():
    manager = TransactionManager()

    manager.add_transaction(make_transaction("txn_001"))

    with pytest.raises(ValueError):
        manager.add_transaction(make_transaction("txn_001"))