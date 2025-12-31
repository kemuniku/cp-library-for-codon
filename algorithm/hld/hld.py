#HL分解
class HL_decomposition:
    '''
    Heavy - Light decomposition for codon, PyPy3
    N頂点の根つき木をO(logN)個のパスに分解します。

    G: 木の隣接リスト  G[now] = [nxt, ･･･]
    root: 根つき木の根
    '''
    N: int
    _order: list[int]
    _visit: list[int]
    _steps: list[int]
    __slots__ = ('N', '_order', '_visit', '_steps')
    def __init__(self, G: list[list[int]], root: int = 0):
        assert 1 <= len(G) < 2 ** 29 - 1, f'頂点数が多すぎます。{len(G) = }'
        assert 0 <= root < len(G), f'rootの頂点番号が不正です。{root = }, {len(G) = }'
        self.N = N = len(G)
        self._order = order = [0] * N  #order[Ti] = now
        self._visit = visit = [0] * N  #visit[now] = depth << 58 | size << 29 | Ti
        self._steps = steps = [root << 29 | N] * N  #steps[Ti]: Hv.左端 << 29 | 左端の親
        stack: list[int] = [root << 29 | N] * N
        d: int = 1
        for x in stack:
            now, back = x >> 29, x & 0x1FFFFFFF
            visit[now] = 0x20000000  #1 << 29
            for nxt in G[now]:
                if visit[nxt] == 0:
                    stack[d] = nxt << 29 | now
                    d += 1
        for d in range(N - 1, 0, -1):  #size[back] += size[now]
            visit[stack[d] & 0x1FFFFFFF] += visit[stack[d] >> 29]
        stack[0] = 1 << 58 | root << 29 | N
        d: int = 1
        for Ti in range(N):
            d -= 1
            f, now, Lt = stack[d] >> 58, stack[d] >> 29 & 0x1FFFFFFF, stack[d] & 0x1FFFFFFF
            visit[now] |= Ti
            order[Ti] = now
            depth_now, size_now = visit[now] >> 58, visit[now] >> 29 & 0x1FFFFFFF
            if f == 1:  #Lt.edgeを移動してきた場合
                steps[Ti], Lt = Ti << 29 | Lt, Ti
            else:
                steps[Ti] = steps[Lt]
            size_max = leader = 0
            for nxt in G[now]:
                size_nxt: int = visit[nxt] >> 29 & 0x1FFFFFFF
                if size_nxt > size_now:  #nxtがnowの親の場合
                    continue
                if size_max < size_nxt:
                    if size_max != 0:  #Hv.edge候補のleaderを修正
                        visit[leader] |= (depth_now + 1) << 58
                        stack[d] = 1 << 58 | leader << 29 | Ti
                        d += 1
                    size_max, leader = size_nxt, nxt
                else:
                    visit[nxt] |= (depth_now + 1) << 58
                    stack[d] = 1 << 58 | nxt << 29 | Ti  #depth + 1っぽいけど
                    d += 1
            if size_max > 0:
                visit[leader] |= depth_now << 58
                stack[d] = leader << 29 | Lt
                d += 1

    #基本機能: 返り値が頂点や時刻でないもの
    def size(self, Vi: int) -> int:
        '根つき木Gにおける、頂点Viの部分木の大きさを返します。'
        assert 0 <= Vi < self.N
        return self._visit[Vi] >> 29 & 0x1FFFFFFF
    def depth(self, Vi: int) -> int:
        '根rootから頂点Viの経路中にある、Light edgeの個数を返します。'
        assert 0 <= Vi < self.N
        return self._visit[Vi] >> 58

    #基本機能: 返り値が頂点番号
    def vertice(self, Ti: int) -> int:
        '到達順がTiである頂点番号を取得します。self._order[Ti]へのアクセスと同値です。'
        assert 0 <= Ti < self.N
        return self._order[Ti]
    def parent(self, Vi: int) -> int:
        '頂点Viの親を返します。Vi == root の場合、代わりに-1を返します。'
        assert 0 <= Vi < self.N
        Tv: int = self.time(Vi)
        Lt, Pt = self._steps[Tv] >> 29, self._steps[Tv] & 0x1FFFFFFF
        assert Lt <= Tv and (Pt == self.N or Pt < Tv)
        return -1 if Tv == 0 else self._order[(Tv - 1) if Lt < Tv else Pt]

    def LCA(self, Ui: int, Vi: int) -> int:
        '根つき木Gにおいて、頂点Uiと頂点Viの最小共通祖先となる頂点を求めます。'
        assert 0 <= Ui < self.N and 0 <= Vi < self.N
        du, Tu = self._visit[Ui] >> 58, self._visit[Ui] & 0x1FFFFFFF
        dv, Tv = self._visit[Vi] >> 58, self._visit[Vi] & 0x1FFFFFFF
        while du > dv:
            Tu = self._steps[Tu] & 0x1FFFFFFF
            du -= 1
        while du < dv:
            Tv = self._steps[Tv] & 0x1FFFFFFF
            dv -= 1
        while self._steps[Tu] >> 29 != self._steps[Tv] >> 29:
            Tu, Tv = self._steps[Tu] & 0x1FFFFFFF, self._steps[Tv] & 0x1FFFFFFF
        return self._order[min(Tu, Tv)]

    #基本機能: 返り値が時刻
    def time(self, Vi: int) -> int:
        '''
        頂点Viの到達時刻Tiを返します。ここで、0 <= Ti < N を満たします。
        頂点Uiと頂点Viを結ぶパスに対して作用積を計算したい場合、
        時刻 max( time(Ui), time(Vi) ) に作用を行ってください。
        '''
        assert 0 <= Vi < self.N
        return self._visit[Vi] & 0x1FFFFFFF
    def subtree(self, Vi: int) -> tuple[int, int]:
        '根つき木Gにおける、頂点Viの部分木に対応する時刻の区間[Tin, Tout)を返します。'
        assert 0 <= Vi < self.N
        time_Vi, size_Vi = self._visit[Vi] & 0x1FFFFFFF, self._visit[Vi] >> 29 & 0x1FFFFFFF
        return (time_Vi, time_Vi + size_Vi)
    def fold(self, Ui: int, Vi: int) -> tuple[
        list[tuple[int, int]], list[tuple[int, int]], int]:
        '''
        Ui → Viのパスの作用区間を取得します。
        返り値は ( upward, downward, time_LCA ) のタプルとなります。
        外部データ構造でパスの作用積を計算したい場合、
        upward[0, 1, ･･･] * A[time_LCA] * downward[0, 1, ･･･] の順に計算してください。
        
        upward: LCA ← Ui の方向のHv.edgeを、Uiに近い順に列挙します。
                返り値は[(Lt, Rt)] のタプルで、Lt, RtはHv.edgeに対応する時刻です。
                これまでの作用積 * prod[Lt ← Rt) と合成してください。
                右から左への合成には、f(Lt, Rt): return Rt * Lt のような引数反転を推奨します。
        downward: LCA → Vi の方向のHv.edgeを、LCAに近い順に列挙します。
                これまでの作用積 * prod[Lt → Rt) と合成してください。
        '''
        assert 0 <= Ui < self.N and 0 <= Vi < self.N
        steps: list[int] = self._steps
        upward: list[tuple[int, int]] = []
        downward: list[tuple[int, int]] = []
        du, Tu = self._visit[Ui] >> 58, self._visit[Ui] & 0x1FFFFFFF
        dv, Tv = self._visit[Vi] >> 58, self._visit[Vi] & 0x1FFFFFFF
        Lu, Tw = self._steps[Tu] >> 29, self._steps[Tu] & 0x1FFFFFFF
        Lv, Tx = self._steps[Tv] >> 29, self._steps[Tv] & 0x1FFFFFFF
        while du > dv:
            upward.append((Lu, Tu + 1))
            Tu, Lu, Tw = Tw, steps[Tw] >> 29, steps[Tw] & 0x1FFFFFFF
            du -= 1
        while du < dv:
            downward.append((Lv, Tv + 1))
            Tv, Lv, Tx = Tx, steps[Tx] >> 29, steps[Tx] & 0x1FFFFFFF
            dv -= 1
        while Lu != Lv:
            upward.append((Lu, Tu + 1))
            downward.append((Lv, Tv + 1))
            Tu, Lu, Tw = Tw, steps[Tw] >> 29, steps[Tw] & 0x1FFFFFFF
            Tv, Lv, Tx = Tx, steps[Tx] >> 29, steps[Tx] & 0x1FFFFFFF
        if Tu > Tv:
            upward.append((Tv + 1, Tu + 1))
        elif Tu < Tv:
            downward.append((Tu + 1, Tv + 1))
        downward.reverse()
        return (upward, downward, min(Tu, Tv))
