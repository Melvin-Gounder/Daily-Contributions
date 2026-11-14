"""Offline educational DNS zone-file record checks."""
import ipaddress
import re

LABEL = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?$")

def hostname(name):
    value = name.rstrip(".")
    return bool(value) and len(value) <= 253 and all(LABEL.fullmatch(part) for part in value.split("."))

def lint(records):
    """Return human-readable errors; records are (owner, type, value) tuples."""
    errors, by_owner = [], {}
    for line, record in enumerate(records, 1):
        if len(record) != 3:
            errors.append(f"record {line}: expected owner, type, value")
            continue
        owner, kind, value = record
        kind = kind.upper()
        if not hostname(owner):
            errors.append(f"record {line}: invalid owner")
        by_owner.setdefault(owner.lower(), set()).add(kind)
        try:
            if kind in ("A", "AAAA"):
                ip = ipaddress.ip_address(value)
                if ip.version != (4 if kind == "A" else 6):
                    raise ValueError("address family mismatch")
            elif kind == "CNAME":
                if not hostname(value): raise ValueError("invalid CNAME target")
            elif kind == "MX":
                priority, destination = value.split(maxsplit=1)
                if not priority.isdigit() or not 0 <= int(priority) <= 65535 or not hostname(destination):
                    raise ValueError("invalid MX value")
            elif kind == "TXT":
                if not value or len(value.encode("utf-8")) > 255:
                    raise ValueError("TXT must contain 1–255 UTF-8 bytes")
            else:
                raise ValueError("unsupported record type")
        except ValueError as exc:
            errors.append(f"record {line}: {exc}")
    for owner, kinds in sorted(by_owner.items()):
        if "CNAME" in kinds and len(kinds) > 1:
            errors.append(f"{owner}: CNAME cannot coexist with other record types")
    return errors

if __name__ == "__main__":
    print(lint([("example.org","A","192.0.2.1"),("www.example.org","CNAME","example.org")]))
