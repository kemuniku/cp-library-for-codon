#Lazy Segment Tree for codon
#Reference: 大槻兼資ほか, 『アルゴリズム実技検定 公式テキスト［上級］～［エキスパート］編』
class LazySegTree[Tnode, Tlazy, Fop, Fmap, Fcomp]:
    '''
    Lazy Segment Tree for codon
    配列の区間作用・区間積取得を行います。

    op: 二項演算の関数  op(node_Lt: Tnode, node_Rt: Tnode) -> node_new: Tnode
    e: opの単位元  型はTnode: 配列の要素と同じ型
    mapping: 遅延を反映する関数  mapping(lazy: Tlazy, node: Tnode) -> node_new: Tnode
    composition:  遅延の合成関数  comp(lazy_now: Tlazy, lazy_prev: Tlazy) -> lazy_new: Tlazy
    id_: 遅延操作の単位元 型はTlazy
    N: 配列の長さ  第6引数にN: intを渡す場合、配列はopの単位元eで初期化します
    A: 初期化に用いる長さNの配列
    '''
    _N: int
    _logN: int
    _size: int
    _en: Tnode
    _eL: Tlazy
    _fn: Fop
    _fL: Fcomp
    _fmap: Fmap
    _node: list[Tnode]
    _lazy: list[Tlazy]
    __slots__ = ('_N', '_logN', '_size', '_en', '_eL',
                 '_fn', '_fL', '_fmap', '_node', '_lazy')
    def __init__(self, op: Fop, e: Tnode, mapping: Fmap,
                 composition: Fcomp, id_: Tlazy, N: int) -> None:
        self._N = N
        self._logN = 64 - max(0, N - 1).__ctlz__()  #max(0, N - 1).bit_length()
        self._size = 1 << self._logN
        self._en: Tnode = e
        self._eL: Tlazy = id_
        self._fn: Fop = op
        self._fL: Fcomp = composition
        self._fmap: Fmap = mapping
        self._node = [self._en for _ in range(self._size << 1)]
        self._lazy = [self._eL for _ in range(self._size << 1)]
    def __init__(self, op: Fop, e: Tnode, mapping: Fmap,
                 composition: Fcomp, id_: Tlazy, A: generator[Tnode]) -> None:
        self.__init__(op, e, mapping, composition, id_, list(A))
    def __init__(self, op: Fop, e: Tnode, mapping: Fmap,
                 composition: Fcomp, id_: Tlazy, A: list[Tnode]) -> None:
        self.__init__(op, e, mapping, composition, id_, len(A))
        for i, Ai in enumerate(A, start = self._size):
            self._node[i] = Ai
        for i in range(self._size - 1 , 0, -1):
            self._node[i] = self._fn(self._node[i << 1], self._node[i << 1 | 1])
    #内部関数
    def _push(self, i: int) -> None:
        if i < self._size and (L := self._lazy[i]) != self._eL:
            self._lazy[i << 1    ] = self._fL(L, self._lazy[i << 1    ])
            self._lazy[i << 1 | 1] = self._fL(L, self._lazy[i << 1 | 1])
            self._node[i], self._lazy[i] = self._fmap(L, self._node[i]), self._eL
    def _propagate(self, i: int) -> None:
        assert self._size <= i < self._size + self._N
        for h in range(self._logN, 0, -1):
            j = i >> h
            if (L := self._lazy[j]) != self._eL:
                self._lazy[j << 1    ] = self._fL(L, self._lazy[j << 1    ])
                self._lazy[j << 1 | 1] = self._fL(L, self._lazy[j << 1 | 1])
                self._node[j], self._lazy[j] = self._fmap(L, self._node[j]), self._eL
    def _update(self, i: int) -> None:
        assert self._size <= i < self._size + self._N
        while (i := i >> 1):
            self._node[i] = self._fn(
                self._fmap( self._lazy[i << 1    ], self._node[i << 1    ] ),
                self._fmap( self._lazy[i << 1 | 1], self._node[i << 1 | 1] ))

    #基本機能: 更新・取得
    def set(self, i: int, node_value: Tnode) -> None:
        'A[i]の値をnode_valueに変更します。'
        assert 0 <= i < self._N
        i |= self._size
        self._propagate(i)
        self._node[i], self._lazy[i] = node_value, self._eL
        self._update(i)
    def get(self, i: int) -> Tnode:
        '時間計算量O(logN)で、A[i]の値を取得します。'
        assert 0 <= i < self._N
        i |= self._size
        self._propagate(i)
        if (L := self._lazy[i]) != self._eL:
            self._node[i] = self._fmap(L, self._node[i])
            self._lazy[i] = self._eL
        return self._node[i]
    def prod(self, Lt: int, Rt: int) -> Tnode:
        '''
        半開区間A[Lt, Rt)の積を返します。A[Rt]は含みません。
        Lt == Rt の場合、opの単位元eを返します。
        '''
        assert 0 <= Lt <= Rt <= self._N
        if Lt == Rt:
            return self._en
        self._propagate(Lt | self._size)
        self._propagate((Rt - 1) | self._size)
        Li, Ri = Lt | self._size, Rt + self._size
        vL, vR = self._en, self._en
        while Li < Ri:
            if Li & 1:
                vL = self._fn(vL, self._fmap(self._lazy[Li], self._node[Li]))
                Li += 1
            if Ri & 1:
                Ri -= 1
                vR = self._fn(self._fmap(self._lazy[Ri], self._node[Ri]), vR)
            Li >>= 1
            Ri >>= 1
        return self._fn(vL, vR)
    def all_prod(self) -> Tnode:
        '時間計算量O(1)で、A[0, N)の全区間積を取得します。'
        if self._N == 0:
            return self._en
        elif (L := self._lazy[1]) != self._eL:
            if self._N != 1:
                self._lazy[2] = self._fL(L, self._lazy[2])
                self._lazy[3] = self._fL(L, self._lazy[3])
            self._node[1], self._lazy[1] = self._fmap(L, self._node[1]), self._eL
        return self._node[1]
    def apply(self, i: int, lazy_op: Tlazy) -> None:
        '''
        A[i]に遅延lazy_opを作用します。
        区間作用を行う場合、3引数版のapply(Lt, Rt, lazy_op)を使用してください。
        '''
        assert 0 <= i < self._N
        i |= self._size
        self._propagate(i)
        self._lazy[i] = self._fL(lazy_op, self._lazy[i])
        self._update(i)
    def apply(self, Lt: int, Rt: int, lazy_op: Tlazy) -> None:
        '''
        半開区間A[Lt, Rt)に遅延lazy_opを作用します。A[Rt]は含みません。
        一点作用の場合、2引数版のapply(i, lazy_op)のほうが定数倍に優れます。
        '''
        assert 0 <= Lt <= Rt <= self._N
        if Lt == Rt:
            return
        self._propagate(Lt | self._size)
        self._propagate((Rt - 1) | self._size)
        Li, Ri = Lt | self._size, Rt + self._size
        while Li < Ri:
            if Li & 1:
                self._lazy[Li] = self._fL(lazy_op, self._lazy[Li])
                Li += 1
            if Ri & 1:
                Ri -= 1
                self._lazy[Ri] = self._fL(lazy_op, self._lazy[Ri])
            Li >>= 1
            Ri >>= 1
        self._update(Lt | self._size)
        self._update((Rt - 1) | self._size)
    #セグメント木内の二分探索
    def max_right(self, Lt: int, judge: Function[tuple[Tnode], bool]) -> int:
        '''
        区間積の単調性を仮定します。
        半開区間の左端Lt(0 <= Lt <= N)と、判定関数 judge(区間積: Tnode) -> bool を渡します。
        ただし、 judge(opの単位元e) == True を要求します。
        judge(半開区間積A[Lt, Rt)) == True を満たす最大のRt(Lt <= Rt <= N)を返します。
        '''
        assert 0 <= Lt <= self._N
        if Lt == self._N:
            return self._N
        i, cnt = Lt | self._size, self._en
        self._propagate(i)
        while True:
            i >>= i.__cttz__()  #i //= i & - i: iの後置0(trailing zeros)を削除
            t = self._fn(cnt, self._fmap(self._lazy[i], self._node[i]))
            if judge(t):
                cnt = t
                i += 1
                if i & (i - 1) == 0:
                    return self._N
            else:
                break
        while i < self._size:
            self._push(i)
            i <<= 1
            t = self._fn(cnt, self._fmap(self._lazy[i], self._node[i]))
            if judge(t):
                cnt = t
                i ^= 1
        return i ^ self._size
    def min_left(self, Rt: int, judge: Function[tuple[Tnode], bool]) -> int:
        '''
        区間積の単調性を仮定します。
        半開区間の右端Rt(0 <= Rt <= N)と、判定関数 judge(区間積: Tnode) -> bool を渡します。
        ただし、 judge(opの単位元e) == True を要求します。
        judge(半開区間積A[Lt, Rt)) == True を満たす最小のLt(0 <= Lt <= Rt)を返します。
        '''
        assert 0 <= Rt <= self._N
        if Rt == 0:
            return 0
        i, cnt = (Rt - 1) | self._size, self._en
        self._propagate(i)
        if Rt == self._N:
            cnt = self._fmap(self._lazy[i], self._node[i])
            if judge(cnt):
                i -= 1
                if self._N == 1:
                    return 0
            else:
                return self._N
        while True:
            i >>= (i + 1).__cttz__()  #i //= (~ i) & - (~ i): iの後置1を削除
            t = self._fn(self._fmap(self._lazy[i], self._node[i]), cnt)
            if judge(t):
                cnt = t
                i -= 1
                if i & (i + 1) == 0:
                    return 0
            else:
                break
        while i < self._size:
            self._push(i)
            i = i << 1 | 1
            t = self._fn(self._fmap(self._lazy[i], self._node[i]), cnt)
            if judge(t):
                cnt = t
                i ^= 1
        return (i ^ self._size) + 1
