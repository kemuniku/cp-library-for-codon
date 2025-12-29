#Rolling Hash
#Reference: https://qiita.com/keymoon/items/11fac5627672a6d6a9f6
from random import randrange as _RollingHash_randrange
_RollingHash_base = _RollingHash_randrange(~ (- 1 << 61))
class RollingHash:
    '''
    Rolling Hash for codon, PyPy3
    法mod = 2 ** 61 - 1の下で、文字列のハッシュを計算します。

    base: 基数 指定がない場合、[0, 2 ** 61 - 1)から乱択
    '''
    base: int
    _builded: bool
    _B: list[int]
    _H: list[int]
    __slots__ = ('base', '_builded', '_B', '_H')
    def __init__(self, base: int = -1) -> None:
        self.base: int = base if 0 <= base < 0x1FFFFFFFFFFFFFFF else _RollingHash_base
        self._B: list[int] = [1]
    #内部関数
    def _mul(self, x: int, y: int) -> int:
        div_x, mod_x = x >> 31, x & 0x7FFFFFFF
        div_y, mod_y = y >> 31, y & 0x7FFFFFFF
        m: int = div_x * mod_y + div_y * mod_x
        ans: int = 2 * div_x * div_y + (m >> 30) + ((m & 0x3FFFFFFF) << 31) + mod_x * mod_y
        if ans < 0x1FFFFFFFFFFFFFFF:
            return ans
        div_ans, mod_ans = ans >> 61, ans & 0x1FFFFFFFFFFFFFFF
        ans2: int = div_ans + mod_ans
        return ans2 if ans2 < 0x1FFFFFFFFFFFFFFF else ans2 - 0x1FFFFFFFFFFFFFFF
    def _build_B(self, x: int) -> None:
        if x >= len(self._B):
            if (x + 1) / len(self._B) < 1.1:
                for _ in range(x + 1 - len(self._B)):
                    self._B.append(self._mul(self._B[-1], self.base))
            else:
                new_B: list[int] = [1] * (x + 1)
                for i, Bi in enumerate(self._B):
                    new_B[i] = Bi
                for i in range(len(self._B), x + 1):
                    new_B[i] = self._mul(new_B[i - 1], self.base)
                self._B = new_B
    def _RH(self, A, k: int) -> list[int]:
        ans: list[int] = [0] * (len(A) - k + 1)
        cnt: int = 0
        pow_base: int = 1
        for i in range(k):
            Ai: int = ord(A[i]) if isinstance(A[i], str) else A[i]
            cnt: int = self._mul(cnt, self.base) + Ai
            if cnt >= 0x1FFFFFFFFFFFFFFF:
                cnt -= 0x1FFFFFFFFFFFFFFF
            pow_base: int = self._mul(pow_base, self.base)
        ans[0] = cnt
        for Li in range(len(A) - k):
            A_back: int = ord(A[Li    ]) if isinstance(A[Li    ], str) else A[Li    ]
            A_now:  int = ord(A[Li + k]) if isinstance(A[Li + k], str) else A[Li + k]
            cnt: int = self._mul(cnt, self.base) + A_now - self._mul(A_back, pow_base)
            if cnt >= 0x1FFFFFFFFFFFFFFF:
                cnt -= 0x1FFFFFFFFFFFFFFF
            if cnt < 0:
                cnt += 0x1FFFFFFFFFFFFFFF
            ans[Li + 1] = cnt
        return ans
    def _build_array(self, A) -> None:
        self._builded: bool = True
        self._H: list[int] = [0] * (len(A) + 1)
        self._build_B(len(A))
        for i, Ai in enumerate(A):
            Bi: int = ord(Ai) if isinstance(Ai, str) else Ai
            self._H[i + 1] = self._mul(self._H[i], self.base) + Bi
            if self._H[i + 1] >= 0x1FFFFFFFFFFFFFFF:
                self._H[i + 1] -= 0x1FFFFFFFFFFFFFFF

    #基本機能
    def hash(self, A) -> int:
        '現在の基数を用い、Aのハッシュ値を計算します。'
        ans: int = 0
        for Ai in A:
            Bi: int = ord(Ai) if isinstance(Ai, str) else Ai
            ans: int = self._mul(ans, self.base) + Bi
            if ans >= 0x1FFFFFFFFFFFFFFF:
                ans -= 0x1FFFFFFFFFFFFFFF
        return ans
    def rolling_hash(self, A, k: int) -> list[int]:
        '0 <= i < len(A) - k + 1 において、A[i: i + k]のハッシュ値を計算します。'
        assert 0 <= k <= len(A)
        return self._RH(A, k)
    def build(self, A) -> None:
        'Aのハッシュの前計算を行います。'
        self._build_array(A)
    def fold(self, Lt: int, Rt: int) -> int:
        'build(A)によるAの前計算の下、A[Lt: Rt]のハッシュをO(1)で取得します。'
        assert self._builded == True
        assert 0 <= Lt and Rt < len(self._H)
        if Lt >= Rt:
            return 0
        ans: int = self._H[Rt] - self._mul(self._H[Lt], self._B[Rt - Lt])
        return ans if ans >= 0 else ans + 0x1FFFFFFFFFFFFFFF
