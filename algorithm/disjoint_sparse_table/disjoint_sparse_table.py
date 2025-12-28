#disjoint Sparse Table for codon
class disjointSparseTable[Te, Tf]:
    '''
    disjoint Sparse Table for codon
    Θ(NlogN)回の前計算の下、配列の区間積をO(1)回の演算で取得します。

    A: 読み込ませる配列
    identity_e: 単位元 要素の型はAの要素と同じにしてください
    node_f: 合成関数 f(node_Lt: Te, node_Rt: Te) -> node_new: Te
    '''
    N: int
    _e: Te
    _f: Tf
    _node: list[Te]
    __slots__ = ('N', '_e', '_f', '_node')
    def __init__(self, A: list[Te], identity_e: Te, node_f: Tf) -> None:
        self.N = N = len(A)
        logN: int = max(1, len(bin(N - 1)) - 2)  #(N - 1).bit_length()
        self._e, self._f = identity_e, node_f
        self._node = node = [self._e for _ in range(N * logN)]
        for h in range(logN):
            offset: int = h * N
            for i, Ai in enumerate(A, start = offset):
                node[i] = Ai
            b = diff = 1 << h
            step: int = 2 << h
            while b < N:
                node[b + offset] = back = A[b]
                i: int = b + 1
                Rt: int = min(b + diff, N)
                while i < Rt:
                    node[i + offset] = back = self._f(back, A[i])
                    i += 1
                b += step
            b: int = diff - 1
            while b < N:
                node[b + offset] = back = A[b]
                i: int = b - 1
                Lt: int = b - diff
                while Lt < i:
                    node[i + offset] = back = self._f(A[i], back)
                    i -= 1
                b += step
    def fold(self, Lt: int, Rt: int) -> Te:
        '半開区間積A[Lt, Rt)を取得します。Lt == Rtの場合、単位元eを返します。'
        assert 0 <= Lt <= Rt <= self.N
        if Lt == Rt:
            return self._e
        Rt -= 1
        if Lt == Rt:
            return self._node[Lt]
        h: int = 63 - (Lt ^ Rt).__ctlz__()  #h ← (Lt ^ Rt).bit_length() - 1
        return self._f( self._node[h * self.N + Lt], self._node[h * self.N + Rt] )
