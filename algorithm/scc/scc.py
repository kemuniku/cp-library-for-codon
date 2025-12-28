#SCC for codon, PyPy3
class SCCGraph:
    '''
    SCC for codon, PyPy3
    頂点数をN, 辺数をMとして、O(N + M)で強連結成分分解を行います。

    ■ACLとの相違点
    scc(make_adjacency_list: bool) の実行結果を以下のように保持します。
     - self.n : 強連結成分の個数 len(self.groups) と等しい
     - self.pos : pos[now] = 頂点nowが属する強連結成分の番号i (0 <= i < n)
     - self.groups : groups[i] = トポロジカルソート順がiの強連結成分に含まれる頂点のリスト
     - self.G : make_adjacency_list = True の時のみ追加で作成する。頂点縮約後の隣接リスト
                G[i] = トポロジカルソート順がiの強連結成分から繋がる強連結成分のリスト

    N: 頂点数 (0 <= N < 2 ** 30)     
    '''
    N: int
    n: int
    pos: list[int]
    groups: list[list[int]]
    G: list[list[int]]
    _edges: list[int]
    __slots__ = ('N', 'n', 'pos', 'groups', 'G', '_edges')
    def __init__(self, N: int) -> None:
        assert 0 <= N < 1 << 30
        self.N = N
        self._edges = [-1] * (N + 1)
    #内部関数
    def _SCC_Tarjan(self, make_adjacency_list: bool) -> None:
        #メンテナンス用メモ: 配列を以下のように使い回す
        #E: [forward_star][1][edges: cur, nxt]  order: [order ][DFS stack]
        #F: [forward_star][team stack        ]  low:   [low,id]
        N, M = self.N, len(self._edges) - (self.N + 1)
        E, F = self._edges, self._edges[:]
        order = DFSstack = [-1] * (N + max(N, M + 1))
        self.n: int = 0
        self.pos = low = [N] * N
        self.groups: list[list[int]] = []
        visited_cnt = -1
        for v in range(N):
            if order[v] != -1:
                continue
            order[v] = low[v] = visited_cnt = visited_cnt + 1
            DFSstack[N] = F[N] = now = v
            d = t = N
            while True:  #ループ中は常に DFSstack[d] == now を満たす
                i = E[now]
                if i != -1:
                    E[now], nxt = E[i] >> 31, E[i] & 0x7FFFFFFF
                    if order[nxt] == -1:
                        order[nxt] = low[nxt] = visited_cnt = visited_cnt + 1
                        d += 1
                        t += 1
                        DFSstack[d] = F[t] = now = nxt
                    elif low[now] > order[nxt]:
                        low[now] = order[nxt]
                else:
                    if order[now] == (low_now := low[now]):
                        start_t = t
                        while True:
                            nxt = F[t]
                            t -= 1
                            low[nxt], order[nxt] = ~ self.n, 0x7FFFFFFF
                            if nxt == now:
                                self.groups.append(F[t + 1: start_t + 1])
                                self.n += 1
                                break
                    if d == N:
                        break
                    d -= 1
                    now = DFSstack[d]
                    if low[now] > low_now:
                        low[now] = low_now
        for now in range(N):
            E[now] = F[now]
            low[now] += self.n
        self.groups.reverse()
        self._create_graph(make_adjacency_list, order)
    def _create_graph(self, make_adjacency_list: bool, order: list[int]) -> None:
        if make_adjacency_list:
            N, E, low = self.N, self._edges, self.pos
            self.G: list[list[int]] = [[] for _ in range(N)]
            for p, group_p in enumerate(self.groups):
                order[p] = 0
                order[N], d = p, N
                G_p_append = self.G[p].append
                for now in group_p:
                    i = E[now]
                    while i != -1:
                        i, q = E[i] >> 31, low[ E[i] & 0x7FFFFFFF ]
                        if order[q]:
                            d += 1
                            order[q], order[d] = 0, q
                            G_p_append(q)
                while d >= N:
                    order[order[d]] = 1
                    d -= 1

    #基本機能             
    def add_edge(self, now: int, nxt: int) -> None:
        '頂点now → 頂点nxt に向かう有向辺を追加します。'
        assert 0 <= now < self.N and 0 <= nxt < self.N, f'{now = }, {nxt = }'
        self._edges.append(self._edges[now] << 31 | nxt)
        self._edges[now] = len(self._edges) - 1
    def scc(self, make_adjacency_list: bool = False) -> list[list[int]]:
        '''
        強連結成分分解を実行し、self.n, self.pos[now], self.groups[i]の値を計算します。
        返り値は self.groups: トポロジカルソート後の強連結成分の二次元リスト です。
        更に make_adjacency_list: bool = True の場合、頂点縮約後の隣接リストを生成し、
        self.G に二次元リストとして格納します。

        時間・空間計算量: 辺数をMとして、SCC・縮約グラフGの作成どちらも O(N + M)
        '''
        self._SCC_Tarjan(make_adjacency_list)
        return self.groups
