from datetime import date

from budget_ai.providers.mock import MockTransactionProvider
from budget_ai.review import ReviewReason
from budget_ai.service import BudgetService
from budget_ai.sync import TransactionSyncService


def test_unknown_transactions_are_saved_for_review(
    tmp_path,
):
    database_path = tmp_path / "budget.db"

    service = BudgetService(
        database_path
    )

    sync_service = TransactionSyncService(
        service
    )

    sync_service.sync(
        MockTransactionProvider(),
        date(2026, 9, 1),
        date(2026, 9, 30),
    )

    pending = (
        service.review_queue.list_pending()
    )

    assert len(pending) == 3

    assert (
        pending[0].reason
        == ReviewReason.NEW_MERCHANT
    )

    service.close()


def test_review_queue_survives_restart(
    tmp_path,
):
    database_path = tmp_path / "budget.db"

    service = BudgetService(
        database_path
    )

    TransactionSyncService(
        service
    ).sync(
        MockTransactionProvider(),
        date(2026, 9, 1),
        date(2026, 9, 30),
    )

    service.close()

    service = BudgetService(
        database_path
    )

    pending = (
        service.review_queue.list_pending()
    )

    assert len(pending) == 3

    service.close()


def test_review_can_be_resolved(
    tmp_path,
):
    service = BudgetService(
        tmp_path / "budget.db"
    )

    TransactionSyncService(
        service
    ).sync(
        MockTransactionProvider(),
        date(2026, 9, 1),
        date(2026, 9, 30),
    )

    pending = (
        service.review_queue.list_pending()
    )

    review = pending[0]

    service.review_queue.resolve(
        review.review_id
    )

    remaining = (
        service.review_queue.list_pending()
    )

    assert len(remaining) == 2

    service.close()


def test_repeated_sync_does_not_duplicate_reviews(
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

    sync_service.sync(
        provider,
        date(2026, 9, 1),
        date(2026, 9, 30),
    )

    pending = (
        service.review_queue.list_pending()
    )

    assert len(pending) == 3

    service.close()