#mincostflow for codon
class MCFGraph[T]:
    '''
    mincostflow for codon
    頂点数V・辺数E・流量Fとして、O(F(E + V)logV)で最小費用流を計算します。
    負辺がある場合、O(EV)が追加でかかります。
    
    最小コストで止めたい場合、St → Gl(容量X・コスト0)を足し、flow_limit = X で流してください。
    制約: 辺容量はすべて非負整数
          初期グラフに正容量辺からなるコスト負閉路が存在しない

    N: 頂点数
    '''
    N: int
    M: int
    _size: int
    _edge: list[int]
    _capa: list[int]
    _cost: list[T]
    __slots__ = ('N', 'M', '_size', '_edge', '_capa', '_cost')
    def __init__(self, N: int) -> None:
        assert 0 <= N < 1 << 30
        self.N: int = N
        self.M: int = 0
        self._edge: list[int] = []
        self._capa: list[int] = []
        self._cost: list[T] = []
    #内部実装
    def _create_neginf_zero_inf(self) -> tuple[T, T, T]:
        if isinstance(T, int):
            return (-1 << 63, 0, ~(-1 << 63))
        elif isinstance(T, Int):
            return (T(-1) << T(T.N - 1), T(0), ~(T(-1) << T(T.N - 1)))
        elif isinstance(T, UInt):
            return (T(0), T(0), T(-1))
        else:
            return (-T(1e1000), T(0), T(1e1000))
    def _min_cost_slope(self, St: int, Gl: int, flow_limit: int) -> list[tuple[int, T]]:
        assert 0 <= St < self.N and 0 <= Gl < self.N and St != Gl and 0 < flow_limit
        N, M = self.N, self.M
        logN: int = 0 if N <= 1 else len(bin(N - 1)) - 2  #max(0, N - 1).bit_length()
        size: int = 1 << logN
        _, zero, INF = self._create_neginf_zero_inf()
        delta: T = zero
        ans: list[tuple[int, T]] = [(0, zero)]
        dist_prev_cost : list[T]   = [zero] * (2 * N + 3 + 2 * M)
        CSR_history_nxt: list[int] = [0]    * (2 * N + 3 + 2 * M)
        nodeid_i2m_m2i : list[int] = [-1]   * (2 * N + 3 + 2 * M + 2 * M)
        forward_star   : list[int] = [0]    * (size + N)
        node           : list[T]   = [INF]  * (size + N)
        #有効な負辺が1本でも存在すればBellman Fordを実行
        if any((self._cost[m] < zero and self._capa[m << 1    ] > 0) or
               (self._cost[m] > zero and self._capa[m << 1 | 1] > 0) for m in range(M)):
            delta, flow_limit = self._Bellman_Ford(
                St, Gl, flow_limit, ans, dist_prev_cost,
                CSR_history_nxt, nodeid_i2m_m2i, forward_star)
        self._Dijkstra(St, Gl, flow_limit, ans, delta, dist_prev_cost, CSR_history_nxt,
                       nodeid_i2m_m2i, forward_star, node)
        return ans
    def _Dijkstra(self, St: int, Gl: int, flow_limit: int, ans: list[tuple[int, T]],
                  delta: T, dist: list[T], CSR: list[int], nodeid: list[int],
                  fstar: list[int], node: list[T]) -> None:
        #Dijkstra with SegTreeで最短路反復  ansを編集した状態にする
        #1. CSR
        N, M = self.N, self.M
        _, zero, INF = self._create_neginf_zero_inf()
        St <<= 1
        Gl <<= 1  #頂点は2倍値で処理
        for m in range(M):
            now, nxt = self._edge[m] >> 32, self._edge[m] & 0xFFFFFFFF
            CSR[(now << 1) + 4] += 1
            CSR[(nxt << 1) + 4] += 1
        CSR[0] = 2 * N + 3
        for now in range(2, 2 * N + 3, +2):
            CSR[now] += CSR[now - 2]
        for m in range(M):
            now, nxt = self._edge[m] >> 32, self._edge[m] & 0xFFFFFFFF
            now <<= 1
            nxt <<= 1
            i: int = CSR[now + 2]
            CSR[i] = nxt if self._capa[m << 1    ] > 0 else ~ nxt
            dist[i] = self._cost[m]
            nodeid[i], nodeid[~(m << 1    )] = m << 1, i
            CSR[now + 2] += 1
            i: int = CSR[nxt + 2]
            CSR[i] = now if self._capa[m << 1 | 1] > 0 else ~ now
            dist[i] = - self._cost[m]
            nodeid[i], nodeid[~(m << 1 | 1)] = m << 1 | 1, i
            CSR[nxt + 2] += 1
        #2. 最短路反復
        while flow_limit > 0:
            #1. 反復前初期化
            for now in range(0, 2 * N, 2):
                dist[now] = INF
            for i in range(N):
                nodeid[i << 1 | 1] = i + 1
            size = free = 1
            head = tail = 0
            dist[St] = node[1] = zero  #assert dist[St] == dist[St | 1] == zero
            nodeid[St], nodeid[0 << 1 | 1] = 1, St
            #2. pop可能な全頂点を更新
            while True:
                #lazy update
                fstar[0], head = head, 0
                while head != tail:
                    fstar[head], head = 0, fstar[head]
                    if head != 1:
                        d: T = node[head]
                        p: int = head >> 1
                        if d < node[p]:
                            node[p] = d
                            if fstar[p] == 0:
                                fstar[tail] = fstar[p] = p
                                tail = p
                fstar[head] = 0  #assert all(fstar[i] == 0 for i in range(len(fstar)))
                head = tail = 0
                #pop now
                cur: int = 1
                dist_now: T = node[1]
                if dist_now == INF:  #停止条件
                    break
                while cur < size:
                    cur <<= 1
                    if node[cur] > dist_now:
                        cur |= 1
                now: int = nodeid[(cur ^ size) << 1 | 1]  #assert dist[now] == dist_now
                w = node[cur] = INF
                nodeid[now] = -1
                nodeid[(cur ^ size) << 1 | 1], free = free, cur ^ size
                while cur != 1:
                    w = min(w, node[cur ^ 1])
                    cur >>= 1
                    node[cur] = w
                #for nxt, d in G[now]
                dist_now += dist[now | 1]  #+= prev[now]
                i, CSRRt = CSR[now], CSR[now + 2]
                while i < CSRRt:
                    nxt, cost = CSR[i], dist[i]
                    if nxt >= 0:  #cap == 0の辺は~ nxt (< 0)として区別している
                        d: T = dist_now + cost - dist[nxt | 1]
                        if d < dist[nxt]:
                            dist[nxt] = d
                            CSR[nxt | 1] = i
                            #chmin(nxt, d)
                            cur: int = nodeid[nxt]
                            if cur == -1:  #初登録
                                if free == size:
                                    for x in range(size, size << 1):
                                        node[x + size], node[x] = node[x], INF
                                        if fstar[x] != 0:
                                            fstar[x + size], fstar[x] = fstar[x] + size, 0
                                    for x in range(size + (-(-size >> 1)) - 1, 0, -1):
                                        node[x] = min(node[x << 1], node[x << 1 | 1])
                                    for x in range(1, 2 * size, 2):
                                        nodeid[nodeid[x]] += size
                                    if head != 0:
                                        head += size
                                        tail += size
                                    size <<= 1
                                cur = nodeid[nxt] = free | size
                                nodeid[free << 1 | 1], free = nxt, nodeid[free << 1 | 1]
                            node[cur] = d
                            if fstar[cur] == 0:
                                if head == 0:
                                    head = tail = cur
                                fstar[cur], head = head, cur
                    i += 1
            #3. pop可能な全頂点更新後、Glに未達なら更新を終了
            if dist[Gl] == INF:
                break
            #4. 最短路復元  nodeid[odd]が廃棄領域なのでここに記録
            now: int = Gl
            flow: int = flow_limit
            current_delta: T = zero
            k: int = 1
            while now != St:
                i: int = CSR[now | 1]
                m: int = nodeid[i]  #assert self._capa[m] > 0
                flow = min(flow, self._capa[m])
                if m & 1 == 0:  #assert now == (self._edge[m >> 1] & 0xFFFFFFFF) << 1
                    back: int = (self._edge[m >> 1] >> 32) << 1
                else:  #assert now == (self._edge[m >> 1] >> 32) << 1
                    back: int = (self._edge[m >> 1] & 0xFFFFFFFF) << 1
                current_delta += dist[i]
                nodeid[k] = m
                k += 2
                now: int = back
            while k > 1:  #assert flow > 0
                k -= 2
                m: int = nodeid[k]  #assert self._capa[m] >= flow
                self._capa[m] -= flow
                if self._capa[m] == 0:
                    i: int = nodeid[~ m]
                    CSR[i] = ~ CSR[i]
                if self._capa[m ^ 1] == 0:
                    i: int = nodeid[~ (m ^ 1)]
                    CSR[i] = ~ CSR[i]
                self._capa[m ^ 1] += flow
            if len(ans) == 1 or delta != current_delta:
                ans.append((ans[-1][0] + flow, ans[-1][1] + T(flow) * current_delta))
            else:
                assert len(ans) > 1 and delta == current_delta
                ans[-1] = (ans[-1][0] + flow, ans[-1][1] + T(flow) * current_delta)
            delta: T = current_delta
            flow_limit -= flow
            #5. prev[now] += dist[now]  INFキャップを忘れずに
            for now in range(0, 2 * N, 2):
                if dist[now ^ 1] >= INF - dist[now]:
                    dist[now ^ 1] = INF
                else:
                    dist[now ^ 1] += dist[now]
    def _Bellman_Ford(self, St: int, Gl: int, flow_limit: int, ans: list[tuple[int, T]],
                      dist: list[T], CSR: list[int], history: list[int],
                      fstar: list[int]) -> tuple[T, int]:
        #1回Bellman Fordを実行しansとcapaに反映。deltaとflow_limitを返す
        #1. CSR
        N, M = self.N, self.M
        NEG_INF, zero, INF = self._create_neginf_zero_inf()
        for m in range(M):
            now, nxt = self._edge[m] >> 32, self._edge[m] & 0xFFFFFFFF
            if self._capa[m << 1] > 0:
                CSR[now + 2] += 1
            if self._capa[m << 1 | 1] > 0:
                CSR[nxt + 2] += 1
        CSR[0] = N + 2
        for now in range(1, N + 2):
            CSR[now] += CSR[now - 1]
        for m in range(M):
            now, nxt = self._edge[m] >> 32, self._edge[m] & 0xFFFFFFFF
            if self._capa[m << 1] > 0:
                i: int = CSR[now + 1]
                CSR[i] = nxt
                dist[i] = self._cost[m]
                history[i] = m << 1
                CSR[now + 1] += 1
            if self._capa[m << 1 | 1] > 0:
                i: int = CSR[nxt + 1]
                CSR[i] = now
                dist[i] = - self._cost[m]
                history[i] = m << 1 | 1
                CSR[nxt + 1] += 1
        #2. min( N - 1, valid_edge := CSR[N + 1] - CSR[0] )回のBellman Ford
        for now in range(N + 1):
            dist[now] = INF  #ループ終了時にnow = Nとなる
            fstar[now] = -1  #未更新のフラグ
        tail = fstar[N] = St
        dist[St] = zero
        loop_limit: int = min(N - 1, CSR[N + 1] - CSR[0])
        while True:
            dist_now: T = dist[now]
            if now == N:
                loop_limit -= 1
                if loop_limit < 0:
                    break
                fstar[tail], tail = N, N
            elif dist_now != INF:
                clamp: T = INF - dist_now if dist_now >= zero else NEG_INF - dist_now
                i, CSRRt = CSR[now], CSR[now + 1]
                while i < CSRRt:
                    nxt, cost = CSR[i], dist[i]
                    if dist_now >= zero:
                        dist_nxt = dist_now + cost if cost <= clamp else INF
                    else:
                        dist_nxt = dist_now + cost if clamp <= cost else NEG_INF
                    if dist[nxt] > dist_nxt:
                        dist[nxt] = dist_nxt
                        history[nxt] = i
                        if fstar[nxt] == -1:
                            fstar[tail], tail = nxt, nxt
                    i += 1
            fstar[now], now = -1, fstar[now]
        #3. 負閉路検知・波及(負閉路がある場合、正常な動作は期待できない)
        for now in range(N):
            dist_now: T = dist[now]
            if dist_now != INF:
                clamp: T = INF - dist_now if dist_now >= zero else NEG_INF - dist_now
                i, CSRRt = CSR[now], CSR[now + 1]
                while i < CSRRt:
                    nxt, cost = CSR[i], dist[i]
                    i += 1
                    if dist_now >= zero:
                        dist_nxt = dist_now + cost if cost <= clamp else INF
                    else:
                        dist_nxt = dist_now + cost if clamp <= cost else NEG_INF
                    if dist[nxt] > dist_nxt:
                        dist[nxt] = NEG_INF
        d: int = 0
        for now in range(N):
            if dist[now] == NEG_INF:
                fstar[d] = now
                d += 1
        while d:
            d -= 1
            now: int = fstar[d]
            i, CSRRt = CSR[now], CSR[now + 1]
            while i < CSRRt:
                nxt, cost = CSR[i], dist[i]
                i += 1
                if dist[nxt] != NEG_INF:
                    dist[nxt] = NEG_INF
                    fstar[d] = nxt
                    d += 1
        #4. dist[Gl] == NEG_INF の場合、復元不可能なのでassertで終了。そうでなければ復元
        assert dist[Gl] != NEG_INF, 'Glを含む負閉路を検知しました。'
        delta: T = dist[Gl]
        if delta != INF:
            flow: int = flow_limit  #今回の最大流量
            d: int = 0
            now: int = Gl
            while now != St:
                i: int = history[now]
                m: int = history[i]  #assert self._capa[m] > 0
                flow = min(flow, self._capa[m])
                if m & 1 == 0:  #assert now == self._edge[m >> 1] & 0xFFFFFFFF
                    back: int = self._edge[m >> 1] >> 32
                else:  #assert now == self._edge[m >> 1] >> 32
                    back: int = self._edge[m >> 1] & 0xFFFFFFFF
                fstar[d] = m
                d += 1
                now: int = back
            while d:
                d -= 1
                m: int = fstar[d]  #assert flow <= self._capa[m]
                self._capa[m] -= flow
                self._capa[m ^ 1] += flow
            ans.append((flow, delta * T(flow)))
            flow_limit -= flow
        #5. 配列整理
        for now in range(N - 1, -1, -1):  #prevへの転記
            dist[now << 1 | 1] = dist[now]
        for now in range(0, 2 * N + 3, 2):    #CSRを初期化
            CSR[now] = 0
        for now in range(N + 1):  #fstarは全要素0で初期化
            fstar[now] = 0
        for now in range(0, 2 * N, 2):  #history = nodeid を初期化
            history[now] = -1
        return (delta, flow_limit)

    #基本機能: 辺の追加・参照
    def add_edge(self, now: int, nxt: int, cap: int, cost: T) -> None:
        '頂点nowから頂点nxtに向かう、容量cap・1流量あたりのコストcostの辺を追加します。'
        assert 0 <= now < self.N and 0 <= nxt < self.N
        assert 0 <= cap
        self.M += 1
        self._edge.append(now << 32 | nxt)
        self._capa.append(cap)
        self._capa.append(0)
        self._cost.append(cost)
    def get_edge(self, i: int) -> tuple[int, int, int, int, T]:
        '''
        i番目に追加した順辺の情報を取得します。
        (now, nxt, 初期容量cap, 現在の流量flow, cost)の順です。
        '''
        assert 0 <= i < self.M
        cap, rev_cap = self._capa[i << 1], self._capa[i << 1 | 1]
        return (self._edge[i] >> 32, self._edge[i] & 0xFFFFFFFF,
                cap + rev_cap, rev_cap, self._cost[i])
    def edges(self) -> list[tuple[int, int, int, int, T]]:
        'すべての順辺iについて、get_edge(i)の結果を返します。'
        return [self.get_edge(i) for i in range(self.M)]

    #基本機能: 最小費用流
    def flow(self, St: int, Gl: int) -> tuple[int, T]:
        '頂点Stから頂点Glに限界までフローを流し、(合計流量, 合計コスト)を返します。'
        assert 0 <= St < self.N and 0 <= Gl < self.N and St != Gl
        return self._min_cost_slope(St, Gl, ~(-1 << 63))[-1]
    def flow(self, St: int, Gl: int, flow_limit: int) -> tuple[int, T]:
        '頂点Stから頂点Glにflow_limitまでフローを流し、(合計流量, 合計コスト)を返します。'
        assert 0 <= St < self.N and 0 <= Gl < self.N and St != Gl
        if flow_limit <= 0:
            return (0, self._create_neginf_zero_inf()[1])
        return self._min_cost_slope(St, Gl, flow_limit)[-1]
    def slope(self, St: int, Gl: int) -> list[tuple[int, T]]:
        '''
        頂点Stから頂点Glまで限界までフローを流し、コストの変曲点を列挙します。
        変曲点における(合計流量, 合計コスト)を列挙し、リストとして返します。
        '''
        assert 0 <= St < self.N and 0 <= Gl < self.N and St != Gl
        return self._min_cost_slope(St, Gl, ~(-1 << 63))
    def slope(self, St: int, Gl: int, flow_limit: int) -> list[tuple[int, T]]:
        '''
        頂点Stから頂点Glまでflow_limitまでフローを流し、コストの変曲点を列挙します。
        変曲点における(合計流量, 合計コスト)を列挙し、リストとして返します。
        '''
        assert 0 <= St < self.N and 0 <= Gl < self.N and St != Gl
        if flow_limit <= 0:
            return [(0, self._create_neginf_zero_inf()[1])]
        return self._min_cost_slope(St, Gl, flow_limit)
