from datetime import date

from budget_ai.providers.mock import (
    MockTransactionProvider,
)
from budget_ai.service import BudgetService
from budget_ai.sync import TransactionSyncService


def test_sync_imports_transactions(tmp_path):
    service = BudgetService(
        tmp_path / "budget.db"
    )

    sync_service = TransactionSyncService(
        service
    )

    provider = MockTransactionProvider()

    result = sync_service.sync(
        provider=provider,
        start_date=date(2026, 9, 1),
        end_date=date(2026, 9, 30),
    )

    assert result.imported == 3

    assert (
        service.transactions.count()
        == 3
    )

    service.close()


def test_sync_does_not_duplicate_transactions(
    tmp_path,
):
    service = BudgetService(
        tmp_path / "budget.db"
    )

    sync_service = TransactionSyncService(
        service
    )

    provider = MockTransactionProvider()

    sync_service.sync(
        provider,
        date(2026, 9, 1),
        date(2026, 9, 30),
    )

    second_sync = sync_service.sync(
        provider,
        date(2026, 9, 1),
        date(2026, 9, 30),
    )

    assert second_sync.imported == 0
    assert second_sync.duplicates == 3

    assert (
        service.transactions.count()
        == 3
    )

    service.close()


def test_unknown_transactions_require_review(
    tmp_path,
):
    service = BudgetService(
        tmp_path / "budget.db"
    )

    sync_service = TransactionSyncService(
        service
    )

    result = sync_service.sync(
        MockTransactionProvider(),
        date(2026, 9, 1),
        date(2026, 9, 30),
    )

    assert len(result.needs_review) == 3

    service.close()
def test_learned_merchant_is_automatically_categorized(
    tmp_path,
):
    service = BudgetService(
        tmp_path / "budget.db"
    )

    service.categories.learn_category(
        "Publix",
        "Food",
    )

    sync_service = TransactionSyncService(
        service
    )

    result = sync_service.sync(
        MockTransactionProvider(),
        date(2026, 9, 1),
        date(2026, 9, 30),
    )

    review_descriptions = [
        transaction.description
        for transaction in result.needs_review
    ]

    assert "Publix" not in review_descriptions

    saved = service.transactions.get_transaction(
        "mock:001"
    )

    assert saved is not None
    assert saved.category == "Food"

    service.close()