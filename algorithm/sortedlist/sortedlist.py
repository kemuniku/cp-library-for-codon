#SortedList for codon (based on SkipList)
from random import getrandbits as _SortedList_getrandbits
class SortedList[T]:
    '''
    SkipListを使用した順序つき多重集合のライブラリです。
    本実装では同じキーを重複して保持せず、個数カウントとして統合します。
    期待時間計算量: O(logN) / クエリ 最悪時間計算量: O(N) / クエリ
    期待空間計算量: O(N)  最悪空間計算量: O(NlogN)
    '''
    logN_GROWTH_FACTOR: int = 2  #動作不良 __init__で再代入する
    
    _len: int
    _logN: int
    _kind_value: int
    _next_increase_logN_size: int
    _val: list[T]
    _skipid: list[int]
    _skip: list[int]
    _freeid: list[int]
    _isfree: int
    _last_i: int
    _last_dist: int
    _last_nxt_i: int
    _path: list[int]
    __slots__ = ('_len', '_logN', '_kind_value', '_next_increase_logN_size',
                 '_val', '_skipid', '_skip', '_freeid', '_isfree',
                 '_last_i', '_last_dist', '_last_nxt_i', '_path')
    def __init__(self) -> None:
        #val[i]: カーソルiに対応した値  val[0]はダミー領域
        #skipid[i]: val[i]が集合内に存在する場合、カーソルiに対応する左端(高さ0)の番号
        #           存在しない場合、(対応するskip[now]の左端, この次のfreeid[h]の値)
        #skip[now]: SkipListのノード番号nowの(右のカーソルi << 32 | ノードの区間幅)
        #           ただし 0 <= now <= logN の場合、各高さの探索開始点のリンクとする
        #           このノードが未使用領域の場合、-1を割り振る
        #freeid[h]: 最後に使用した際のノードの高さがhだったようなカーソルi  なければ0
        #last_i, last_dist, last_nxt_i: 最終検索履歴。関数終了時に常に以下を維持する:
        #  last_i = 0 の時、val[last_i] = - inf
        #  last_nxt_i = 0 の時、val[last_nxt_i] = + inf と定義する。
        #   1. val[last_i] の次に大きい値は val[last_nxt_i]
        #   2. val[last_i] より真に小さい値の個数は last_dist
        #   3. path[h] には高さhにおける、val[last_nxt_i]を超えない最大値の情報が入る
        self._len = self._logN = self._kind_value = 0
        self._next_increase_logN_size = self.logN_GROWTH_FACTOR = 2  #再代入
        self._val: list[T] = []
        self._skipid: list[int] = [0]
        self._skip: list[int] = [0]
        self._freeid: list[int] = [0]
        self._isfree = self._last_i = self._last_dist = self._last_nxt_i = 0
        self._path: list[int] = [0]
    def __init__(self, A: generator[T]) -> None:
        self.__init__()
        for Ai in A:
            self._SortedList_add(Ai, 1)
    def __init__(self, A: list[T]) -> None:
        self.__init__()
        for Ai in A:
            self._SortedList_add(Ai, 1)
    #内部関数: 便利系
    def _merge_add(self: SortedList[T], other: SortedList[T]) -> SortedList[T]:  #加算(+): 互いの出現回数の総和
        new_SL = SortedList()
        for v, a in self._generate_items():
            new_SL.add(v, a)
        for v, a in other._generate_items():
            new_SL.add(v, a)
        return new_SL
    def _inplace_add(self: SortedList[T], other: SortedList[T]) -> SortedList[T]:
        for v, a in other._generate_items():
            self.add(v, a)
        return self
    def _merge_or(self: SortedList[T], other: SortedList[T]) -> SortedList[T]:  #和集合(|): 互いの出現回数の最大値
        new_SL = SortedList()
        A = self.items()
        cur = 0
        for v, a in other._generate_items():
            while cur < len(A) and A[cur][0] < v:
                new_SL.add(A[cur][0], A[cur][1])
                cur += 1
            if cur < len(A) and A[cur][0] == v:
                new_SL.add(v, max(A[cur][1], a))
                cur += 1
            new_SL.add(v, a)
        while cur < len(A):
            new_SL.add(A[cur][0], A[cur][1])
            cur += 1
        return new_SL
    def _inplace_or(self: SortedList[T], other: SortedList[T]) -> SortedList[T]:
        for v, a in other._generate_items():
            c = self.count(v)
            if c < a:
                self.add(v, a - c)
        return self
    def _merge_and(self: SortedList[T], other: SortedList[T]) -> SortedList[T]:  #積集合(&): 互いの出現回数の最小値
        new_SL = SortedList()
        A = self.items()
        cur = 0
        for v, a in other._generate_items():
            while cur < len(A) and A[cur][0] < v:
                cur += 1
            if cur < len(A) and A[cur][0] == v:
                new_SL.add(v, min(A[cur][1], a))
                cur += 1
            if cur == len(A):
                break
        return new_SL
    def _inplace_and(self: SortedList[T], other: SortedList[T]) -> SortedList[T]:
        A = self.items()
        cur = 0
        for v, a in other._generate_items():
            while cur < len(A) and A[cur][0] < v:
                self.remove(A[cur][0], A[cur][1])
                cur += 1
            if cur < len(A) and A[cur][0] == v:
                self.discard(v, A[cur][1] - min(A[cur][1], a))
                cur += 1
        while cur < len(A):
            self.remove(A[cur][0], A[cur][1])
            cur += 1
        return self
    def _all_list_clear(self) -> None:
        self._len = self._logN = self._kind_value = 0
        self._next_increase_logN_size = self.logN_GROWTH_FACTOR
        self._val.clear()
        self._skipid.clear(); self._skipid.append(0)
        self._skip.clear(); self._skip.append(0)
        self._freeid.clear(); self._freeid.append(0)
        self._isfree = self._last_i = self._last_dist = self._last_nxt_i = 0
        self._path.clear(); self._path.append(0)
    def _generate_items(self) -> generator[tuple[T, int]]:
        now_i: int = self._skip[0] >> 32
        while now_i:
            x = self._skipid[now_i]
            nxt_i, w = self._skip[x] >> 32, self._skip[x] & 0xFFFFFFFF
            yield (self._val[now_i], w)
            now_i = nxt_i
    #内部関数: 値の検索
    def _update_path_val(self, value: T) -> None:
        #再検索の必要性を確認
        if ((self._last_i == 0 or self._val[self._last_i] < value) and
            (self._last_nxt_i == 0 or value <= self._val[self._last_nxt_i])):
            return
        #再検索  期待計算量 O(logN)
        dist = offset = i = nxt_i = 0
        h = now = self._logN
        while h >= 0:
            nxt_i, w = self._skip[now] >> 32, self._skip[now] & 0xFFFFFFFF
            if nxt_i and self._val[nxt_i] < value:
                i = nxt_i
                now = self._skipid[i] + h
                dist += w
            else:
                self._path[h] = now << 32 | (dist - offset)
                now -= 1
                h -= 1
                offset = dist
        self._last_i, self._last_dist, self._last_nxt_i = i, dist, nxt_i
    def _SortedList_bisect(self, value: T, bRight: bool) -> int:
        self._update_path_val(value)
        ans = self._last_dist + (self._skip[self._path[0] >> 32] & 0xFFFFFFFF)
        if bRight and self._last_nxt_i and self._val[self._last_nxt_i] == value:
            ans += self._skip[self._skipid[self._last_nxt_i]] & 0xFFFFFFFF
        return ans
    def _SortedList_prev_val(self, value: T, allow_equal: bool) -> Optional[T]:
        self._update_path_val(value)
        if allow_equal and self._last_nxt_i and self._val[self._last_nxt_i] == value:
            return value
        elif self._last_i == 0:
            return None
        else:
            return self._val[self._last_i]
    def _SortedList_next_val(self, value: T, allow_equal: bool) -> Optional[T]:
        self._update_path_val(value)
        nxt_i = self._last_nxt_i
        if nxt_i and self._val[nxt_i] == value:
            if allow_equal:
                return value
            nxt_i = self._skip[self._skipid[nxt_i]] >> 32
        if nxt_i:
            return self._val[nxt_i]
        else:
            return None
    #内部関数: add
    def _generate_random_height(self) -> int:  #[0, logN]から重み付けして高さを割り当てる
        n = _SortedList_getrandbits(self._logN)
        n = n & (n + 1) ^ n
        return 64 - n.__ctlz__()  #return n.bit_length()
    def _prepare_new_node(self) -> tuple[int, int, int]:
        #新ノードの(高さh, 新規カーソルi, skipの空き領域の左端cur) を返す
        h = self._generate_random_height()  #[0, logN]
        if len(self._val) == 0 or self._kind_value + 1 == len(self._val):
            i = self._kind_value + 1
            cur = len(self._skip)
            for _ in range(h + 1):
                self._skip.append(-1)
        else:
            #isfreeから(あればh bit目以上の)最小bitを探索し割り振り
            n, k = self._isfree, h
            if n >> k:
                n >>= k
            else:
                k = 0
            k += 63 - (n & - n).__ctlz__()  #k += n.bit_length() - 1
            i = self._freeid[k]
            cur, self._freeid[k] = self._skipid[i] >> 32, self._skipid[i] & 0xFFFFFFFF
            if self._freeid[k] == 0:
                self._isfree ^= 1 << k
            #curを変更 特にcur <= logN の場合も、探索開始点として押収されている
            if h > k or cur <= self._logN:
                cur = len(self._skip)
                for _ in range(h + 1):
                    self._skip.append(-1)
        return (h, i, cur)
    def _increase_logN(self) -> None:  #addから直接呼ぶ  logN += 1を処理  期待O(logN)
        #1. skip[logN + 1]の徴用
        if len(self._skip) == self._logN + 1:
            self._skip.append(-1)
        if self._skip[self._logN + 1] != -1:  #探索開始点として押収
            x = self._skip[self._logN + 1]
            nxt_i, amount = x >> 32, x & 0xFFFFFFFF
            if nxt_i:
                self._update_path_val(self._val[nxt_i])
                self._update_path_val(self._val[self._last_i])
            else:
                self._update_path_val(self.__getitem__(self._len - 1))
            mid_i = self._last_nxt_i
            for h in range(self._logN, -1, -1):  #mid_iの高さを確認
                if self._skip[self._path[h] >> 32] >> 32 == mid_i:
                    break
            #assert all(self._skip[self._path[k] >> 32] >> 32 == mid_i for k in range(h + 1))
            self._skipid[mid_i] = len(self._skip)  #[logN + 1:] → 末尾へ
            for k in range(self._logN + 1, self._logN + 1 + h + 1):
                self._skip.append(self._skip[k])
                self._skip[k] = -1
        #2. logN += 1
        self._next_increase_logN_size *= self.logN_GROWTH_FACTOR
        self._logN += 1
        self._freeid.append(0)
        self._path.append(0)
        h = now = self._logN - 1
        i = Lt_i = 0  #Lt_i: 最後にノード増設を行ったノード番号  探索開始点は0として扱う
        nxt_i, dist_sum = self._skip[now] >> 32, self._skip[now] & 0xFFFFFFFF
        while nxt_i:  #次の処理対象 i := nxt_i が終点0に到達するまで
            i = nxt_i
            now = self._skipid[i] + h
            if _SortedList_getrandbits(0):  #50%の確率で1上げる
                prev_skipid, self._skipid[i] = self._skipid[i], len(self._skip)
                for k in range(prev_skipid, prev_skipid + self._logN):
                    self._skip.append(self._skip[k])
                    self._skip[k] = -1
                self._skip.append(-1)
                self._skip[self._skipid[Lt_i] + self._logN] = i << 32 | dist_sum
                dist_sum = 0
                Lt_i = i
            nxt_i, w = self._skip[now] >> 32, self._skip[now] & 0xFFFFFFFF
            dist_sum += w
        self._skip[self._skipid[Lt_i] + self._logN] = 0 << 32 | dist_sum
        self._last_i = self._last_dist = 0  #念のためpathの値を再更新
        self._last_nxt_i = self._skip[0] >> 32
        for h in range(self._logN + 1):
            self._path[h] = h << 32 | 0
    def _SortedList_add(self, value: T, amount: int) -> None:
        if amount <= 0:
            return
        self._update_path_val(value)
        #value in SortedList
        if self._last_nxt_i and self._val[self._last_nxt_i] == value:
            for h, x in enumerate(self._path):
                now, w = x >> 32, x & 0xFFFFFFFF
                nxt_i = self._skip[now] >> 32
                if nxt_i == self._last_nxt_i:
                    self._skip[self._skipid[nxt_i] + h] += amount
                else:
                    self._skip[now] += amount
            self._len += amount
            return
        #value not in SortedList
        else:
            #logN += 1, 新規ノード割り当て
            if self._kind_value >= self._next_increase_logN_size:
                self._increase_logN()
                self._update_path_val(value)  #再設定
            Ht, new_i, cur = self._prepare_new_node()
            if len(self._val) == 0:  #ダミーノードの設定
                self._val.append(value)  #assert new_i == 1
            if new_i >= len(self._val):
                self._val.append(value)
                self._skipid.append(0)
            self._val[new_i] = value
            self._skipid[new_i] = cur
            self._kind_value += 1
            #手前のノードの値を変更
            dist_sum = self._skip[self._path[0] >> 32] & 0xFFFFFFFF
            h = 0
            while h <= Ht:
                now, d = self._path[h] >> 32, self._path[h] & 0xFFFFFFFF
                nxt_i, w = self._skip[now] >> 32, self._skip[now] & 0xFFFFFFFF
                self._skip[cur + h] = nxt_i << 32 | (w - dist_sum + amount)
                self._skip[now] = new_i << 32 | dist_sum
                dist_sum += d
                h += 1
            while h <= self._logN:
                self._skip[self._path[h] >> 32] += amount
                h += 1
            self._len += amount
            self._last_nxt_i = new_i
    #内部関数: discard
    def _SortedList_discard(self, value: T, amount: int) -> int:
        if amount <= 0:
            return 0
        self._update_path_val(value)
        if self._last_nxt_i == 0 or self._val[self._last_nxt_i] != value:
            return 0
        #h <= Ht := ノードの高さ まで処理を分岐
        h = 0
        nxt_i, nxt_i_skipid = self._last_nxt_i, self._skipid[self._last_nxt_i]
        w = self._skip[nxt_i_skipid] & 0xFFFFFFFF
        if amount < w:  #ノードは残す
            while h <= self._logN:
                if self._skip[self._path[h] >> 32] >> 32 != nxt_i:
                    break
                else:
                    self._skip[nxt_i_skipid + h] -= amount
                    h += 1
        else:  #ノードを削除
            amount = w
            while h <= self._logN:
                now = self._path[h] >> 32
                if self._skip[now] >> 32 != nxt_i:
                    break
                x = self._skip[now] & 0xFFFFFFFF
                self._skip[now] = self._skip[nxt_i_skipid + h] - amount + x
                self._skip[nxt_i_skipid + h] = -1
                h += 1
            self._skipid[nxt_i] = nxt_i_skipid << 32 | self._freeid[h - 1]
            self._freeid[h - 1] = nxt_i
            self._isfree |= 1 << h - 1
            self._last_nxt_i = self._skip[self._path[0] >> 32] >> 32
            self._kind_value -= 1
        #共通処理
        while h <= self._logN:
            self._skip[self._path[h] >> 32] -= amount
            h += 1
        self._len -= amount
        return amount

    #特殊メソッド
    def __len__(self) -> int:
        return self._len
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({list(self)})'
    def __str__(self) -> str:
        return str(list(self))
    def __bool__(self) -> bool:
        return self._len > 0
    def __getitem__(self, i: int) -> T:
        '期待計算量 O(logN)で要素を取得します。'
        if i < 0:
            i += self._len
        if not 0 <= i < self._len:
            raise IndexError('SortedList index out of range.')
        cnt = i
        #検索履歴から判定  O(1)
        w = self._skip[self._skipid[self._last_i]] & 0xFFFFFFFF  #last_iの個数
        if self._last_dist <= i < self._last_dist + w:
            return self._val[self._last_i]
        x = self._skip[self._skipid[self._last_nxt_i]] & 0xFFFFFFFF  #last_nxt_iの個数
        if self._last_dist + w <= i < self._last_dist + w + x:
            return self._val[self._last_nxt_i]
        #再計算して取得  期待計算量 O(logN)
        dist = i = 0
        h = now = self._logN
        while h >= 0:
            nxt_i, w = self._skip[now] >> 32, self._skip[now] & 0xFFFFFFFF
            if nxt_i and dist + w <= cnt:
                i = nxt_i
                now = self._skipid[nxt_i] + h
                dist += w
            else:
                now -= 1
                h -= 1
        return self._val[i]
    def __delitem__(self, i: int) -> None:
        if i < 0:
            i += self._len
        if not 0 <= i < self._len:
            raise IndexError('SortedList index out of range.')
        self.pop(i)
    def __contains__(self, value: T) -> bool:
        '期待計算量 O(logN)で要素の有無を判定します。'
        #検索履歴から判定  O(1)
        if ((self._last_i and self._val[self._last_i] == value) or
            (self._last_nxt_i and self._val[self._last_nxt_i] == value)):
            return True
        #再計算して取得  期待計算量 O(logN)
        self._update_path_val(value)
        return self._last_nxt_i and self._val[self._last_nxt_i] == value
    def __iter__(self) -> generator[T]:
        '計算量 O(size)で要素を列挙します。'
        now_i = self._skip[0] >> 32
        while now_i:
            x = self._skipid[now_i]
            nxt_i, w = self._skip[x] >> 32, self._skip[x] & 0xFFFFFFFF
            for _ in range(w):
                yield self._val[now_i]
            now_i = nxt_i
    def __reversed__(self) -> generator[T]:
        'O(size)でリストを作成してから、逆順に出力します。'
        A = list(self)
        A.reverse()
        for v in A:
            yield v
    #加算(+): 互いの出現回数の総和
    def __add__(self: SortedList[T], other: SortedList[T]) -> SortedList[T]:
        return self._merge_add(other)
    def __iadd__(self: SortedList[T], other: SortedList[T]) -> SortedList[T]:
        return self._inplace_add(other)
    #和集合(|): 互いの出現回数の最大値
    def __or__(self: SortedList[T], other: SortedList[T]) -> SortedList[T]:
        return self._merge_or(other)
    def __ior__(self: SortedList[T], other: SortedList[T]) -> SortedList[T]:
        return self._inplace_or(other)
    #積集合(&): 互いの出現回数の最小値
    def __and__(self: SortedList[T], other: SortedList[T]) -> SortedList[T]:
        return self._merge_and(other)
    def __iand__(self: SortedList[T], other: SortedList[T]) -> SortedList[T]:
        return self._inplace_and(other)
    def clear(self) -> None:
        '配列を初期化します。'
        self._all_list_clear()
    def items(self) -> list[tuple[T, int]]:
        '(値value, 個数amount) を昇順に格納したリストを生成します。'
        return list(self._generate_items())

    #値の検索
    def bisect(self, value: T) -> int:
        '値がvalue以下の要素の個数を返します。'
        return self._SortedList_bisect(value, True)
    def bisect_left(self, value: T) -> int:
        '値がvalue未満の要素の個数を返します。'
        return self._SortedList_bisect(value, False)
    def bisect_right(self, value: T) -> int:
        '値がvalue以下の要素の個数を返します。'
        return self._SortedList_bisect(value, True)
    def prev_value(self, value: T, allow_equal: bool = False) -> Optional[T]:
        '''
        値がvalueより真に小さい最大の要素を返します。存在しない場合、Noneを返します。
        allow_equal = Trueにした場合、value「以下」の最大要素の検索とします。
        '''
        return self._SortedList_prev_val(value, allow_equal)
    def next_value(self, value: T, allow_equal: bool = False) -> Optional[T]:
        '''
        値がvalueより真に大きい最小の要素を返します。存在しない場合、Noneを返します。
        allow_equal = Trueにした場合、value「以上」の最小要素の検索とします。
        '''
        return self._SortedList_next_val(value, allow_equal)
    def count(self, value: T) -> int:
        '値valueの個数を返します。'
        self._update_path_val(value)
        if self._last_nxt_i and self._val[self._last_nxt_i] == value:
            return self._skip[self._skipid[self._last_nxt_i]] & 0xFFFFFFFF
        return 0

    #値の追加・削除
    def add(self, value: T, amount: int = 1) -> None:
        '値valueをamount個追加します。'
        if amount < 0: raise ValueError('amount must be non-negatve')
        if amount > 0: self._SortedList_add(value, amount)
    def discard(self, value: T, amount: int = 1) -> None:
        '値valueを最大amount個削除します。不足していても例外は発生しません。'
        self._SortedList_discard(value, amount)
    def remove(self, value: T, amount: int = 1) -> None:
        '値valueをamount個削除します。不足していた場合、削除後にValueErrorを返します。'
        if amount < 0:
            raise ValueError('amount must be >= 0')
        if amount > 0 and amount != self._SortedList_discard(value, amount):
            raise ValueError(f'value is insufficient')
    def pop(self, i: int = -1) -> T:
        'SortedList[i]の要素を削除して返します。'
        if i < 0: i += self._len
        if self._len == 0:
            raise IndexError('pop from empty SortedList')
        if not 0 <= i < self._len:
            raise IndexError('pop index out of range')
        v = self.__getitem__(i)
        self._SortedList_discard(v, 1)
        return v
