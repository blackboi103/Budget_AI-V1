from dataclasses import dataclass
from enum import Enum

from budget_ai.database import BudgetDatabase


class ReviewReason(str, Enum):
    NEW_MERCHANT = "new_merchant"
    AMBIGUOUS_CATEGORY = "ambiguous_category"
    UNUSUAL_AMOUNT = "unusual_amount"
    POSSIBLE_DUPLICATE = "possible_duplicate"
    UNKNOWN_TRANSACTION = "unknown_transaction"


class ReviewStatus(str, Enum):
    PENDING = "pending"
    RESOLVED = "resolved"
    DISMISSED = "dismissed"


@dataclass
class ReviewItem:
    review_id: str
    transaction_id: str
    reason: ReviewReason
    status: ReviewStatus
    note: str | None = None


class ReviewQueue:
    def __init__(
        self,
        database: BudgetDatabase,
    ):
        self.database = database

    def add(
        self,
        transaction_id: str,
        reason: ReviewReason,
        note: str | None = None,
    ) -> None:
        review_id = (
            f"{transaction_id}:{reason.value}"
        )

        self.database.add_review_item(
            review_id=review_id,
            transaction_id=transaction_id,
            reason=reason.value,
            status=ReviewStatus.PENDING.value,
            note=note,
        )

    def list_pending(
        self,
    ) -> list[ReviewItem]:
        rows = self.database.list_review_items(
            status=ReviewStatus.PENDING.value
        )

        return [
            ReviewItem(
                review_id=row["review_id"],
                transaction_id=row["transaction_id"],
                reason=ReviewReason(row["reason"]),
                status=ReviewStatus(row["status"]),
                note=row["note"],
            )
            for row in rows
        ]

    def resolve(
        self,
        review_id: str,
    ) -> None:
        self.database.update_review_status(
            review_id,
            ReviewStatus.RESOLVED.value,
        )

    def dismiss(
        self,
        review_id: str,
    ) -> None:
        self.database.update_review_status(
            review_id,
            ReviewStatus.DISMISSED.value,
        )