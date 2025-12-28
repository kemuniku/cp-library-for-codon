#Fenwick Tree for codon
class FenwickTree[T]:
    '''
    Fenwick Tree for codon
    配列Aの一点加算・区間和取得をO(logN)で行います。

    N: 配列Aの長さ
    '''
    N: int
    _step: int
    _node: list[T]
    __slots__ = ('N', '_step', '_node')
    def __init__(self, N: int) -> None:
        assert N >= 0
        self.N = N
        self._step = 1 << max(0, 63 - N.__ctlz__())  #1 << max(0, N.bit_length() - 1)
        self._node = [T(0) for _ in range(N + 1)]
    def _build_array(self) -> None:
        for h in range(1, 64 - self.N.__ctlz__()):
            back = step = 1 << h - 1
            for now in range(1 << h, self.N + 1, 1 << h):
                self._node[now] += self._node[back]
                back = now | step
    def build(self, A: generator[T]) -> None:
        '時間計算量 Θ(N)で、Fenwick Treeを配列Aで初期化します。'
        for i, Ai in enumerate(A, start = 1):
            self._node[i] = Ai
        self._build_array()
    def build(self, A: list[T]) -> None:
        '時間計算量 Θ(N)で、Fenwick Treeを配列Aで初期化します。'
        for i, Ai in enumerate(A, start = 1):
            self._node[i] = Ai
        self._build_array()
    def add(self, i: int, value: T) -> None:
        'A[i] += value の一点加算を行います。'
        assert 0 <= i < self.N
        i += 1
        while i <= self.N:
            self._node[i] += value
            i += i & - i
    def sum0(self, i: int) -> T:
        'sum(A[0: i + 1]) を返します。A[i]までを含みます。(sum(i)と同じ機能です)'
        assert i < self.N
        i += 1
        ans = T(0)
        while i > 0:
            ans += self._node[i]
            i ^= i & - i
        return ans
    def sum(self, i: int) -> T:
        'sum(A[0: i + 1]) を返します。A[i]までを含みます。(sum0(i)と同じ機能です)'
        return self.sum0(i)
    def sum(self, Lt: int, Rt: int) -> T:
        '0 <= Lt, Rt <= Nに対し、sum(A[Lt: Rt])を返します。A[Rt]は含みません。'
        assert 0 <= Lt and Rt <= self.N
        if Lt >= Rt:
            return T(0)
        ans = T(0)
        while Lt != Rt:
            if Lt > Rt:
                ans -= self._node[Lt]
                Lt ^= Lt & - Lt
            else:
                ans += self._node[Rt]
                Rt ^= Rt & - Rt
        return ans
    def bisect(self, value: T) -> int:
        '''
        配列Aのすべての要素が非負と仮定します。
        sum0(i) >= value となる最小のiを返します。存在しない場合、Nを返します。
        '''
        now, cnt, step = 0, T(0), self._step
        while step:
            nxt: int = now | step
            step >>= 1
            if nxt <= self.N and cnt + self._node[nxt] < value:
                cnt += self._node[nxt]
                now: int = nxt
        return now
