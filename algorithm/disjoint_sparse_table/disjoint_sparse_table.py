#Disjoint Sparse Table
class DisjointSparseTable[T, F]:
    '''
    Disjoint Sparse Table for codon
    時間・空間Θ(NlogN)の前計算の下、O(1)回の演算で区間積を取得します。

    op: 合成関数  op(node_Lt: T, node_Rt: T) -> node_new: T
    A: 読み込ませる配列
    '''
    N: int
    _op: F
    _node: list[T]
    __slots__ = ('N', '_op', '_node')
    def __init__(self, op: F, A: list[T]) -> None:
        self.N = N = len(A)
        logN: int = len(bin(N - 1)) - 2 if N >= 2 else N  #(N - 1).bit_length()
        self._op = op
        self._node = node = A * logN
        for h in range(logN):
            offset: int = h * N
            b = diff = 1 << h
            step: int = 2 << h
            while b < N:
                node[b + offset] = back = A[b]
                i: int = b + 1
                Rt: int = min(b + diff, N)
                while i < Rt:
                    node[i + offset] = back = self._op(back, A[i])
                    i += 1
                b += step
            b: int = diff - 1
            while b < N:
                node[b + offset] = back = A[b]
                i: int = b - 1
                Lt: int = b - diff
                while Lt < i:
                    node[i + offset] = back = self._op(A[i], back)
                    i -= 1
                b += step
    def fold(self, Lt: int, Rt: int) -> T:
        '半開区間積A[Lt, Rt)を取得します。制約で 0 <= Lt < Rt <= Nを要求します。'
        assert 0 <= Lt < Rt <= self.N
        Rt -= 1
        if Lt == Rt:
            return self._node[Lt]
        h: int = 63 - (Lt ^ Rt).__ctlz__()  #h ← (Lt ^ Rt).bit_length() - 1
        return self._op( self._node[h * self.N + Lt], self._node[h * self.N + Rt] )
