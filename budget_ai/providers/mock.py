from datetime import date
from decimal import Decimal

from budget_ai.contracts import TransactionType
from budget_ai.providers.base import ImportedTransaction


class MockTransactionProvider:
    @property
    def name(self) -> str:
        return "mock"

    def get_transactions(
        self,
        start_date: date,
        end_date: date,
    ) -> list[ImportedTransaction]:
        transactions = [
            ImportedTransaction(
                external_id="001",
                transaction_date=date(2026, 9, 1),
                description="Publix",
                amount=Decimal("42.18"),
                transaction_type=TransactionType.EXPENSE,
            ),
            ImportedTransaction(
                external_id="002",
                transaction_date=date(2026, 9, 2),
                description="Shell",
                amount=Decimal("51.70"),
                transaction_type=TransactionType.EXPENSE,
            ),
            ImportedTransaction(
                external_id="003",
                transaction_date=date(2026, 9, 2),
                description="Amazon",
                amount=Decimal("27.41"),
                transaction_type=TransactionType.EXPENSE,
            ),
        ]

        return [
            transaction
            for transaction in transactions
            if (
                start_date
                <= transaction.transaction_date
                <= end_date
            )
        ]