#高速素因数分解 for codon
#Reference: https://qiita.com/t_fuki/items/7cd50de54d3c5d063b4a
class prime:
    #内部関数
    def _miller_rabin(N: int) -> bool:
        if N < 2 or N & 1 == 0:
            return N == 2
        M, e = N - 1, (N - 1).__cttz__()  #e = (M & - M).bit_length() - 1
        d = M >> e  #M = N - 1 = d << e
        N128, M128 = UInt[128](N), UInt[128](M)
        for a in ([2, 7, 61] if N < 48781 * 97561 else
                  [2, 325, 9375, 28178, 450775, 9780504, 1795265022]):
            if a >= N:
                continue
            c = d
            x128, y128 = UInt[128](1), UInt[128](a)  #x = pow(a, d, N)
            while c:  #x = pow(a, d, N)
                if c & 1:
                    x128 = x128 * y128 % N128
                y128 = y128 * y128 % N128
                c >>= 1
            if x128 == UInt[128](1):  #x = pow(a, d, N) ≡ 1 ならおそらく素数
                continue
            while x128 != M128:  #pow(x, 2 ** (c := e未満), N) ≡ -1 ならおそらく素数
                x128 = x128 * x128 % N128
                c += 1
                if x128 == UInt[128](1) or c == e:
                    return False
        return True
    def _pollard_rho(N: int) -> int:  #Nの素因数を探索  ミラーラビンを参照する
        assert N > 0
        if N & 1 == 0:
            return 2
        if N == 1 or prime._miller_rabin(N):
            return N
        while True:
            N128 = Int[128](N)
            step = int(N ** 0.125) + 1
            for c in range(1, N):
                #f(n) = n ** 2 + c mod N と疑似乱数を定義する
                #y128 = f^{s}(0), z128: Π(x128 - y128) mod N128
                #g: gcd(x, y)  t: sの次の目標となる2冪
                y128, z128, c128 = Int[128](0), Int[128](1), Int[128](c)
                g, s, t = 1, 0, 1
                while g == 1:
                    x128 = y128
                    nxt_s = (3 * t) >> 2
                    for _ in range(nxt_s - s):
                        y128 = (y128 * y128 + c128) % N128  #y ← f(y)
                    s = nxt_s
                    while s < t and g == 1:
                        backtrack128 = y128
                        for _ in range(min(step, t - s)):  #N ** 1/8回まとめてgcdを計算
                            y128 = (y128 * y128 + c128) % N128  #y ← f(y)
                            z128 = z128 * (x128 - y128) % N128
                        g, h = N, abs(int(z128))
                        while h:  #g ← gcd(N, z128)
                            g, h = h, g % h
                        s += step
                    s, t = t, t << 1
                if g == N:
                    g, y128 = 1, backtrack128
                    while g == 1:
                        y128 = (y128 * y128 + c128) % N128  #y ← f(y)
                        g, h = abs(int(x128 - y128)), N
                        while h:  #g ← gcd(N, x128 - y128)
                            g, h = h, g % h
                    if g == N:
                        continue  #検出失敗
                if prime._miller_rabin(g):
                    return g
                elif prime._miller_rabin(N // g):
                    return N // g
                else:
                    N = g
                    break  #while Trueへ
    def _fast_fact(N: int) -> list[tuple[int, int]]:
        assert N >= 1
        ans: list[tuple[int, int]] = []
        if N & 1 == 0:
            ans.append((2, N.__cttz__()))
            N >>= N.__cttz__()
        p2 = 1
        for p in range(3, int(N ** 0.25), 2):  #O(N ** 1/4)回のためし割り
            p2 += (p - 1) << 2  #assert p * p == p2
            if p2 > N:
                if N > 1:
                    ans.append((N, 1))
                    N = 1
                break
            if N % p == 0:
                e = 0
                while N % p == 0:
                    N //= p
                    e += 1
                ans.append((p, e))
        while N > 1:
            p = prime._pollard_rho(N)
            e = 0
            while N % p == 0:
                N //= p
                e += 1
            ans.append((p, e))
        ans.sort()
        return ans
    def _enumerate_divisor(N: int) -> list[int]:
        F: list[tuple[int, int]] = prime._fast_fact(N)
        Rt: int = 1
        for _, e in F:
            Rt *= e + 1
        D: list[int] = [1] * Rt
        Rt: int = 1
        for p, e in F:
            for Lt in range(Rt * e):
                D[Rt] = D[Lt] * p
                Rt += 1
        D.sort()
        return D

    #素数判定
    def is_prime(N: int) -> bool:
        '''
        ミラーラビン素数判定法により素数判定を行います。
        計算量: int128の剰余演算の計算量をO(L)としたとき、O(7L * logN)
        制約: 1 <= N < 2 ** 63
        '''
        assert 1 <= N
        return prime._miller_rabin(N)

    #O(N ** 1/4) 高速素因数分解
    def factorize(N: int) -> list[tuple[int, int]]:
        '''
        Nを素因数分解し、(素因数, 次数) の形のリストとして返します。
        期待計算量: int128の剰余演算をO(L)としたとき、O(L * N ** 1/4)
        制約: 1 <= N < 2 ** 63
        '''
        assert 1 <= N
        return prime._fast_fact(N)

    #約数列挙
    def divisor(N: int) -> list[int]:
        '''
        Nの約数を列挙し、ソートして返します。
        期待計算量: 約数の個数をdとしたとき、prime.factorize + O(d * logd)
        制約: 1 <= N < 2 ** 63
        '''
        assert 1 <= N
        return prime._enumerate_divisor(N)
