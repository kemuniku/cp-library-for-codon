#行列累乗 for codon, PyPy3
class matrix_power:
    '''
    行列累乗 for codon, PyPy3
    法MODの下、行列計算を行います。
    行列は2次元リストとして渡してください。
    返り値は新しい2次元リストで、全成分が0以上MOD未満を満たします。

    MOD: 法
    '''
    MOD: int
    _acc_limit: int
    __slots__ = ('MOD', '_acc_limit')
    def __init__(self, MOD: int) -> None:
        assert 1 ≤ MOD
        self.MOD = MOD
        if MOD > 3037000500:  #3_037_ + 3_037 ** 2 >= 2 ** 63
            self._acc_limit: int = 1
        else:  #(MOD - 1) + _acc_limit * (MOD - 1) ** 2 < 2 ** 63
            self._acc_limit: int = (~(-1 << 63) - (MOD - 1)) // ((MOD - 1) ** 2)
    #内部関数
    def _matrix_add(self, A: list[list[int]], B: list[list[int]],
                    H: int, W: int) -> list[list[int]]:
        C: list[list[int]] = [[0] * W for _ in range(H)]
        for h in range(H):
            Ah, Bh, Ch = A[h], B[h], C[h]
            for w, Ahw in enumerate(Ah):
                Ch[w] = (Ahw % self.MOD) + (Bh[w] % self.MOD)
                if Ch[w] >= self.MOD:
                    Ch[w] -= self.MOD
                while Ch[w] < 0:
                    Ch[w] += self.MOD
        return C
    def _matrix_mul(self, A: list[list[int]], B: list[list[int]], C: list[list[int]],
                    H: int, W: int, X: int) -> list[list[int]]:
        #すべての成分が 0 <= A[h][x], B[x][w] < MOD を満たすことを要求する
        B_w: list[int] = [0] * X
        for w in range(W):  #C[h][w] = sum(A[h][x] * B[x][w] for all x)
            for x in range(X):
                B_w[x] = B[x][w]
            for h in range(H):
                cnt: int = 0
                k: int = self._acc_limit
                for x, Ahx in enumerate(A[h]):
                    cnt += Ahx * B_w[x]
                    k -= 1
                    if k == 0:
                        cnt %= self.MOD
                        k = self._acc_limit
                C[h][w] = cnt % self.MOD
        return C
    def _matrix_doubling_mul(self, A: list[list[int]], N: int, k: int) -> list[list[int]]:
        if k == 0:
            return self.eye(N)
        C: list[list[int]] = [[0] * N for _ in range(N)]
        for h in range(N):
            Ch: list[int] = C[h]
            for w, Ahw in enumerate(A[h]):
                Ch[w] = Ahw % self.MOD
                if Ch[w] < 0:
                    Ch[w] += self.MOD
        if k == 1:
            return C
        D: list[list[int]] = [[0] * N for _ in range(N)]
        E: list[list[int]] = [C[h][:] for h in range(N)]
        for i in range(len(bin(k)) - 4, -1, -1):
            self._matrix_mul(C, C, D, N, N, N)
            C, D = D, C
            if k >> i & 1 == 1:
                self._matrix_mul(C, E, D, N, N, N)
                C, D = D, C
        return C
        
    #基本機能
    def eye(self, N: int) -> list[list[int]]:
        'N行N列の単位行列を返します。'
        A: list[list[int]] = [[0] * N for _ in range(N)]
        if self.MOD > 1:
            for i in range(N):
                A[i][i] = 1
        return A
    def add(self, A: list[list[int]], B: list[list[int]]) -> list[list[int]]:
        '行列C := A + B を新しく生成します。'
        assert len(A) == len(B)
        if len(A) == 0:
            return []
        H: int = len(A)
        W: int = len(A[0])
        assert all(len(Ai) == W for Ai in A) and all(len(Bi) == W for Bi in B)
        return self._matrix_add(A, B, H, W)
    def mul(self, A: list[list[int]], B: list[list[int]]) -> list[list[int]]:
        'H行X列の行列Aと、X行W列の行列Bから、行列C := A * Bを新しく作成します。'
        H: int = len(A)
        if H == 0:
            return []
        X: int = len(A[0])
        assert all(len(Ai) == X for Ai in A) and len(B) == X
        if X == 0:
            return [[] for _ in range(H)]
        W: int = len(B[0])
        assert all(len(Bi) == W for Bi in B)
        new_A: list[list[int]] = [[0] * X for _ in range(H)]
        new_B: list[list[int]] = [[0] * W for _ in range(X)]
        for h in range(H):
            new_Ah: list[int] = new_A[h]
            for x, Ahx in enumerate(A[h]):
                new_Ah[x] = Ahx % self.MOD
                if new_Ah[x] < 0:
                    new_Ah[x] += self.MOD
        for x in range(X):
            new_Bx: list[int] = new_B[x]
            for w, Bxw in enumerate(B[x]):
                new_Bx[w] = Bxw % self.MOD
                if new_Bx[w] < 0:
                    new_Bx[w] += self.MOD
        return self._matrix_mul(new_A, new_B, [[0] * W for _ in range(H)], H, W, X)
    def doubling_mul(self, A: list[list[int]], k: int) -> list[list[int]]:
        '正方行列Aから、正方行列C := A ** k を新しく作成します。'
        N: int = len(A)
        if N == 0:
            return []
        assert all(len(Ai) == N for Ai in A)
        assert k >= 0
        return self._matrix_doubling_mul(A, N, k)
