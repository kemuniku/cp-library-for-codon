#floor(√n) for codon
def isqrt(n: int) -> int:
    'floor(√n): m ** 2 <= n < (m + 1) ** 2 を満たす非負整数mを求めます。'
    assert n >= 0
    if n >= 3037000499 ** 2:  #floor( √(2 ** 63 - 1) ) = 3037000499
       return 3037000499
    m: int = max(0, int(float(n).sqrt()))  #int(n ** 0.5)
    m2: int = m * m
    while m2 < n:
        m2 += m << 1 | 1
        m += 1
    while m2 > n:
        m -= 1
        m2 -= m << 1 | 1
    return m
