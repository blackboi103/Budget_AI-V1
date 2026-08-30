from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from enum import Enum


class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"


@dataclass
class Transaction:
    transaction_id: str
    transaction_date: date
    description: str
    amount: Decimal
    transaction_type: TransactionType
    category: str | None = None