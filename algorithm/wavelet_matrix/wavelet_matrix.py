#Wavelet Matrix for codon, PyPy3
import heapq as _WM_heapq
class WaveletMatrix:
    '''
    Wavelet Matrix for codon, PyPy3
    非負整数列Aに対する検索を対数時間で行います。
    bit_countの実装上、すべての操作にO(log wordsize) (ただし wordsize = 64)の定数項がかかります。
    
    N = len(A), M = max(A) として
    構築: 時間 O(NlogM), 空間O(N)
    検索: 時間 O(logM) ～

    A: 読み込ませたい非負整数列
    '''
    _N: int
    _logM: int
    _size: int
    _C: list[int]
    _D: list[int]
    _zero: list[int]
    _one: list[int]
    _stack: list[int]
    __slots__ = ('_N', '_logM', '_size', '_C', '_D', '_zero', '_one', '_stack')
    def __init__(self, A: list[int]) -> None:
        assert len(A) == 0 or min(A) >= 0, f'Aに負の要素が含まれます。{min(A) = }'
        assert len(A) < 2 ** 29, f'len(A)が長すぎます。 {len(A) = }'
        self._N = N = len(A)
        maxA: int = 0 if len(A) == 0 else max(A)
        self._logM = logM = 0 if maxA == 0 else len(bin(maxA)) - 2
        self._size = size = -(- N >> 5)
        self._C = C = [0] * size * logM  #FIDをlogM個作成
        self._zero: list[int] = [0] * logM
        self._one: list[int] = [0] * logM
        self._stack: list[int] = [0] * ((logM + 1) << 1)
        D: list[int] = list(range(N))
        E: list[int] = [0] * N  #DとEをswapしながら上の桁から決定
        for k in range(logM - 1, -1, -1):
            offset: int = size * k
            zero = one = now = 0
            for b in range(offset, offset + size):
                C[b] = one << 32
                for c in range(32):
                    if now >= N:
                        break
                    v: int = A[D[now]] >> k & 1
                    if v == 0:
                        zero += 1
                    else:
                        one += 1
                        C[b] |= 1 << c
                    now += 1
            Lt, Rt = 0, zero
            for D_now in D:
                if A[D_now] >> k & 1 == 0:
                    E[Lt] = D_now
                    Lt += 1
                else:
                    E[Rt] = D_now
                    Rt += 1
            self._zero[k], self._one[k] = zero, one
            D, E = E, D
        self._D: list[int] = D
    #内部関数: FID
    def _FID_access(self, k: int, i: int) -> int:  #FID[k]に対し、B[i] >> k & 1
        #assert 0 <= k < self._logM and 0 <= i < self._N
        return self._C[self._size * k + (i >> 5)] >> (i & 31) & 1
    def _FID_rank(self, k: int, i: int, num: int) -> int:  #[0, i]のnumの個数
        #assert 0 <= k < self._logM and i < self._N and 0 <= num <= 1
        if i < 0:
            return 0
        Ci: int = self._C[self._size * k + (i >> 5)]
        n: int = Ci & ~(-1 << ((i & 31) + 1))  #one = (Ci >> 32) + n.bit_count()
        n: int = ( n & 0x55555555 ) + ( (n >> 1) & 0x55555555 )
        n: int = ( n & 0x33333333 ) + ( (n >> 2) & 0x33333333 )
        n: int = ( n & 0x0F0F0F0F ) + ( (n >> 4) & 0x0F0F0F0F )
        one: int = (Ci >> 32) + (n * 0x1010101 >> 24 & 63)
        return one if num == 1 else 1 + i - one
    def _FID_stable_sort(self, k: int, i: int) -> int:  #安定ソート後のiの位置
        #assert 0 <= k < self._logM and 0 <= i < self._N
        num: int = self._C[self._size * k + (i >> 5)] >> (i & 31) & 1  #access(i)
        if num == 0:
            return self._FID_rank(k, i - 1, 0)
        else:
            return self._FID_rank(k, i - 1, 1) + self._zero[k]
    def _FID_range_sort(self, k: int, Lt: int, Rt: int, num: int) -> tuple[int, int]:
        #[Lt, Rt)を安定ソートした後のnumの区間
        #assert 0 <= k < self._logM and 0 <= Lt <= Rt <= self._N and 0 <= num <= 1
        offset: int = 0 if num == 0 else self._zero[k]
        return (offset + self._FID_rank(k, Lt - 1, num),
                offset + self._FID_rank(k, Rt - 1, num))

    #基本機能: 計算量がO(logM)
    def access(self, i: int) -> int:
        'A[i]をO(logM)で取得します。'
        if i < 0:
            i += self._N
        assert 0 <= i < self._N
        ans: int = 0
        for k in range(self._logM - 1, -1, -1):
            b: int = self._FID_access(k, i)
            ans |= b << k
            i: int = self._FID_stable_sort(k, i)
        return ans
    def rank(self, Lt: int, Rt: int, value: int) -> int:
        'A[Lt, Rt)のvalueの出現回数をO(logM)で取得します。'
        assert 0 <= Lt <= Rt <= self._N
        if value < 0 or value >> self._logM >= 1:
            return 0
        for k in range(self._logM - 1, -1, -1):
            Lt, Rt = self._FID_range_sort(k, Lt, Rt, value >> k & 1)
        return Rt - Lt
    def select(self, cnt: int, value: int) -> int:
        '''
        0-indexedでcnt個目のvalueの添字をO(logM)で取得します。
        特に、cnt = 0 かつ value in A の時は A.index(value) と返り値が一致します。
        cnt >= A.count(value) の場合、Nを返します。
        '''
        if value < 0 or value >> self._logM >= 1:
            return self._N
        Lt, Rt = 0, self._N
        for k in range(self._logM - 1, -1, -1):
            Lt, Rt = self._FID_range_sort(k, Lt, Rt, value >> k & 1)
        if cnt >= Rt - Lt:
            return self._N
        else:
            return self._D[Lt + cnt]
    def kth_min(self, Lt: int, Rt: int, k: int) -> int:
        'sorted( A[Lt, Rt) )[k] : A[Lt, Rt)の小さい側からk番目の要素 をO(logM)で取得します。'
        assert 0 <= Lt <= Rt <= self._N
        assert 0 <= k < Rt - Lt, f'k is out of range: {Rt - Lt = }, {k = }'
        cnt: int = k  #内部的に添字をk → cntに変更
        ans: int = 0
        for k in range(self._logM - 1, -1, -1):
            Li: int = self._FID_rank(k, Lt - 1, 0)
            Ri: int = self._FID_rank(k, Rt - 1, 0)
            zero: int = Ri - Li
            if cnt < zero:
                Lt, Rt = Li, Ri
            else:  #Lt, Rt = self._FID_range_sort(k, Lt, Rt, 1)
                ans |= 1 << k
                cnt -= zero
                offset: int = self._zero[k]
                Lt, Rt = offset + (Lt - Li), offset + (Rt - Ri)
        return ans
    def range_freq(self, Lt: int, Rt: int, vL: int, vR: int) -> int:
        'A[Lt, Rt)に存在する、 vL <= Ai < vR を満たすAiの個数をO(logM)で取得します。'
        assert 0 <= Lt <= Rt <= self._N
        if not vL < vR:
            return 0
        ans: int = Rt - Lt
        stack: list[int] = self._stack
        if vL > 0:
            stack[0], stack[1] = 0, self._logM << 58 | Lt << 29 | Rt
            d: int = 2
            while d:
                c, x = stack[d - 2], stack[d - 1]
                d -= 2
                k, Li, Ri = x >> 58, x >> 29 & 0x1FFFFFFF, x & 0x1FFFFFFF
                if c + (1 << k) <= vL:
                    ans -= Ri - Li
                    continue
                k -= 1
                if k == -1:
                    break
                for b in (1, 0):
                    Lj, Rj = self._FID_range_sort(k, Li, Ri, b)
                    if Lj != Rj:
                        stack[d], stack[d + 1] = c | b << k, k << 58 | Lj << 29 | Rj
                        d += 2
        if vR <= ~(-1 << self._logM):
            stack[0], stack[1] = 0, self._logM << 58 | Lt << 29 | Rt
            d: int = 2
            while d:
                c, x = stack[d - 2], stack[d - 1]
                d -= 2
                k, Li, Ri = x >> 58, x >> 29 & 0x1FFFFFFF, x & 0x1FFFFFFF
                if c >= vR:  #変更点
                    ans -= Ri - Li
                    continue
                k -= 1
                if k == -1:
                    break
                for b in (0, 1):  #変更点
                    Lj, Rj = self._FID_range_sort(k, Li, Ri, b)
                    if Lj != Rj:
                        stack[d], stack[d + 1] = c | b << k, k << 58 | Lj << 29 | Rj
                        d += 2   
        return ans
    def prev_value(self, Lt: int, Rt: int, value: int) -> int:
        '''
        A[Lt, Rt)のうち、valueより真に小さい最大値をO(logM)で取得します。
        そのような値が存在しない場合、-1を返します。
        '''
        assert 0 <= Lt <= Rt <= self._N
        if Lt == Rt or value <= 0:
            return -1
        stack: list[int] = self._stack
        stack[0], stack[1] = 0, self._logM << 58 | Lt << 29 | Rt
        d: int = 2
        while d:
            c, x = stack[d - 2], stack[d - 1]
            d -= 2
            k, Li, Ri = x >> 58, x >> 29 & 0x1FFFFFFF, x & 0x1FFFFFFF
            if c >= value:  #変更点
                continue
            k -= 1
            if k == -1:
                return c
            for b in (0, 1):  #変更点
                Lj, Rj = self._FID_range_sort(k, Li, Ri, b)
                if Lj != Rj:
                    stack[d], stack[d + 1] = c | b << k, k << 58 | Lj << 29 | Rj
                    d += 2
        else:
            return -1
    def next_value(self, Lt: int, Rt: int, value: int) -> int:
        '''
        A[Lt, Rt)のうち、valueより真に大きい最小値をO(logM)で取得します。
        そのような値が存在しない場合、-1を返します。
        '''
        assert 0 <= Lt <= Rt <= self._N
        if Lt == Rt or value >= ~(-1 << self._logM):
            return -1
        value += 1
        stack: list[int] = self._stack
        stack[0], stack[1] = 0, self._logM << 58 | Lt << 29 | Rt
        d: int = 2
        while d:
            c, x = stack[d - 2], stack[d - 1]
            d -= 2
            k, Li, Ri = x >> 58, x >> 29 & 0x1FFFFFFF, x & 0x1FFFFFFF
            if c + (1 << k) <= value:
                continue
            k -= 1
            if k == -1:
                return c
            for b in (1, 0):
                Lj, Rj = self._FID_range_sort(k, Li, Ri, b)
                if Lj != Rj:
                    stack[d], stack[d + 1] = c | b << k, k << 58 | Lj << 29 | Rj
                    d += 2
        else:
            return -1
        
    #基本機能: 計算量がO(logM)でないもの
    def topk_mode(self, Lt: int, Rt: int, k: int) -> list[tuple[int, int]]:
        '''
        A[Lt, Rt)の頻度を数え、E: [(値, 個数) のリスト]を作成します。
        その後 個数の降順・同率なら値の昇順 にEをソートし、E[:cnt]を返します。
        計算量は O( cnt * logNlogM ) です。返り値のタプルの順序は(値, 個数)です。
        '''
        assert 0 <= Lt <= Rt <= self._N
        ans: list[tuple[int, int]] = []
        cnt: int = k  #内部的に添字をk → cntに変更
        if Lt == Rt or cnt <= 0:
            return ans
        Q: list[tuple[int, int, int]] = [
            ( ~( (Rt - Lt) << 32 | self._logM), 0, Lt << 32 | Rt )]
        while Q and len(ans) < cnt:
            x, y, z = _WM_heapq.heappop(Q)
            w, k = (~ x) >> 32, ((~ x) & 0xFFFFFFFF) - 1
            Li, Ri = z >> 32, z & 0xFFFFFFFF
            assert Li <= Ri and 0 <= w == Ri - Li and k >= -1
            if k == -1:
                ans.append((y, Ri - Li))
                continue
            for b in range(2):
                Lj, Rj = self._FID_range_sort(k, Li, Ri, b)
                if Rj > Lj:
                    _WM_heapq.heappush(
                        Q, (~ ((Rj - Lj) << 32 | k), y | b << k, Lj << 32 | Rj ))
        return ans
    def intersect(self, L1: int, R1: int, L2: int, R2: int) -> list[tuple[int, int]]:
        '''
        A[L1, R1) と A[L2, R2) の共通要素を取り出し、(値, 個数) の昇順で返します。
        計算量は O( (R - L)logM )です。
        '''
        assert 0 <= L1 <= R1 <= self._N and 0 <= L2 <= R2 <= self._N
        ans: list[tuple[int, int]] = []
        if L1 == R1 or L2 == R2:
            return ans
        stack: list[int] = self._stack
        while len(stack) < (self._logM + 1) * 3:
            stack.append(0)
        stack[0], stack[1], stack[2] = 0, self._logM << 58 | L1 << 29 | R1, L2 << 29 | R2
        d: int = 3
        while d:
            c, y, z = stack[d - 3], stack[d - 2], stack[d - 1]
            d -= 3
            k, L1i, R1i = (y >> 58) - 1, y >> 29 & 0x1FFFFFFF, y & 0x1FFFFFFF
            L2i, R2i = z >> 29 & 0x1FFFFFFF, z & 0x1FFFFFFF
            if k == -1:
                ans.append((c, min(R1i - L1i, R2i - L2i)))
                continue
            for b in (1, 0):
                L1j, R1j = self._FID_range_sort(k, L1i, R1i, b)
                L2j, R2j = self._FID_range_sort(k, L2i, R2i, b)
                if L1j != R1j and L2j != R2j:
                    stack[d] = c | b << k
                    stack[d + 1] = k << 58 | L1j << 29 | R1j
                    stack[d + 2] = L2j << 29 | R2j
                    d += 3
        return ans
