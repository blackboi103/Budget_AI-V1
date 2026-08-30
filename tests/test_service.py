from datetime import date
from decimal import Decimal

from budget_ai.contracts import (
    Transaction,
    TransactionType,
)
from budget_ai.service import BudgetService


def make_transaction(
    transaction_id: str,
    description: str,
) -> Transaction:
    return Transaction(
        transaction_id=transaction_id,
        transaction_date=date(2026, 8, 30),
        description=description,
        amount=Decimal("47.82"),
        transaction_type=TransactionType.EXPENSE,
    )


def test_new_merchant_needs_category(tmp_path):
    service = BudgetService(
        tmp_path / "test.db"
    )

    transaction = make_transaction(
        "txn_001",
        "Publix",
    )

    service.add_transaction(transaction)

    assert service.needs_category(
        transaction
    ) is True

    service.close()


def test_service_learns_category(tmp_path):
    service = BudgetService(
        tmp_path / "test.db"
    )

    transaction = make_transaction(
        "txn_001",
        "Publix",
    )

    service.add_transaction(transaction)

    service.learn_transaction_category(
        transaction,
        "Food",
    )

    assert transaction.category == "Food"

    service.close()


def test_future_transaction_uses_learned_category(
    tmp_path,
):
    service = BudgetService(
        tmp_path / "test.db"
    )

    first = make_transaction(
        "txn_001",
        "Publix",
    )

    service.add_transaction(first)

    service.learn_transaction_category(
        first,
        "Food",
    )

    second = make_transaction(
        "txn_002",
        "Publix",
    )

    service.add_transaction(second)

    assert second.category == "Food"

    assert service.needs_category(
        second
    ) is False

    service.close()