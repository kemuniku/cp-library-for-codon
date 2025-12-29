#Lowlink
class LowLink:
    '''
    LowLink for codon, PyPy3
    二重辺連結成分分解をO(N + M)で実行し、以下の配列を登録します。
    parent[now]: DFS木(森)をひとつ固定したときの、木上の親(根の場合、-1)
    odr[now]: DFS到達順
    low[now]: 後退辺を1回以下使用して到達できる、min(odr)
    A[now]: グラフから頂点now(と接続する辺)を削除した時の、連結成分数の変化量
            孤立点ならば-1, 関節点(articulation)ならば+1以上

    G: 無向グラフの隣接リスト  多重辺・自己ループがあってもよい
    '''
    parent: list[int]
    odr: list[int]
    low: list[int]
    A: list[int]
    __slots__ = ('parent', 'odr', 'low', 'A')
    def __init__(self, G: list[list[int]]) -> None:
        assert len(G) < 2 ** 31 - 1
        N, DFS_count = len(G), -1
        odr, low, A_f_parent, stack = [-1] * N, [-1] * N, [0x7FFFFFFF] * N, [0] * N
        for p in range(N):
            if odr[p] != -1:
                continue
            A_f_parent[p] -= 0x100000000  #1 << 32
            stack[0], d = p << 31 | 0x7FFFFFFF, 1  #(1 << 31) - 1
            while d:
                d -= 1
                x: int = stack[d] if d < N else stack.pop()
                if x >= 0:  #入りがけの処理
                    now, back = x >> 31, x & 0x7FFFFFFF
                    if odr[now] != -1:  #先行辺・後退辺共通
                        low[back] = min(low[back], odr[now])
                        continue
                    odr[now] = low[now] = DFS_count = DFS_count + 1
                    A_f_parent[now] = A_f_parent[now] >> 31 << 31 | back
                    if d < N: stack[d] = ~ x
                    else: stack.append(~ x)
                    d += 1
                    for nxt in G[now]:  #多重辺: 逆辺を1回だけ無視して判定
                        if nxt == back and A_f_parent[now] >> 31 & 1 == 0:
                            A_f_parent[now] |= 0x80000000  #1 << 31
                            continue
                        if d < N: stack[d] = nxt << 31 | now
                        else: stack.append(nxt << 31 | now)
                        d += 1
                else:  #出がけの処理
                    now, back = (~ x) >> 31, (~ x) & 0x7FFFFFFF
                    if back == 0x7FFFFFFF:
                        continue  #assert now == p
                    if odr[back] <= low[now]:
                        A_f_parent[back] += 0x100000000
                    low[back] = min(low[back], low[now])
        #実行後に配列を整理: A_f_parent を A, parent に分割
        self.odr, self.low, self.A, self.parent = odr, low, A_f_parent, stack
        for now, Ai in enumerate(A_f_parent):
            self.A[now], self.parent[now] = Ai >> 32, Ai & 0x7FFFFFFF
            if self.parent[now] == 0x7FFFFFFF:
                self.parent[now] = -1
    def find_bridge(self) -> list[tuple[int, int]]:
        '''
        無向グラフGにおける橋を列挙し、[(Ui, Vi), ･･･] の形で橋の端点を列挙します。
        橋の列挙順は未定義ですが、 タプル内の順序について Ui < Vi を保障します。
        '''
        #nowの親をback := parent[now] としたとき、常に odr[back] < odr[now] を満たす
        #このとき、橋の条件は 木辺 かつ odr[back] < odr[now]
        return [(now, back) if now < back else (back, now)
                for now, back in enumerate(self.parent)
                if back != -1 and self.odr[back] < self.low[now]]
    def is_articulation(self) -> list[bool]:
        '''
        各頂点に対し、B[now]: 頂点nowが関節点ならTrue を返します。
        頂点nowが孤立点の場合、Falseとします。
        なお、self.Aには頂点削除時の連結成分数の変化量が入っています。
        より多くの情報が必要な場合、self.Aを参照してください。
        '''
        return [Ai > 0 for Ai in self.A]
