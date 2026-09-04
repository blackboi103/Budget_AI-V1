from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Protocol

from budget_ai.contracts import TransactionType


@dataclass
class ImportedTransaction:
    external_id: str
    transaction_date: date
    description: str
    amount: Decimal
    transaction_type: TransactionType


class TransactionProvider(Protocol):
    @property
    def name(self) -> str:
        ...

    def get_transactions(
        self,
        start_date: date,
        end_date: date,
    ) -> list[ImportedTransaction]:
        ...