from budget_ai.contracts import Transaction
from budget_ai.database import BudgetDatabase


class TransactionManager:
    def __init__(
        self,
        database: BudgetDatabase | None = None,
    ):
        if database is None:
            database = BudgetDatabase(":memory:")

        self.database = database

    def add_transaction(
        self,
        transaction: Transaction,
    ) -> None:
        self.database.add_transaction(transaction)

    def get_transaction(
        self,
        transaction_id: str,
    ) -> Transaction | None:
        return self.database.get_transaction(
            transaction_id
        )

    def list_transactions(
        self,
    ) -> list[Transaction]:
        return self.database.list_transactions()

    def count(self) -> int:
        return self.database.count_transactions()

    def update_category(
        self,
        transaction_id: str,
        category: str,
    ) -> None:
        self.database.update_transaction_category(
            transaction_id,
            category,
        )