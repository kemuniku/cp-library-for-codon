#dynamic Li Chao Tree
class Li_Chao_Tree:
    '''
    dynamic Li Chao Tree for codon, PyPy3
    線分追加・一点の最小値計算をO(log^2 X)で行います。
    異常値を検出した場合、self.inf(初期値は 2 ** 63 - 1)を返します。

    min_x, max_x: 線分追加・最小値計算を行うxの区間の最小値・最大値
                  すべてのxの入力は 閉区間[min_x, max_x] に収まることを要求します。
    '''
    inf: int
    _L: list[int]
    _C: list[int]
    _X: list[int]
    __slots__ = ('inf', '_L', '_C', '_X')
    def __init__(self, min_x: int, max_x: int) -> None:
        assert min_x <= max_x, f'xの大小が逆転しています。{min_x = }, {max_x = }'
        self.inf = ~(-1 << 63)
        self._L = [self.inf, self.inf]  #ノードiの線分(a, b) 線分不在ならinf
        self._C = [0x7FFFFFFF7FFFFFFF]  #ノードiの(左子 << 32 | 右子)
        self._X = [min_x, max_x]        #ノードiの左端, 右端
    #内部関数
    def _get_child(self, i: int, access_left: bool) -> int:  #子を返す 必要なら作成
        child: int = self._C[i] >> 32 if access_left else self._C[i] & 0x7FFFFFFF
        if child != 0x7FFFFFFF:
            return child
        Lx, Rx = self._X[i << 1], self._X[i << 1 | 1]
        assert Lx < Rx  #Lx == Rx も不可
        if access_left:
            self._C[i] = len(self._C) << 32 | self._C[i] & 0x7FFFFFFF
            self._X.append(Lx)
            self._X.append((Lx & Rx) + ((Lx ^ Rx) >> 1))  #(Lx + Rx) >> 1
        else:
            self._C[i] = self._C[i] >> 32 << 32 | len(self._C)
            self._X.append((Lx & Rx) + ((Lx ^ Rx) >> 1) + 1)  #((Lx + Rx) >> 1) + 1
            self._X.append(Rx)
        self._C.append(0x7FFFFFFF7FFFFFFF)
        self._L.append(self.inf)
        self._L.append(self.inf)
        return len(self._C) - 1
    def _add_lineseg(self, i: int, a: int, b: int) -> None:  #node iにf = ax + bを追加
        while True:
            c, d = self._L[i << 1], self._L[i << 1 | 1]
            if c == d == self.inf:
                self._L[i << 1], self._L[i << 1 | 1] = a, b
                return
            Lx, Rx = self._X[i << 1], self._X[i << 1 | 1]
            Mx = (Lx & Rx) + ((Lx ^ Rx) >> 1)  #(Lx + Rx) >> 1
            islower_L: bool = (a * Lx + b) < (c * Lx + d)
            islower_R: bool = (a * Rx + b) < (c * Rx + d)
            if islower_L == islower_R:
                if islower_L == True:
                    self._L[i << 1], self._L[i << 1 | 1] = a, b
                return
            islower_M: bool = (a * Mx + b) < (c * Mx + d)
            if islower_M == True:  #ax + b と cx + dをswap
                self._L[i << 1], self._L[i << 1 | 1] = a, b
                a, b = c, d
            i: int = self._get_child(i, islower_L != islower_M)
    
    #基本機能
    def add_line(self, a: int, b: int, xL: int, xR: int) -> None:
        '''
        閉区間[xL, xR]に線分 y = ax + b を追加します。
        直線追加にしたい場合、xL <= min_x, xR >= max_x を満たすxL, xRを指定してください。
        
        計算量: 直線追加 O(logX), 線分追加 O(log^2 X)
        '''
        if xL < self._X[0]:
            xL = self._X[0]
        if xR > self._X[1]:
            xR = self._X[1]
        assert xL <= xR, f'線分追加の範囲が逆転しています。{xL = }, {xR = }'
        assert not a == b == self.inf, 'y = ax + bのうち、(a, b)の両方がinfです。'
        stack: list[int] = [0]
        while stack:
            i: int = stack.pop()
            Lt, Rt = self._X[i << 1], self._X[i << 1 | 1]
            if xL <= Lt and Rt <= xR:
                self._add_lineseg(i, a, b)
                continue
            Md = (Lt & Rt) + ((Lt ^ Rt) >> 1)
            if xL <= Md:  #左子を探索
                stack.append(self._get_child(i, True))
            if Md < xR:  #右子を探索
                stack.append(self._get_child(i, False))
    def fold(self, x: int) -> int:
        '座標xにおける、線分の最小値を求めます。線分がない場合、self.infを返します。'
        assert self._X[0] <= x <= self._X[1], (
            f'xが範囲外です。{self._X[0] = }, {self._X[1] = }, {x = }')
        i: int = 0
        ans = self.inf
        while i != 0x7FFFFFFF:
            if not self._L[i << 1] == self._L[i << 1 | 1] == self.inf:
                ans = min(ans, self._L[i << 1] * x + self._L[i << 1 | 1])
            Lt, Rt = self._X[i << 1], self._X[i << 1 | 1]
            Md = (Lt & Rt) + ((Lt ^ Rt) >> 1)
            i = self._C[i] >> 32 if x <= Md else self._C[i] & 0x7FFFFFFF
        return ans
