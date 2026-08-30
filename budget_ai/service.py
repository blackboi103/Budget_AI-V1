from pathlib import Path

from budget_ai.categories import (
    CategoryManager,
    DEFAULT_CATEGORIES,
)
from budget_ai.contracts import Transaction
from budget_ai.database import BudgetDatabase
from budget_ai.transactions import TransactionManager


class BudgetService:
    def __init__(
        self,
        database_path: str | Path = "data/budget.db",
    ):
        self.database = BudgetDatabase(
            database_path
        )

        self.transactions = TransactionManager(
            self.database
        )

        self.categories = CategoryManager(
            self.database
        )

    def add_transaction(
        self,
        transaction: Transaction,
    ) -> Transaction:
        learned_category = (
            self.categories.categorize(
                transaction
            )
        )

        if learned_category is not None:
            transaction.category = (
                learned_category
            )

        self.transactions.add_transaction(
            transaction
        )

        return transaction

    def needs_category(
        self,
        transaction: Transaction,
    ) -> bool:
        return transaction.category is None

    def learn_transaction_category(
        self,
        transaction: Transaction,
        category: str,
    ) -> None:
        self.categories.learn_category(
            transaction.description,
            category,
        )

        transaction.category = category

        self.transactions.update_category(
            transaction.transaction_id,
            category,
        )

    def get_available_categories(
        self,
    ) -> list[str]:
        return DEFAULT_CATEGORIES.copy()

    def close(self) -> None:
        self.database.close()