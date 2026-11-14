# RFC 7396 JSON Merge Patch

Standards-based JSON object merge patching with deletion semantics and immutable inputs.

## Run

Python 3.9+; standard library only.

```sh
cd projects/2026-11-15-json-merge-patch
python tool.py
python -m unittest -v test_tool.py
```

## Design and limitations

Standards-based JSON object merge patching with deletion semantics and immutable inputs. Educational implementation with deterministic unit tests. Not hardened for untrusted workloads or large inputs; validate concurrency and performance before production use.
