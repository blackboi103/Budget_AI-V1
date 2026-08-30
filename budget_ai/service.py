from budget_ai.categories import CategoryManager, DEFAULT_CATEGORIES
from budget_ai.contracts import Transaction
from budget_ai.transactions import TransactionManager


class BudgetService:
    def __init__(self):
        self.transactions = TransactionManager()
        self.categories = CategoryManager()

    def add_transaction(self, transaction: Transaction) -> Transaction:
        learned_category = self.categories.categorize(transaction)

        if learned_category is not None:
            transaction.category = learned_category

        self.transactions.add_transaction(transaction)

        return transaction

    def needs_category(self, transaction: Transaction) -> bool:
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

    def get_available_categories(self) -> list[str]:
        return DEFAULT_CATEGORIES.copy()