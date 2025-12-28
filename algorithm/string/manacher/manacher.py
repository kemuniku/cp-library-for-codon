#manacher algorithm
#Reference: https://tjkendev.github.io/procon-library/python/string/manacher.html
def manacher(S) -> list[int]:
    '''
    manacher algorithm for codon, PyPy3
    文字列あるいは配列Sに対して、Sの最長回文長を列挙します。
    A[2 * i]: S[i]を中心とする奇数長の最大回文長(1以上の奇数)
    A[2 * i + 1]: S[i]とS[i + 1]の間を中心とする偶数長の最大回文長(0以上の偶数)
    '''
    N: int = 2 * len(S) - 1
    A: list[int] = [0] * N
    i = j = 0
    while i < N:
        while j <= i < N - j and ((i + j) & 1 or S[(i - j) >> 1] == S[(i + j) >> 1]):
            j += 1
        A[i] = j
        k: int = 1
        while j - A[i - k] > k <= i < N - k:
            A[i + k] = A[i - k]
            k += 1
        i += k
        j -= k
    for i in range(N):
        if i & 1 == A[i] & 1:
            A[i] -= 1
    return A
