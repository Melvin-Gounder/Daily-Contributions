import base64
import hashlib
import hmac
import struct
import time

def hotp(secret, counter, digits=6, digest="sha1"):
    if not isinstance(secret,bytes) or not secret:
        raise ValueError("secret must be nonempty bytes")
    if not isinstance(counter,int) or not (0 <= counter < 2**64):
        raise ValueError("counter out of range")
    if digits not in (6,7,8):
        raise ValueError("digits must be 6, 7, or 8")
    if digest not in ("sha1","sha256","sha512"):
        raise ValueError("unsupported digest")
    mac=hmac.new(secret,struct.pack(">Q",counter),getattr(hashlib,digest)).digest()
    offset=mac[-1]&15
    number=struct.unpack(">I",mac[offset:offset+4])[0]&0x7fffffff
    return str(number % 10**digits).zfill(digits)

def totp(secret, at=None, step=30, t0=0, digits=6, digest="sha1"):
    if not isinstance(step,int) or step <= 0:
        raise ValueError("step must be positive")
    now=time.time() if at is None else at
    counter=int((now-t0)//step)
    return hotp(secret,counter,digits,digest)

def verify(secret, code, at=None, window=1, step=30, digits=6, digest="sha1"):
    if not isinstance(window,int) or not (0 <= window <= 10):
        raise ValueError("window must be between 0 and 10")
    if not isinstance(code,str) or len(code)!=digits or not code.isascii() or not code.isdecimal():
        return False
    now=time.time() if at is None else at
    if step <= 0: raise ValueError("step must be positive")
    counter=int(now//step)
    matched=False
    for candidate in range(max(0,counter-window),counter+window+1):
        matched=hmac.compare_digest(hotp(secret,candidate,digits,digest),code) or matched
    return matched

def generate_secret(nbytes=20):
    import secrets
    if nbytes < 16: raise ValueError("use at least 16 bytes")
    return base64.b32encode(secrets.token_bytes(nbytes)).decode("ascii").rstrip("=")

if __name__ == "__main__":
    secret=generate_secret()
    print("Demo secret (do not use in production):",secret)
    print("Current code:",totp(base64.b32decode(secret+"="*((-len(secret))%8))))
