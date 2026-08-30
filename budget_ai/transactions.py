from budget_ai.contracts import Transaction


class TransactionManager:
    def __init__(self):
        self._transactions: dict[str, Transaction] = {}

    def add_transaction(self, transaction: Transaction) -> None:
        if transaction.transaction_id in self._transactions:
            raise ValueError(
                f"Transaction '{transaction.transaction_id}' already exists."
            )

        self._transactions[transaction.transaction_id] = transaction

    def get_transaction(self, transaction_id: str) -> Transaction | None:
        return self._transactions.get(transaction_id)

    def list_transactions(self) -> list[Transaction]:
        return list(self._transactions.values())

    def count(self) -> int:
        return len(self._transactions)