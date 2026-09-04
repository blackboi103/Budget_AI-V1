from calendar import month_abbr
from decimal import Decimal
from pathlib import Path

from openpyxl import load_workbook

from budget_ai.contracts import Transaction


class ExcelBudgetWriter:
    def __init__(
        self,
        workbook_path: str | Path,
        sheet_name: str = "Sheet1",
    ):
        self.workbook_path = Path(workbook_path)
        self.sheet_name = sheet_name

    def _find_cell(
        self,
        worksheet,
        value: str,
    ):
        target = value.strip().lower()

        for row in worksheet.iter_rows():
            for cell in row:
                if (
                    isinstance(cell.value, str)
                    and cell.value.strip().lower() == target
                ):
                    return cell

        return None

    def get_month_column(
        self,
        worksheet,
        month: int,
    ) -> int:
        if month < 1 or month > 12:
            raise ValueError(
                f"Invalid month: {month}"
            )

        month_name = month_abbr[month]

        cell = self._find_cell(
            worksheet,
            month_name,
        )

        if cell is None:
            raise ValueError(
                f"Could not find month "
                f"'{month_name}' in the spreadsheet."
            )

        return cell.column

    def get_category_row(
        self,
        worksheet,
        category: str,
    ) -> int:
        cell = self._find_cell(
            worksheet,
            category,
        )

        if cell is None:
            raise ValueError(
                f"Could not find category "
                f"'{category}' in the spreadsheet."
            )

        return cell.row

    def calculate_category_total(
        self,
        transactions: list[Transaction],
        category: str,
        year: int,
        month: int,
    ) -> Decimal:
        total = Decimal("0.00")

        for transaction in transactions:
            if (
                transaction.category == category
                and transaction.transaction_date.year == year
                and transaction.transaction_date.month == month
            ):
                total += transaction.amount

        return total

    def write_category_total(
        self,
        category: str,
        year: int,
        month: int,
        total: Decimal,
        output_path: str | Path | None = None,
    ) -> Path:
        workbook = load_workbook(
            self.workbook_path
        )

        if self.sheet_name not in workbook.sheetnames:
            raise ValueError(
                f"Worksheet '{self.sheet_name}' "
                "does not exist."
            )

        worksheet = workbook[
            self.sheet_name
        ]

        row = self.get_category_row(
            worksheet,
            category,
        )

        column = self.get_month_column(
            worksheet,
            month,
        )

        worksheet.cell(
            row=row,
            column=column,
        ).value = float(total)

        if output_path is None:
            output_path = (
                self.workbook_path.parent
                / (
                    f"{self.workbook_path.stem}"
                    "_BudgetAI.xlsx"
                )
            )

        output_path = Path(output_path)

        workbook.save(output_path)

        return output_path

    def sync_month(
        self,
        transactions: list[Transaction],
        categories: list[str],
        year: int,
        month: int,
        output_path: str | Path | None = None,
    ) -> Path:
        month_transactions = [
            transaction
            for transaction in transactions
            if (
                transaction.transaction_date.year == year
                and transaction.transaction_date.month == month
            )
        ]

        if not month_transactions:
            raise ValueError(
                f"No transactions found for "
                f"{month_abbr[month]} {year}. "
                "Excel sync cancelled."
            )

        workbook = load_workbook(
            self.workbook_path
        )

        if self.sheet_name not in workbook.sheetnames:
            raise ValueError(
                f"Worksheet '{self.sheet_name}' "
                "does not exist."
            )

        worksheet = workbook[
            self.sheet_name
        ]

        month_column = self.get_month_column(
            worksheet,
            month,
        )

        for category in categories:
            category_cell = self._find_cell(
                worksheet,
                category,
            )

            if category_cell is None:
                continue

            total = self.calculate_category_total(
                transactions=transactions,
                category=category,
                year=year,
                month=month,
            )

            worksheet.cell(
                row=category_cell.row,
                column=month_column,
            ).value = float(total)

        if output_path is None:
            output_path = (
                self.workbook_path.parent
                / (
                    f"{self.workbook_path.stem}"
                    "_BudgetAI.xlsx"
                )
            )

        output_path = Path(output_path)

        workbook.save(output_path)

        return output_path