"""Evaluate selected HTTP entity-tag preconditions for an existing resource."""
import re

_TAG = re.compile(r'^(W/)?"[^"\\\r\n]*"$')

def parse_etags(header):
    if header.strip() == "*":
        return ["*"]
    parts = [part.strip() for part in header.split(",")]
    if not parts or not all(_TAG.fullmatch(part) for part in parts):
        raise ValueError("invalid ETag header")
    return parts

def strong(a, b):
    return not a.startswith("W/") and not b.startswith("W/") and a == b

def weak(a, b):
    return a.removeprefix("W/") == b.removeprefix("W/")

def evaluate(method, current_etag, if_match=None, if_none_match=None):
    """Return 200 (proceed), 304 (not modified), or 412 (failed)."""
    if current_etag is not None and not _TAG.fullmatch(current_etag):
        raise ValueError("invalid current ETag")
    exists = current_etag is not None
    if if_match is not None:
        tags = parse_etags(if_match)
        if not (exists and ("*" in tags or any(strong(t, current_etag) for t in tags))):
            return 412
    if if_none_match is not None:
        tags = parse_etags(if_none_match)
        matches = exists and ("*" in tags or any(weak(t, current_etag) for t in tags))
        if matches:
            return 304 if method.upper() in ("GET", "HEAD") else 412
    return 200

if __name__ == "__main__":
    print(evaluate("GET", '"v1"', if_none_match='W/"v1"'))
