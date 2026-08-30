from dataclasses import dataclass

from budget_ai.contracts import Transaction
from budget_ai.database import BudgetDatabase


CATEGORY_GROUPS = {
    "Income": [
        "Respiratory",
        "Income 2",
        "Sent By Mom",
    ],

    "Needs": [
        "Gas",
        "Insurance",
        "Paying Mom",
    ],

    "Savings and Payments": [
        "Savings Account",
        "Investment Accounts",
        "Trading Expenses",
        "Tolls",
    ],

    "Wants": [
        "Stuff",
        "Angel",
        "Family",
        "Food",
        "Friends",
        "Project Car",
        "YouTube Channel",
        "Crunchyroll",
        "Spotify",
        "Amazon",
        "Apple",
    ],
}


DEFAULT_CATEGORIES = [
    category
    for categories in CATEGORY_GROUPS.values()
    for category in categories
]


@dataclass
class CategoryRule:
    merchant: str
    category: str


class CategoryManager:
    def __init__(
        self,
        database: BudgetDatabase | None = None,
    ):
        if database is None:
            database = BudgetDatabase(":memory:")

        self.database = database

    def _normalize_merchant(
        self,
        description: str,
    ) -> str:
        return description.strip().lower()

    def learn_category(
        self,
        merchant: str,
        category: str,
    ) -> None:
        if category not in DEFAULT_CATEGORIES:
            raise ValueError(
                f"Unknown category: {category}"
            )

        normalized = self._normalize_merchant(
            merchant
        )

        self.database.save_category_rule(
            normalized,
            category,
        )

    def get_learned_category(
        self,
        merchant: str,
    ) -> str | None:
        normalized = self._normalize_merchant(
            merchant
        )

        return self.database.get_category_rule(
            normalized
        )

    def categorize(
        self,
        transaction: Transaction,
    ) -> str | None:
        return self.get_learned_category(
            transaction.description
        )

    def correct_category(
        self,
        merchant: str,
        new_category: str,
    ) -> None:
        self.learn_category(
            merchant,
            new_category,
        )