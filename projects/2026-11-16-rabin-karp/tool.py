"""Rabin-Karp rolling hash; verifies candidates to avoid hash-collision false positives."""
def find_all(text, pattern, base=257, modulus=1_000_000_007):
    if not isinstance(text, str) or not isinstance(pattern, str):
        raise TypeError("text and pattern must be strings")
    if not isinstance(base, int) or not isinstance(modulus, int) or base <= 1 or modulus <= 1:
        raise ValueError("invalid hash parameters")
    m, n = len(pattern), len(text)
    if m == 0: return list(range(n + 1))
    if m > n: return []
    power = pow(base, m - 1, modulus)
    target = window = 0
    for i in range(m):
        target = (target * base + ord(pattern[i])) % modulus
        window = (window * base + ord(text[i])) % modulus
    matches = []
    for start in range(n - m + 1):
        if target == window and text[start:start + m] == pattern:
            matches.append(start)
        if start + m < n:
            window = ((window - ord(text[start]) * power) * base + ord(text[start + m])) % modulus
    return matches

if __name__ == "__main__":
    print(find_all("bananana", "ana"))
