from datetime import date
from decimal import Decimal

from openpyxl import Workbook, load_workbook

from budget_ai.contracts import (
    Transaction,
    TransactionType,
)
from budget_ai.excel import ExcelBudgetWriter


def create_test_workbook(path):
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Sheet1"

    worksheet["A1"] = "Category"
    worksheet["B1"] = "Jan"
    worksheet["C1"] = "Feb"
    worksheet["D1"] = "Mar"
    worksheet["E1"] = "Apr"
    worksheet["F1"] = "May"
    worksheet["G1"] = "Jun"
    worksheet["H1"] = "Jul"
    worksheet["I1"] = "Aug"

    worksheet["A2"] = "Food"
    worksheet["A3"] = "Project Car"
    worksheet["A4"] = "YouTube Channel"

    workbook.save(path)


def test_find_category_and_month(tmp_path):
    workbook_path = (
        tmp_path / "budget.xlsx"
    )

    create_test_workbook(
        workbook_path
    )

    writer = ExcelBudgetWriter(
        workbook_path
    )

    workbook = load_workbook(
        workbook_path
    )

    worksheet = workbook["Sheet1"]

    assert (
        writer.get_category_row(
            worksheet,
            "Food",
        )
        == 2
    )

    assert (
        writer.get_month_column(
            worksheet,
            8,
        )
        == 9
    )


def test_calculate_category_total(tmp_path):
    workbook_path = (
        tmp_path / "budget.xlsx"
    )

    create_test_workbook(
        workbook_path
    )

    writer = ExcelBudgetWriter(
        workbook_path
    )

    transactions = [
        Transaction(
            transaction_id="txn_001",
            transaction_date=date(
                2026,
                8,
                5,
            ),
            description="Publix",
            amount=Decimal("47.82"),
            transaction_type=(
                TransactionType.EXPENSE
            ),
            category="Food",
        ),
        Transaction(
            transaction_id="txn_002",
            transaction_date=date(
                2026,
                8,
                10,
            ),
            description="Chipotle",
            amount=Decimal("18.25"),
            transaction_type=(
                TransactionType.EXPENSE
            ),
            category="Food",
        ),
    ]

    total = (
        writer.calculate_category_total(
            transactions,
            category="Food",
            year=2026,
            month=8,
        )
    )

    assert total == Decimal("66.07")


def test_write_category_total(tmp_path):
    workbook_path = (
        tmp_path / "budget.xlsx"
    )

    output_path = (
        tmp_path / "updated.xlsx"
    )

    create_test_workbook(
        workbook_path
    )

    writer = ExcelBudgetWriter(
        workbook_path
    )

    writer.write_category_total(
        category="Food",
        year=2026,
        month=8,
        total=Decimal("66.07"),
        output_path=output_path,
    )

    workbook = load_workbook(
        output_path
    )

    worksheet = workbook["Sheet1"]

    assert worksheet["I2"].value == 66.07
def test_sync_entire_month(tmp_path):
    workbook_path = (
        tmp_path / "budget.xlsx"
    )

    output_path = (
        tmp_path / "updated.xlsx"
    )

    create_test_workbook(
        workbook_path
    )

    writer = ExcelBudgetWriter(
        workbook_path
    )

    transactions = [
        Transaction(
            transaction_id="txn_001",
            transaction_date=date(2026, 8, 5),
            description="Publix",
            amount=Decimal("47.82"),
            transaction_type=TransactionType.EXPENSE,
            category="Food",
        ),
        Transaction(
            transaction_id="txn_002",
            transaction_date=date(2026, 8, 10),
            description="Chipotle",
            amount=Decimal("18.25"),
            transaction_type=TransactionType.EXPENSE,
            category="Food",
        ),
        Transaction(
            transaction_id="txn_003",
            transaction_date=date(2026, 8, 15),
            description="Car Parts",
            amount=Decimal("125.00"),
            transaction_type=TransactionType.EXPENSE,
            category="Project Car",
        ),
    ]

    writer.sync_month(
        transactions=transactions,
        categories=[
            "Food",
            "Project Car",
            "YouTube Channel",
        ],
        year=2026,
        month=8,
        output_path=output_path,
    )

    workbook = load_workbook(
        output_path
    )

    worksheet = workbook["Sheet1"]

    assert worksheet["I2"].value == 66.07
    assert worksheet["I3"].value == 125.00
    assert worksheet["I4"].value == 0