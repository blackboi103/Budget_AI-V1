from datetime import date
from decimal import Decimal

import pytest

from budget_ai.categories import CategoryManager
from budget_ai.contracts import Transaction, TransactionType


def make_transaction(description: str = "Publix") -> Transaction:
    return Transaction(
        transaction_id="txn_001",
        transaction_date=date(2026, 8, 30),
        description=description,
        amount=Decimal("47.82"),
        transaction_type=TransactionType.EXPENSE,
    )


def test_unknown_merchant_returns_none():
    manager = CategoryManager()

    transaction = make_transaction("Publix")

    category = manager.categorize(transaction)

    assert category is None


def test_learn_category():
    manager = CategoryManager()

    manager.learn_category("Publix", "Food")

    transaction = make_transaction("Publix")

    assert manager.categorize(transaction) == "Food"


def test_learning_is_case_insensitive():
    manager = CategoryManager()

    manager.learn_category("Publix", "Food")

    transaction = make_transaction("PUBLIX")

    assert manager.categorize(transaction) == "Food"


def test_correct_category():
    manager = CategoryManager()

    manager.learn_category("Publix", "Stuff")
    manager.correct_category("Publix", "Food")

    assert manager.get_learned_category("Publix") == "Food"


def test_invalid_category_is_rejected():
    manager = CategoryManager()

    with pytest.raises(ValueError):
        manager.learn_category("Publix", "Random Category")