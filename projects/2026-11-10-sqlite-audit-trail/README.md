# SQLite Audit Trail Demo

SQLite trigger-based change history for inventory records, parameterized updates, transactional writes, and history reconstruction.

## Run

Requires Python 3.10+ and only the standard library. From this project directory:

```bash
python audit.py
python -m unittest -v test_audit.py
```

## Design and limitations

Uses SQLite JSON1 functions (included in modern SQLite builds). Triggers fire inside the same transaction as the inventory mutation. This is an application demonstration, not a tamper-proof audit log: a database administrator can still edit the audit table.

## Learning objectives

Read the implementation and tests together to understand invariants, input validation, boundary cases, and failure behavior. Extend the tests before modifying core logic.
