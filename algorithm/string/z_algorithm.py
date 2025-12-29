#Z algorithm
#Reference: https://tjkendev.github.io/procon-library/python/string/z-algorithm.html
def Z_algorithm(A) -> list[int]:
    '''
    Z algorithm for codon, PyPy3
    すべての0 <= i < N = len(A) に対し、AとA[i:]の最長共通接頭辞をO(N)で求めます。

    A: 読み込ませる文字列(または配列)
    '''
    N: int = len(A)
    B: list[int] = [0] * N
    if N > 0:
        B[0] = N
        Rt: int = 0
        same: int = 0
        ok: int = 0
        for i in range(1, N):
            if Rt:
                Rt -= 1
            same += 1
            if B[same] < Rt:
                B[i] = B[same]
                continue
            while i + Rt < N and A[Rt] == A[i + Rt]:
                Rt += 1
            B[i] = Rt
            same: int = 0
    return B
