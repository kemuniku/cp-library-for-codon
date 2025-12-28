#Bipartite Matching for codon
#Reference: https://judge.yosupo.jp/submission/279592
from random import getrandbits as _BipartiteMatching_getrandbits
class BipartiteMatching:
    '''
    Bipartite Matching for codon
    L個の左側頂点と、R個の右側頂点の間の最大マッチングを計算します。
    マッチング結果は self.matched 配列に登録します。
    matched[Lt]: 左側頂点Ltとマッチした右側頂点Rt(0 <= Rt < R)。アンマッチの場合は-1
    時間計算量: E = (辺数), V = min(L, R) として O(E√V + L + R)

    L: 左側頂点数
    R: 右側頂点数  
    '''
    L: int
    R: int
    _edges: list[int]
    matched: list[int]
    _seed: u32
    __slots__ = ('L', 'R', '_edges', 'matched', '_seed')
    def __init__(self, L: int, R: int) -> None:
        assert 0 <= L < 1 << 30
        assert 0 <= R < 1 << 30
        self.L: int = L
        self.R: int = R
        self._edges: list[int] = []
        self.matched: list[int] = [-1] * L
        self._seed: u32 = u32(_BipartiteMatching_getrandbits(32) | 1)
    #内部関数
    def _build_CSR(self) -> tuple[int, int, list[i32], list[i32]]:
        compress_id: list[i32] = [i32(0)] * (self.L + self.R + self.L + 1)
        for x in self._edges:
            compress_id[x >> 32] += i32(1)
            compress_id[(x & 0xFFFFFFFF) + self.L] += i32(1)
        n: int = sum(compress_id[now] > i32(0) for now in range(self.L))
        m: int = 0
        CSR: list[i32] = [i32(0)] * (n + 1 + len(self._edges))
        for now in range(self.L):
            if compress_id[now] == i32(0):
                compress_id[now] = i32(-1)
            else:
                CSR[m + 1], compress_id[now] = compress_id[now], i32(m)
                m += 1
        for nxt in range(self.L, self.L + self.R):
            if compress_id[nxt] == i32(0):
                compress_id[nxt] = i32(-1)
            else:
                compress_id[nxt] = i32(m)
                m += 1
        m -= n
        CSR[0] = val = i32(n + 1)
        for now in range(1, n + 1):
            CSR[now], val = val, val + CSR[now]
        for x in self._edges:
            now: int = int(compress_id[x >> 32])
            nxt: i32 = compress_id[(x & 0xFFFFFFFF) + self.L]
            CSR[int(CSR[now + 1])] = nxt
            CSR[now + 1] += i32(1)
        for now in range(n + 1):
            compress_id[~ now] = CSR[now]  #CSR snapshot
        s: u32 = self._seed
        for now in range(n):  #CSR shuffle
            CSR_head: int = int(CSR[now])
            CSR_tail: int = int(CSR[now + 1])
            i: int = CSR_head
            diff: int = CSR_tail - CSR_head
            while i < CSR_tail:
                s ^= s << u32(13)
                s ^= s >> u32(17)
                s ^= s << u32(5)
                j: int = CSR_head + (int(s) % diff)
                CSR[i], CSR[j] = CSR[j], CSR[i]
                i += 1
        self._seed: u32 = s
        return (n, m, compress_id, CSR)
    def _solve_max_BipartiteMatching(self) -> None:
        #メンテナンス用メモ: 配列は以下の通り使い回す(Kuhn法 → Hopcroft-Karp法)
        #queue: i32 : [n: parent][n: queue] → dist : [n: dist_now][m: dist_nxt], stack
        #root : i32 : [n: root  ][m: rev  ] → CSRRt: [n: CSR_tail][m: rev     ]
        n, m, compress_id, CSR = self._build_CSR()
        parent = queue = [i32(-1)] * (n + max(n, m))
        root = rev = [i32(-1)] * (n + m)
        matched: list[int] = self.matched
        #1. 頂点の圧縮
        for original_now, nxt in enumerate(matched):
            original_nxt, matched[original_now] = matched[original_now], -1
            if original_nxt != -1:
                now: int = int(compress_id[original_now])
                matched[now] = nxt = int(compress_id[original_nxt + self.L])
                rev[nxt] = i32(now)
        #2. Kuhn法: 1回あたりO(V + E) * 最大√V回 = O(E√V)
        loop_count: int = 0
        loop_limit: int = int(min(n, m) ** 0.5) + 1
        found: bool = True
        s: u32 = self._seed
        while loop_count < loop_limit and found:
            loop_count += 1
            found: bool = False
            Lt = Rt = n - 1
            for now in range(n):
                if matched[now] == -1:
                    Rt += 1
                    root[now] = queue[Rt] = i32(now)
                    parent[now] = i32(-2)
                else:
                    root[now] = parent[now] = i32(-1)
            i: int = n
            offset: int = n
            diff: int = Rt + 1 - n
            while i <= Rt:  #キューをシャッフル
                s ^= s << u32(13)
                s ^= s >> u32(17)
                s ^= s << u32(5)
                j: int = offset + (int(s) % diff)
                queue[i], queue[j] = queue[j], queue[i]
                i += 1
            while Lt < Rt:
                Lt += 1
                now: int = int(queue[Lt])
                if matched[int(root[now])] != -1:
                    continue
                i: int = int(CSR[now])
                CSR_tail: int = int(CSR[now + 1])
                while i < CSR_tail:
                    nxt: int = int(CSR[i])
                    i += 1
                    back: int = int(rev[nxt])
                    if back == -1:
                        while now > -1:
                            rev[nxt] = i32(now)
                            matched[now], nxt = nxt, matched[now]
                            now: int = int(parent[now])
                        found: bool = True
                        break
                    elif parent[back] == i32(-1):
                        parent[back] = i32(now)
                        root[back] = root[now]
                        Rt += 1
                        queue[Rt] = i32(back)
        #3. Hopcroft-Karp法  O(E√V)
        if found:
            dist: list[i32] = queue
            CSRRt: list[i32] = root
            stack: list[i32] = [i32(0)] * n
            for now in range(n):
                CSRRt[now] = compress_id[~ now - 1]
            while True:
                #1. BFS
                Rt: int = 0
                aug_dist: i32 = i32(0x7FFFFFFF)
                for v in range(n + m):
                    dist[v] = i32(-1)
                for now in range(n):
                    if matched[now] == -1:
                        dist[now] = i32(0)
                        stack[Rt] = i32(now)
                        Rt += 1
                for Lt in range(n):
                    now: int = int(stack[Lt])
                    dist_now: i32 = dist[now]
                    if Lt == Rt or dist_now > aug_dist:
                        break
                    i: int = int(compress_id[~ now])
                    CSR[now] = compress_id[~ now]
                    CSR_tail: int = int(CSRRt[now])
                    while i < CSR_tail:
                        nxt: int = int(CSR[i])
                        i += 1
                        if dist[nxt] == i32(-1):
                            dist[nxt] = dist_now
                            back: int = int(rev[nxt])
                            if back == -1:
                                aug_dist: i32 = dist_now
                            elif dist[back] == i32(-1):
                                dist[back] = dist_now + i32(1)
                                stack[Rt] = i32(back)
                                Rt += 1
                if aug_dist == i32(0x7FFFFFFF):
                    break
                #2. DFS
                for now in range(n):
                    if dist[now] != i32(0):
                        continue
                    d: int = 0
                    stack[d] = i32(now)
                    dist[now] = i32(-1)
                    i: int = int(CSR[now])
                    CSR_tail: int = int(CSRRt[now])
                    while True:  #assert now == int(stack[d])
                        if i < CSR_tail:
                            nxt: int = int(CSR[i])
                            i += 1
                            if int(dist[nxt]) == d:
                                CSR[now] = i32(i - 1)
                                dist[nxt] = i32(-1)
                                back: int = int(rev[nxt])
                                if back == -1:  #assert i32(d) == aug_dist
                                    while d >= 0:
                                        now: int = int(stack[d])
                                        d -= 1
                                        matched[now] = nxt = int(CSR[int(CSR[now])])
                                        rev[nxt] = i32(now)
                                    break
                                elif dist[back] == i32(d + 1):
                                    now: int = back
                                    dist[now] = i32(-1)
                                    d += 1
                                    stack[d] = i32(now)
                                    i: int = int(CSR[now])
                                    CSR_tail: int = int(CSRRt[now])
                        else:
                            if d == 0:
                                break
                            d -= 1
                            now: int = int(stack[d])
                            i: int = int(CSR[now]) + 1
                            CSR_tail: int = int(CSRRt[now])
        #4. 解の復元
        for original_nxt in range(self.L, self.L + self.R):
            nxt: int = int(compress_id[original_nxt])
            if nxt != -1:
                root[nxt] = i32(original_nxt - self.L)
        for original_now in range(self.L - 1, -1, -1):
            now: int = int(compress_id[original_now])
            nxt, matched[original_now] = matched[now], -1
            if now != -1 != nxt:
                matched[original_now] = int(root[nxt])
        self._seed: u32 = s 
    
    #基本機能
    def add_edge(self, Lt: int, Rt: int) -> None:
        '左側頂点Ltと右側頂点Rtの間に辺を追加します。'
        assert 0 <= Lt < self.L
        assert 0 <= Rt < self.R
        self._edges.append(Lt << 32 | Rt)
    def build(self) -> None:
        '''
        これまでに追加した辺を用い、最大二部マッチングを求めます。
        マッチング結果は self.matched を参照してください。
        '''
        self._solve_max_BipartiteMatching()
