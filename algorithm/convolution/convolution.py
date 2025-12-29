#convolution for codon, PyPy3
#Reference: https://github.com/shakayami/ACL-for-python/blob/master/convolution.py
class convolution:
    '''
    convolution for codon, PyPy3
    mod Pにおける畳み込みを O(NlogN + Nlog(wordsize)) で行います。
    (wordsize = 64(定数) とします。実装上、CPUの64bitワードに基づくビット演算を行います)

    P: 法となる素数 2 <= P <= 2_147_483_648 を満たす
    primitive_root: Pの原始根 分からない場合は0を入力してください(自動で探索します)
    '''
    P: int
    _rank2: int
    _root: list[int]
    _iroot: list[int]
    _rate2: list[int]
    _rate3: list[int]
    _irate2: list[int]
    _irate3: list[int]
    __slots__ = ('P', '_rank2', '_root', '_iroot', '_rate2', '_rate3', '_irate2', '_irate3')
    def __init__(self, P: int, primitive_root: int = 0) -> None:
        assert 2 <= P <= 2147_483_648, f'2 <= P <= 2147_483_648 から外れています。{P = }'
        if not 1 <= primitive_root < P:
            primitive_root: int = self.find_primitive_root(P)
        self.P: int = P
        Q: int = P - 1
        self._rank2: int = len(bin(Q & - Q)) - 3  #(Q & - Q).bit_length() - 1
        self._root = [pow(primitive_root, Q >> e, P) for e in range(self._rank2 + 1)]
        self._iroot = [pow(Ri, P - 2, P) for Ri in self._root]  #pow(Ri, -1, P)
        self._rate2, self._irate2 = [0] * (self._rank2    ), [0] * (self._rank2    )
        self._rate3, self._irate3 = [0] * (self._rank2 - 1), [0] * (self._rank2 - 1)
        r2 = i2 = r3 = i3 = 1
        for i in range( self._rank2 - 1 ):
            self._rate2[i] = ( self._root[i + 2] * r2 ) % P
            self._irate2[i] = ( self._iroot[i + 2] * i2 ) % P
            r2, i2 = ( r2 * self._iroot[i + 2] ) % P, ( i2 * self._root[i + 2] ) % P
        for i in range( self._rank2 - 2 ):
            self._rate3[i] = ( self._root[i + 3] * r3 ) % P
            self._irate3[i] = ( self._iroot[i + 3] * i3 ) % P
            r3, i3 = ( r3 * self._iroot[i + 3] ) % P, ( i3 * self._root[i + 3] ) % P
    def __init__(self, P: int, primitive_root: int = 0) -> None:
        assert 2 <= P <= 2147_483_648, f'2 <= P <= 2147_483_648 から外れています。{P = }'
        if not 1 <= primitive_root < P:
            primitive_root: int = self.find_primitive_root(P)
        self.P: int = P
        Q: int = P - 1
        self._rank2: int = len(bin(Q & - Q)) - 3  #(Q & - Q).bit_length() - 1
        self._root = [pow(primitive_root, Q >> e, P) for e in range(self._rank2 + 1)]
        self._iroot = [pow(Ri, P - 2, P) for Ri in self._root]  #pow(Ri, -1, P)
        self._rate2, self._irate2 = [0] * (self._rank2    ), [0] * (self._rank2    )
        self._rate3, self._irate3 = [0] * (self._rank2 - 1), [0] * (self._rank2 - 1)
        r2 = i2 = r3 = i3 = 1
        for i in range( self._rank2 - 1 ):
            self._rate2[i] = ( self._root[i + 2] * r2 ) % P
            self._irate2[i] = ( self._iroot[i + 2] * i2 ) % P
            r2, i2 = ( r2 * self._iroot[i + 2] ) % P, ( i2 * self._root[i + 2] ) % P
        for i in range( self._rank2 - 2 ):
            self._rate3[i] = ( self._root[i + 3] * r3 ) % P
            self._irate3[i] = ( self._iroot[i + 3] * i3 ) % P
            r3, i3 = ( r3 * self._iroot[i + 3] ) % P, ( i3 * self._root[i + 3] ) % P
    #内部関数
    def _factorize(self, N: int) -> list[int]:  #O(√N) 素因数のみ
        n: int = N
        F: list[int] = []
        for p in range(2, N + 1):
            if p ** 2 > n:
                if n > 1:
                    F.append(n)
                break
            if n % p == 0:
                F.append(p)
                while n % p == 0:
                    n //= p
        return F
    def _butterfly(self, B: list[int], required_len: int) -> list[int]:
        logN: int = 0
        while not required_len <= 1 << logN:
            logN += 1
        assert logN <= self._rank2, (
            f'{required_len = } は NTT可能な長さ {1 << self._rank2} を超えています。')
        A: list[int] = [0] * (1 << logN)
        for i in range( min(len(A), len(B)) ):
            A[i] = B[i] % self.P
        h: int = 0
        P, rate2, rate3 = self.P, self._rate2, self._rate3
        while h < logN:
            if logN - h == 1 or P >= 1753_413_058:
                d: int = 1 << (logN - h - 1)
                rot: int = 1
                for b in range(1 << h):
                    offset: int = b << (logN - h)
                    for i in range(d):
                        Ai, Aj = A[i | offset], A[i | offset | d] * rot
                        A[i | offset], A[i | offset | d] = (Ai + Aj) % P, (Ai - Aj) % P
                    c: int = (~b & - ~b) - 1  #c ← (~b & - ~b).bit_length() - 1
                    c: int = ( c & 0x55555555 ) + ( (c >> 1) & 0x55555555 )
                    c: int = ( c & 0x33333333 ) + ( (c >> 2) & 0x33333333 )
                    c: int = ( c & 0x0F0F0F0F ) + ( (c >> 4) & 0x0F0F0F0F )
                    c: int = c * 0x1010101 >> 24 & 63
                    rot: int = rot * rate2[c] % P
                h += 1
            else:
                d: int = 1 << (logN - h - 2)
                rot: int = 1
                imag: int = self._root[2]
                for b in range(1 << h):
                    offset: int = b << (logN - h)
                    r2: int = rot * rot % P
                    r3: int = r2 * rot % P
                    for i in range(d):
                        Ai, Aj = A[i | offset        ],      A[i | offset | d    ] * rot
                        Ak, AL = A[i | offset | 2 * d] * r2, A[i | offset | 3 * d] * r3
                        AjL: int = (Aj - AL) % P * imag
                        A[i | offset        ] = (Ai + Aj + Ak + AL) % P
                        A[i | offset | d    ] = (Ai - Aj + Ak - AL) % P
                        A[i | offset | 2 * d] = (Ai - Ak + AjL) % P
                        A[i | offset | 3 * d] = (Ai - Ak - AjL) % P
                    c: int = (~b & - ~b) - 1  #c ← (~b & - ~b).bit_length() - 1
                    c: int = ( c & 0x55555555 ) + ( (c >> 1) & 0x55555555 )
                    c: int = ( c & 0x33333333 ) + ( (c >> 2) & 0x33333333 )
                    c: int = ( c & 0x0F0F0F0F ) + ( (c >> 4) & 0x0F0F0F0F )
                    c: int = c * 0x1010101 >> 24 & 63
                    rot: int = rot * rate3[c] % P
                h += 2 
        return A
    def _butterfly_inv(self, A: list[int]) -> list[int]:
        N: int = len(A)
        logN: int = len(bin(N)) - 3
        assert 0 <= logN and N == 1 << logN
        for i, Ai in enumerate(A):
            A[i] = Ai % self.P  #abs(Ai) < P に補正
        h: int = logN
        P, irate2, irate3 = self.P, self._irate2, self._irate3
        while h > 0:
            if h == 1 or P > 1518_500_250:
                h -= 1
                d: int = 1 << (logN - h - 1)
                irot: int = 1
                for b in range(1 << h):
                    offset: int = b << (logN - h)
                    for i in range(d):
                        Ai, Aj = A[i | offset], A[i | offset | d]
                        A[i | offset], A[i | offset | d] = (Ai + Aj) % P, (Ai - Aj) * irot % P
                    c: int = (~b & - ~b) - 1  #c ← (~b & - ~b).bit_length() - 1
                    c: int = ( c & 0x55555555 ) + ( (c >> 1) & 0x55555555 )
                    c: int = ( c & 0x33333333 ) + ( (c >> 2) & 0x33333333 )
                    c: int = ( c & 0x0F0F0F0F ) + ( (c >> 4) & 0x0F0F0F0F )
                    c: int = c * 0x1010101 >> 24 & 63
                    irot: int = irot * irate2[c] % P
            else:
                h -= 2
                d: int = 1 << (logN - h - 2)
                irot: int = 1
                iimag: int = self._iroot[2]
                for b in range(1 << h):
                    offset: int = b << (logN - h)
                    i2: int = irot * irot % P
                    i3: int = i2 * irot % P
                    for i in range(d):
                        Ai, Aj = A[i | offset        ], A[i | offset | d    ]
                        Ak, AL = A[i | offset | 2 * d], A[i | offset | 3 * d]
                        AkL: int = (Ak - AL) * iimag % P
                        A[i | offset        ] = (Ai + Aj + Ak + AL) % P
                        A[i | offset | d    ] = (Ai - Aj + AkL) * irot % P
                        A[i | offset | 2 * d] = (Ai + Aj - Ak - AL) * i2 % P
                        A[i | offset | 3 * d] = (Ai - Aj - AkL) * i3 % P
                    c: int = (~b & - ~b) - 1  #c ← (~b & - ~b).bit_length() - 1
                    c: int = ( c & 0x55555555 ) + ( (c >> 1) & 0x55555555 )
                    c: int = ( c & 0x33333333 ) + ( (c >> 2) & 0x33333333 )
                    c: int = ( c & 0x0F0F0F0F ) + ( (c >> 4) & 0x0F0F0F0F )
                    c: int = c * 0x1010101 >> 24 & 63
                    irot: int = irot * irate3[c] % P
        revN: int = pow(N, P - 2, P)
        for i in range(N):
            A[i] = A[i] * revN % P
            if A[i] < 0:
                A[i] += P
        return A

    #高度な機能
    def find_primitive_root(self, P: int) -> int:
        'O(√P + log^2 P)で、素数Pの原始根のひとつを返します。'
        if P in (998244353, 1107296257, 1711276033, 1811939329, 2013265921, 2113929217):
            return 1542
        assert 2 <= P and self._factorize(P)[-1] == P
        F: list[int] = self._factorize(P - 1)
        for a in range(1, P):
            if all(pow(a, (P - 1) // Pi, P) != 1 for Pi in F):
                return a
    def DFT(self, A: list[int], required_len: int) -> list[int]:
        '''
        元となる配列Aと、畳み込みに必要な配列の長さ required_len を入力します。
        Nを「required_len 以上となる最小の2冪」として、
        Aをゼロ埋めしてDFTした、長さNの配列B を新しく作成し返します。
        N < len(A) の時は、Aの先頭N要素をDFTします。
        '''
        return self._butterfly(A, required_len)
    def IDFT(self, A: list[int]) -> list[int]:
        '''
        DFT表現の配列AにIDFTを行います。
        DFTと異なり、返り値は 「破壊的変更を加えた、長さ2冪の配列A」 です。
        '''
        return self._butterfly_inv(A)

    #基本機能: 畳み込み
    def convolve(self, F: list[int], G: list[int]) -> list[int]:
        '''
        配列Fと配列Gを畳み込み、長さ len(F) + len(G) - 1 の配列Hを返します。
        ここで、 0 <= H[i] < P を満たします。
        ただし、len(F) == 0 または len(G) == 0 の時は [] を返します。
        '''
        i, j = len(F), len(G)
        if min(i, j) == 0:
            return []
        while i > 0 and F[i - 1] == 0:
            i -= 1
        while j > 0 and G[j - 1] == 0:
            j -= 1
        n: int = max(0, i + j - 1)
        A_F: list[int] = self._butterfly(F, n)
        A_G: list[int] = self._butterfly(G, n)
        for i, A_Gi in enumerate(A_G):
            A_F[i] = A_F[i] * A_Gi % self.P
        A_F: list[int] = self._butterfly_inv(A_F)
        H: list[int] = [0] * (len(F) + len(G) - 1)
        for i in range( min(len(H), len(A_F)) ):
            H[i] = A_F[i]
        return H
