#中国剰余定理
def CRT(R: list[int], M: list[int]) -> tuple[int, int]:
    '''
    n ≡ R[i] mod M[i] をすべて満たす非負整数n < lcm(M)を求め、(n, lcm(M))を返します。
    答えがない場合は(0, 0)を、len(R) == len(M) == 0の場合は(0, 1)を返します。
    制約: len(R) == len(M), 0 < M[i], lcm(M) < 2 ** 63
    '''
    assert len(R) == len(M)
    assert all(0 < Mi for Mi in M)
    R1, M1 = 0, 1
    for R2, M2 in zip(R, M):
        R2 %= M2
        if R2 < 0:
            R2 += M2
        if M1 > M2:
            R1, M1, R2, M2 = R2, M2, R1, M1
        f, g, i, j = M1, M2, 1, 0  #g: gcd(M1, M2),  i: invmod(M1 // g, M2 // g)
        while f:
            h = g // f
            f, g, i, j = g - h * f, f, j, i - h * j
        p, q = R1 - R2, M1 // g
        r, s = p // g, p % g
        if s:
            return (0, 0)
        R1, M1 = r * i % q * M2 + R2, M2 * q  #assert abs(r * i) < M2 * q
        if R1 < 0:
            R1 += M1
    return (R1, M1)
