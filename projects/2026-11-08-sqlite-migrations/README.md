# Transactional SQLite Migrations

Demonstrates schema versioning, drift detection using SHA-256 checksums, idempotent application, and atomic per-migration rollback. The sample schema models customers and orders with referential integrity.

Run `python migrations.py` or `python -m unittest -v test_migrations.py` in this directory. Uses Python's standard-library sqlite3.

Migrations are trusted, single-statement SQL strings. Each executes under BEGIN IMMEDIATE and its checksum is recorded in the same transaction. SQLite foreign-key checks are enabled. History validation is O(n), excluding database DDL cost. This is an educational runner, not a production framework with down-migrations, multi-statement scripts, or cross-database support.
