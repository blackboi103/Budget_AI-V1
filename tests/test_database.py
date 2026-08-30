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


def test_transaction_survives_restart(
    tmp_path,
):
    database_path = tmp_path / "budget.db"

    service = BudgetService(database_path)

    transaction = make_transaction(
        "txn_001",
        "Publix",
    )

    service.add_transaction(transaction)

    service.close()

    service = BudgetService(database_path)

    saved = (
        service.transactions.get_transaction(
            "txn_001"
        )
    )

    assert saved is not None
    assert saved.description == "Publix"
    assert saved.amount == Decimal("47.82")

    service.close()


def test_learned_category_survives_restart(
    tmp_path,
):
    database_path = tmp_path / "budget.db"

    service = BudgetService(database_path)

    first = make_transaction(
        "txn_001",
        "Publix",
    )

    service.add_transaction(first)

    service.learn_transaction_category(
        first,
        "Food",
    )

    service.close()

    # Simulates reopening BudgetAI later.
    service = BudgetService(database_path)

    second = make_transaction(
        "txn_002",
        "Publix",
    )

    service.add_transaction(second)

    assert second.category == "Food"

    service.close()