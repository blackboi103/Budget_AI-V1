from dataclasses import dataclass, field
from datetime import date
from unittest import result

from budget_ai.contracts import Transaction
from budget_ai.providers.base import TransactionProvider
from budget_ai.service import BudgetService
from budget_ai.review import ReviewReason


@dataclass
class SyncResult:
    imported: int = 0
    duplicates: int = 0

    needs_review: list[Transaction] = field(
        default_factory=list
    )


class TransactionSyncService:
    def __init__(
        self,
        budget_service: BudgetService,
    ):
        self.budget_service = budget_service

    def sync(
        self,
        provider: TransactionProvider,
        start_date: date,
        end_date: date,
    ) -> SyncResult:
        result = SyncResult()

        imported_transactions = (
            provider.get_transactions(
                start_date=start_date,
                end_date=end_date,
            )
        )

        for imported in imported_transactions:
            transaction_id = (
                f"{provider.name}:"
                f"{imported.external_id}"
            )

            transaction = Transaction(
                transaction_id=transaction_id,
                transaction_date=(
                    imported.transaction_date
                ),
                description=imported.description,
                amount=imported.amount,
                transaction_type=(
                    imported.transaction_type
                ),
            )

            try:
                self.budget_service.add_transaction(
                    transaction
                )

            except ValueError:
                result.duplicates += 1
                continue

            result.imported += 1

            if self.budget_service.needs_category(
                transaction
            ):
                result.needs_review.append(
                    transaction
                )

                self.budget_service.review_queue.add(
                    transaction_id=(
                        transaction.transaction_id
         ),
                    reason=ReviewReason.NEW_MERCHANT,
                    note=(
                        f"BudgetAI has not learned how "
                        f"to categorize "
                        f"'{transaction.description}'."
                    ),
        )

        return result