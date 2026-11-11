import secrets

PRIME = 2**127 - 1

def split(secret, threshold, count, prime=PRIME):
    """Return (x,y) shares; each subset of threshold shares can reconstruct."""
    if not isinstance(prime,int) or prime < 3:
        raise ValueError("invalid field")
    if not all(isinstance(v,int) and not isinstance(v,bool) for v in (secret,threshold,count)):
        raise ValueError("integer inputs required")
    if not (0 <= secret < prime and 2 <= threshold <= count < prime):
        raise ValueError("invalid secret or threshold")
    coefficients = [secret] + [secrets.randbelow(prime) for _ in range(threshold-2)]
    coefficients.append(secrets.randbelow(prime-1)+1)
    return [(x, sum(c*pow(x,i,prime) for i,c in enumerate(coefficients)) % prime)
            for x in range(1,count+1)]

def recover(shares, prime=PRIME):
    if not shares or not isinstance(prime,int) or prime < 3:
        raise ValueError("invalid shares or field")
    xs = [x for x,y in shares]
    if len(xs) != len(set(xs)):
        raise ValueError("duplicate share coordinates")
    if any(not isinstance(x,int) or not isinstance(y,int) or not (1 <= x < prime and 0 <= y < prime) for x,y in shares):
        raise ValueError("share outside field")
    result = 0
    for i,(xi,yi) in enumerate(shares):
        numerator, denominator = 1,1
        for j,(xj,_) in enumerate(shares):
            if i != j:
                numerator = numerator*(-xj) % prime
                denominator = denominator*(xi-xj) % prime
        result = (result + yi*numerator*pow(denominator,-1,prime)) % prime
    return result

if __name__ == "__main__":
    shares = split(123456,3,5)
    print("Recovered:", recover(shares[1:4]))
