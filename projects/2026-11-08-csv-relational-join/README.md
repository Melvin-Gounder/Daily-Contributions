# CSV Hash Join CLI

Merge exports with inner or left joins on independently named key columns. Duplicate right-hand keys produce multiple rows. Colliding non-key column names receive repeated `right_` prefixes until unique. Invalid headers and malformed rows raise errors.

Example: `python join_csv.py customers.csv orders.csv joined.csv --left-key id --right-key customer_id --how left`.

Tests: `python -m unittest -v test_join_csv.py`. Standard library only.

The right table is indexed in memory, while left rows stream into the output. Expected time O(L+R+K) for L left rows, R right rows and K output rows; memory O(R). For huge right inputs use a database or external merge join. Never use an input path as the output path.
