from datetime import date
from decimal import Decimal

from budget_ai.contracts import Transaction, TransactionType


def test_create_transaction():
    transaction = Transaction(
        transaction_id="txn_001",
        transaction_date=date(2026, 8, 30),
        description="Publix",
        amount=Decimal("47.82"),
        transaction_type=TransactionType.EXPENSE,
        category="Food",
    )

    assert transaction.description == "Publix"
    assert transaction.amount == Decimal("47.82")
    assert transaction.transaction_type == TransactionType.EXPENSE
    assert transaction.category == "Food"