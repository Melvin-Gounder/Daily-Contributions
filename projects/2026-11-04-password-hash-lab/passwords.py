"""Educational PBKDF2 password storage; not an authentication service."""
import base64
import hashlib
import hmac
import secrets

ALGORITHM = "pbkdf2_sha256"
ITERATIONS = 600_000
SALT_BYTES = 16

def hash_password(password, iterations=ITERATIONS):
    if not isinstance(password, str) or not password:
        raise ValueError("password must be a nonempty string")
    if not isinstance(iterations, int) or isinstance(iterations, bool) or iterations < 100_000:
        raise ValueError("iterations must be >= 100000")
    salt = secrets.token_bytes(SALT_BYTES)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    return "$".join((ALGORITHM, str(iterations),
                     base64.b64encode(salt).decode("ascii"),
                     base64.b64encode(digest).decode("ascii")))

def verify_password(password, encoded):
    try:
        algorithm, rounds, salt_text, digest_text = encoded.split("$")
        if algorithm != ALGORITHM: return False
        iterations = int(rounds)
        if not 100_000 <= iterations <= 10_000_000: return False
        salt = base64.b64decode(salt_text, validate=True)
        expected = base64.b64decode(digest_text, validate=True)
        if len(salt) != SALT_BYTES or len(expected) != 32: return False
        actual = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
        return hmac.compare_digest(actual, expected)
    except (ValueError, TypeError, AttributeError):
        return False

def needs_rehash(encoded, minimum_iterations=ITERATIONS):
    try:
        algorithm, rounds, _, _ = encoded.split("$")
        return algorithm != ALGORITHM or int(rounds) < minimum_iterations
    except (ValueError, TypeError, AttributeError):
        return True

if __name__ == "__main__":
    stored = hash_password("correct horse battery staple")
    print("Password verified:", verify_password("correct horse battery staple", stored))
    print("Incorrect password rejected:", not verify_password("incorrect", stored))
