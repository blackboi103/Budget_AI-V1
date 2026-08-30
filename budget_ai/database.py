from datetime import date
from decimal import Decimal
from pathlib import Path
import sqlite3

from budget_ai.contracts import Transaction, TransactionType


class BudgetDatabase:
    def __init__(self, database_path: str | Path = "data/budget.db"):
        self.database_path = str(database_path)

        if self.database_path != ":memory:":
            path = Path(self.database_path)
            path.parent.mkdir(parents=True, exist_ok=True)

        self.connection = sqlite3.connect(self.database_path)
        self.connection.row_factory = sqlite3.Row

        self._create_tables()

    def _create_tables(self) -> None:
        with self.connection:
            self.connection.execute(
                """
                CREATE TABLE IF NOT EXISTS transactions (
                    transaction_id TEXT PRIMARY KEY,
                    transaction_date TEXT NOT NULL,
                    description TEXT NOT NULL,
                    amount TEXT NOT NULL,
                    transaction_type TEXT NOT NULL,
                    category TEXT
                )
                """
            )

            self.connection.execute(
                """
                CREATE TABLE IF NOT EXISTS category_rules (
                    merchant TEXT PRIMARY KEY,
                    category TEXT NOT NULL,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

    def add_transaction(self, transaction: Transaction) -> None:
        try:
            with self.connection:
                self.connection.execute(
                    """
                    INSERT INTO transactions (
                        transaction_id,
                        transaction_date,
                        description,
                        amount,
                        transaction_type,
                        category
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        transaction.transaction_id,
                        transaction.transaction_date.isoformat(),
                        transaction.description,
                        str(transaction.amount),
                        transaction.transaction_type.value,
                        transaction.category,
                    ),
                )

        except sqlite3.IntegrityError as exc:
            raise ValueError(
                f"Transaction '{transaction.transaction_id}' already exists."
            ) from exc

    def get_transaction(
        self,
        transaction_id: str,
    ) -> Transaction | None:
        row = self.connection.execute(
            """
            SELECT *
            FROM transactions
            WHERE transaction_id = ?
            """,
            (transaction_id,),
        ).fetchone()

        if row is None:
            return None

        return self._row_to_transaction(row)

    def list_transactions(self) -> list[Transaction]:
        rows = self.connection.execute(
            """
            SELECT *
            FROM transactions
            ORDER BY transaction_date, transaction_id
            """
        ).fetchall()

        return [
            self._row_to_transaction(row)
            for row in rows
        ]

    def count_transactions(self) -> int:
        row = self.connection.execute(
            """
            SELECT COUNT(*) AS count
            FROM transactions
            """
        ).fetchone()

        return row["count"]

    def update_transaction_category(
        self,
        transaction_id: str,
        category: str,
    ) -> None:
        with self.connection:
            cursor = self.connection.execute(
                """
                UPDATE transactions
                SET category = ?
                WHERE transaction_id = ?
                """,
                (
                    category,
                    transaction_id,
                ),
            )

        if cursor.rowcount == 0:
            raise KeyError(
                f"Transaction '{transaction_id}' does not exist."
            )

    def save_category_rule(
        self,
        merchant: str,
        category: str,
    ) -> None:
        with self.connection:
            self.connection.execute(
                """
                INSERT INTO category_rules (
                    merchant,
                    category
                )
                VALUES (?, ?)

                ON CONFLICT(merchant)
                DO UPDATE SET
                    category = excluded.category,
                    updated_at = CURRENT_TIMESTAMP
                """,
                (
                    merchant,
                    category,
                ),
            )

    def get_category_rule(
        self,
        merchant: str,
    ) -> str | None:
        row = self.connection.execute(
            """
            SELECT category
            FROM category_rules
            WHERE merchant = ?
            """,
            (merchant,),
        ).fetchone()

        if row is None:
            return None

        return row["category"]

    def _row_to_transaction(
        self,
        row: sqlite3.Row,
    ) -> Transaction:
        return Transaction(
            transaction_id=row["transaction_id"],
            transaction_date=date.fromisoformat(
                row["transaction_date"]
            ),
            description=row["description"],
            amount=Decimal(row["amount"]),
            transaction_type=TransactionType(
                row["transaction_type"]
            ),
            category=row["category"],
        )

    def close(self) -> None:
        self.connection.close()