# BudgetAI: Plaid-first backend, statement fallback

BudgetAI is a private finance specialist for BlackBot. This repository supplies the finance logic and connection hooks; it does **not** replace BlackBot's WebUI with a separate budgeting website.

## What works in this migration

- Transactions-only Plaid SDK adapter, sandbox by default.
- Bank access tokens stored in a vetted native OS keyring, not SQLite or source files.
- Account/currency/environment-aware transaction identities.
- Pending purchases, posted replacements, modified records, and removals.
- Complete paginated updates and their sync cursor committed together. Failed pagination leaves the old state intact.
- Purchase-specific category reviews and explicit classification approval; type-only approvals retain any missing-category question.
- Actual income excludes pending inflows, and Excel exports reject mixed known/unknown currencies rather than adding them.
- Local PDF candidate extraction, reviewed statement reconciliation, and the original historical fallback tools.
- CLI entry points for status, setup, sync, polling, and month-end checks.

## Browser integration checkpoint — November 12, 2026

**Not cleared for real-bank setup or real workbook writes.** The reviewed
connection-handoff, recovery-UI/CSP and worksheet-XML fixes pass the parent's
713-test checkpoint, 29 frontend tests and all four original independent workbook
regressions. Isolated browser navigation/status and public SDK/CSP checks also
passed. Independent re-review found a delayed-worker authorization race and
worksheet namespace/preflight mismatches; a second targeted fix cycle is running.
Re-review clearance and operational acceptance remain pending.
Automatic post-crash provider recovery is not implemented; unresolved attempts
stay durably blocked. The commands below document entry points, not clearance
to connect a real account or publish a financial workbook.

The user-selected BlackBot v0.2 frontend is preserved as a working copy under
`budget_ai/web_static/blackbot`. Its BudgetAI room now has an authenticated
loopback backend for configuration, official Plaid Link, explicit sync and
purchase-specific reviews. The other agents remain clearly labeled demonstrations.
The original downloaded ZIP is not the served working copy and was not modified.

Install the additional browser dependencies with the project's interpreter:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-web.txt
```

The implemented launcher is:

```powershell
.\.venv\Scripts\python.exe -m budget_ai.web_runtime --open-browser
```

It binds only to `127.0.0.1` and opens Chrome with a temporary authorization
fragment. Do not copy that authorization into chat or store it in a bookmark.
Keys belong only in the local masked setup form, never in chat. Production setup
and each bank action require explicit approval; installing or opening the UI does
not connect TD. Independent current-code review and a real browser exercise remain
deployment gates at this checkpoint.

Additional implemented modules include conservative TD CSV/wrapped-PDF evidence
readers (`td_evidence.py`) and a workbook dry-run/approved new-copy engine
(`workbook_catchup.py`). These modules are not yet a complete browser/CLI
three-way reconciliation workflow. No approval to change the original workbook
is implied. Formula recalculation and output verification remain separate gates.

Latest local verification: **670 Python tests passed**, with one upstream
Starlette/httpx test-client deprecation warning; **22 standalone frontend tests
passed**. These are offline/synthetic integration checks, not proof of a live TD
connection or completed real-data reconciliation. See the roadmap checkpoint for
the actual CSV/PDF intake findings.

## Install

From this repository on Windows:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-plaid.txt
.\.venv\Scripts\python.exe -m budget_ai --help
.\.venv\Scripts\python.exe -m budget_ai status
```

`run_budget_ai.py` exposes the same commands. `status` and `reviews` are read-only and do not initialize a missing database.

Default private database locations:

- Sandbox: `~/BudgetAI-Private/plaid-sandbox.db`
- Production: `~/BudgetAI-Private/plaid-production.db`

Override with `--database PATH` **before** the subcommand, or `BUDGETAI_DATABASE`. Do not point a bank connection at an existing historical-import database: this migration requires explicit reconciliation rather than silently merging two spending histories. Sandbox and production cannot share a registered ledger. Nothing automatically moves your older databases or spreadsheets.

## Next steps

See [the setup and reconciliation guide](docs/plaid-migration.md) for environment variables, Sandbox setup, bank-sync polling, PDF fallback, approval commands, and BlackBot integration boundaries.

**No live bank connection is created just by installing or running tests.** The user confirmed the v0.2 ZIP as the WebUI baseline and completed trial enrollment. Actual TD eligibility, live Link consent, available history and account-specific costs still require verification. The tests use deliberately simulated Plaid responses, not results from your bank.
