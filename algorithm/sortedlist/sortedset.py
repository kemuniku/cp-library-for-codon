#SortedSet for codon (based on SkipList)
from random import getrandbits as _SortedSet_getrandbits
class SortedSet[T]:
    '''
    SkipListを用いた順序付き集合です。重複したキーは保持しません。
    時間計算量: 期待 O(logN) / クエリ  最悪 O(N) / クエリ
    空間計算量: 期待 O(N)  最悪 O(NlogN)
    '''
    logN_GROWTH_FACTOR = 2

    _len: int
    _logN: int
    _next_increase_logN_size: int
    _val: list[T]
    _skip: list[int]
    _freeid: list[int]
    _isfree: int
    _last_i: int
    _last_dist: int
    _last_nxt_i: int
    _path: list[int]
    __slots__ = ('_len', '_logN', '_next_increase_logN_size', '_val', '_skip',
                 '_freeid', '_isfree', '_last_i', '_last_dist', '_last_nxt_i', '_path')
    def __init__(self) -> None:
        #val[i]: カーソルiに対応した値  val[0]はダミー領域
        #skip[now]: SkipListのノード番号nowの(右の基準ノード << 32 | ノードの区間幅)
        #           ただし 0 <= now <= logN の場合、各高さの探索開始点のリンクとする
        #           未使用先頭ノードなら、~ (対応カーソル位置i << 32 | 直前のfreeid[h])
        #freeid[h]: 削除時の高さがhであったような、最後に削除した要素のノード領域左端
        #last_i, last_dist, last_nxt_i: 最終検索履歴
        #  last_i == 0 の時、val[last_i] = - inf
        #  last_nxt_i == 0 の時、val[last_nxt_i] = + inf と定義する。このとき
        #   1. now = path[0] >> 32 として、skip[now] & 0xFFFFFFFF == last_i
        #   2. nxt = skip[now] >> 32 として、skip[nxt] & 0xFFFFFFFF == last_nxt_i
        #   3. last_dist == val[last_i] 未満の値の個数
        self._len = self._logN = 0
        self._next_increase_logN_size = SortedSet.logN_GROWTH_FACTOR
        self._val: list[T] = []
        self._skip: list[int] = [0]
        self._freeid: list[int] = [0]
        self._isfree = self._last_i = self._last_dist = self._last_nxt_i = 0
        self._path: list[int] = [0]
    def __init__(self, A: generator[T]) -> None:
        self.__init__()
        for Ai in A: self.add(Ai)
    def __init__(self, A: list[T]) -> None:
        self.__init__()
        for Ai in A: self.add(Ai)
    #内部関数: 便利機能
    def _all_clear(self) -> None:
        self._len = self._logN = 0
        self._next_increase_logN_size = SortedSet.logN_GROWTH_FACTOR
        self._val.clear()
        self._skip.clear(); self._skip.append(0)
        self._freeid.clear(); self._freeid.append(0)
        self._isfree = self._last_i = self._last_dist = self._last_nxt_i = 0
        self._path.clear(); self._path.append(0)
    #内部関数: 値の検索
    def _update_path_val(self, value: T) -> None:  #直右にvalue以上の値を捉える
        if ((self._last_i == 0 or self._val[self._last_i] < value) and
            (self._last_nxt_i == 0 or value <= self._val[self._last_nxt_i])):
            return
        dist = offset = i = nxt_i = now = 0
        h = self._logN
        while h >= 0:
            nxt, w = self._skip[now + h] >> 32, self._skip[now + h] & 0xFFFFFFFF
            if h == 0: w = 1
            nxt_i = self._skip[nxt] & 0xFFFFFFFF
            if nxt and self._val[nxt_i] < value:
                i, now = nxt_i, nxt
                dist += w
            else:
                self._path[h] = now << 32 | (dist - offset)
                h -= 1; offset = dist
        self._last_i, self._last_dist, self._last_nxt_i = i, dist, nxt_i
    def _update_path_cnt(self, cnt: int) -> None:  #直右に0-indexedでcnt番目の値を捉える
        assert 0 <= cnt < self._len
        if self._last_dist == cnt: return
        dist = offset = i = nxt_i = now = 0
        h = self._logN
        while h >= 0:
            nxt, w = self._skip[now + h] >> 32, self._skip[now + h] & 0xFFFFFFFF
            if h == 0: w = 1
            nxt_i = self._skip[nxt] & 0xFFFFFFFF
            if nxt and dist + w <= cnt:  #ここを変更
                i, now = nxt_i, nxt
                dist += w
            else:
                self._path[h] = now << 32 | (dist - offset)
                h -= 1; offset = dist
        self._last_i, self._last_dist, self._last_nxt_i = i, dist, nxt_i
    def _SortedSet_bisect(self, value: T, bRight: bool) -> int:
        self._update_path_val(value)
        if bRight and self._last_nxt_i and self._val[self._last_nxt_i] == value:
            return self._last_dist + 1
        else: return self._last_dist
    def _SortedSet_prev_val(self, value: T, allow_equal: bool) -> Optional[T]:
        self._update_path_val(value)
        if allow_equal and self._last_nxt_i and self._val[self._last_nxt_i] == value:
            return value
        elif self._last_i == 0: return None
        else: return self._val[self._last_i]
    def _SortedSet_next_val(self, value: T, allow_equal: bool) -> Optional[T]:
        self._update_path_val(value)
        nxt_i = self._last_nxt_i
        if nxt_i and self._val[nxt_i] == value:
            if allow_equal: return value
            nxt = self._skip[ self._path[0] >> 32 ] >> 32
            nxt_i = self._skip[ self._skip[nxt] >> 32 ] & 0xFFFFFFFF
        if nxt_i: return self._val[nxt_i]
        else: return None  
    #内部関数: add
    def _generate_random_height(self) -> int:  #[0, logN]から重み付けして高さを割り当てる
        n = _SortedSet_getrandbits(self._logN)
        n = n & (n + 1) ^ n
        return 64 - n.__ctlz__()  #n.bit_length()
    def _prepare_new_node(self) -> tuple[int, int, int]:
        #新ノードの(高さh, 新規カーソルi, skipの空き領域の左端cur) を返す
        h = self._generate_random_height()
        if self._isfree == 0:  #空きスロットがない状態
            i, cur = max(1, len(self._val)), len(self._skip)
        else:  #適切なノードを選択
            n, k = self._isfree, h
            if n >> k: n >>= k
            else: k = 0
            k += 63 - (n & - n).__ctlz__()  #(n & - n).bit_length() - 1
            cur = self._freeid[k]
            if cur <= self._logN:  #特殊分岐: increase_logNで押収済。freeid[k]はすべて破棄
                self._freeid[k] = 0
                self._isfree ^= 1 << k
                i, cur = max(1, len(self._val)), len(self._skip)
            else:
                x = ~ self._skip[cur]
                i, self._freeid[k] = x >> 32, x & 0xFFFFFFFF
                self._skip[cur] = -1
                if self._freeid[k] == 0:
                    self._isfree ^= 1 << k
                if h > k: cur = len(self._skip)
        if cur == len(self._skip):
            for _ in range(h + 1): self._skip.append(-1)
        return (h, i, cur)
    def _increase_logN(self) -> None:
        if len(self._skip) == self._logN + 1:
            self._skip.append(-1)
        p = self._logN + 1  #skip[logN + 1]の枠を開ける
        if self._skip[p] != -1:
            if self._skip[p] >> 32 >= 0:
                nxt, now_i = self._skip[p] >> 32, self._skip[p] & 0xFFFFFFFF
                self._update_path_val(self._val[now_i])  #assert self._last_nxt_i == now_i
                tail, h = len(self._skip), 0  #prev → logN + 1 の辺を prev → tail に張り直し
                while h <= self._logN:
                    prev = self._path[h] >> 32
                    nxt, prev_i = self._skip[prev + h] >> 32, self._skip[prev + h] & 0xFFFFFFFF
                    if nxt != p: break
                    self._skip[prev + h] = tail << 32 | prev_i
                    self._skip.append(self._skip[p + h])
                    self._skip[p + h] = -1
                    h += 1
            else: self._skip[p] = -1  #assert self._skip[p] < -1
        #logN += 1
        self._next_increase_logN_size *= SortedSet.logN_GROWTH_FACTOR
        self._logN += 1
        self._freeid.append(0)      
        self._path.append(0)  #なんでもいい
        h = self._logN - 1  #hのデータを基に、高さlogNのデータを作成
        now = last_now = 0
        nxt, dist_sum = self._skip[now + h] >> 32, self._skip[now + h] & 0xFFFFFFFF
        if h == 0: dist_sum = 1
        while nxt:  #移動先が終点となるまで
            back, now = now, nxt
            if _SortedSet_getrandbits(0):  #50%の確率でノードnowの高さを1上げる
                #prev → now を prev → cur(:= len(self._skip)) に張り直し
                cur = len(self._skip)
                for t in range(self._logN):
                    self._skip.append(self._skip[now + t])
                    self._skip[now + t] = -1
                t, prev = self._logN - 1, back
                while t >= 0:
                    if self._skip[prev + t] >> 32 != now:
                        prev = now
                    else:
                        self._skip[prev + t] = cur << 32 | (self._skip[prev + t] & 0xFFFFFFFF)
                        t -= 1
                self._skip[last_now + self._logN] = cur << 32 | dist_sum
                dist_sum = 0
                last_now = now = cur
            nxt, w = self._skip[now + h] >> 32, self._skip[now + h] & 0xFFFFFFFF
            if h == 0: w = 1
            dist_sum += w
        self._skip[last_now + self._logN] = 0 << 32 | dist_sum
        #念のため初期化
        self._last_i = self._last_dist = 0
        self._last_nxt_i = self._skip[ self._skip[0] >> 32 ] & 0xFFFFFFFF
        for h in range(self._logN + 1): self._path[h] = 0
    def _SortedSet_add(self, value: T) -> None:
        self._update_path_val(value)
        if self._last_nxt_i and self._val[self._last_nxt_i] == value:
            return  #val in SortedSet
        #logN += 1の処理
        if self._len >= self._next_increase_logN_size:
            self._increase_logN()
            self._update_path_val(value)  #即座に再設定
        #ノードの割り当て
        Ht, new_i, cur = self._prepare_new_node()
        if len(self._val) == 0: self._val.append(value)  #ダミーノードの設定
        if new_i == len(self._val): self._val.append(value)
        self._val[new_i] = value
        now, d = self._path[0] >> 32, self._path[0] & 0xFFFFFFFF
        nxt, now_i = self._skip[now] >> 32, self._skip[now] & 0xFFFFFFFF
        self._skip[now] = cur << 32 | now_i  #now → cur → nxt とつなぎ直し
        self._skip[cur] = nxt << 32 | new_i
        dist_sum = d + 1
        h = 1
        while h <= Ht:
            now, d = self._path[h] >> 32, self._path[h] & 0xFFFFFFFF
            nxt, w = self._skip[now + h] >> 32, self._skip[now + h] & 0xFFFFFFFF
            self._skip[cur + h] = self._skip[now + h] + 1 - dist_sum
            self._skip[now + h] = cur << 32 | dist_sum
            dist_sum += d
            h += 1
        while h <= self._logN:
            now = self._path[h] >> 32
            self._skip[now + h] += 1
            h += 1
        self._len += 1
        self._last_nxt_i = new_i
    def _SortedSet_discard(self, value: T) -> bool:  #SortedListから変更: 返り値はbool値
        self._update_path_val(value)
        if self._last_nxt_i == 0 or self._val[self._last_nxt_i] != value:
            return False  #val not in SortedSet
        #削除対象のノード番号をtargetとして記録
        now = self._path[0] >> 32
        target, now_i = self._skip[now] >> 32, self._skip[now] & 0xFFFFFFFF
        double_nxt = self._skip[target] >> 32
        last_nxt_i = self._last_nxt_i
        self._skip[now] = double_nxt << 32 | now_i
        self._last_nxt_i = self._skip[double_nxt] & 0xFFFFFFFF
        h = 1
        while h <= self._logN:
            now = self._path[h] >> 32
            nxt, w = self._skip[now + h] >> 32, self._skip[now + h] & 0xFFFFFFFF
            if nxt != target: break
            else:
                self._skip[now + h] = self._skip[target + h] + (w - 1)
                self._skip[target + h] = -1
                h += 1
        #ノード削除
        self._skip[target] = ~ (last_nxt_i << 32 | self._freeid[h - 1])
        self._freeid[h - 1] = target
        self._isfree |= 1 << h - 1

        #3. 残りの処理
        while h <= self._logN:
            now = self._path[h] >> 32
            self._skip[now + h] -= 1
            h += 1
        self._len -= 1
        return True
                
    #特殊メソッド
    def __len__(self) -> int:
        return self._len
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({list(self)})'
    def __str__(self) -> str:
        return '{' + str(list(self))[1: -1] + '}'
    def __bool__(self) -> bool:
        return self._len > 0
    def __getitem__(self, i: int) -> T:
        if i < 0:
            i += self._len
        if not 0 <= i < self._len:
            raise IndexError('SortedSet index out of range')
        self._update_path_cnt(i)
        return self._val[self._last_nxt_i]
    def __delitem__(self, i: int) -> None:
        if i < 0:
            i += self._len
        if not 0 <= i < self._len:
            raise IndexError('SortedSet index out of range')
        self.pop(i)
    def __contains__(self, value: T) -> bool:
        '期待計算量 O(logN)で要素の有無を判定します。'
        self._update_path_val(value)
        return self._last_nxt_i and self._val[self._last_nxt_i] == value
    def __reversed__(self) -> generator[T]:
        'O(size)でリストを作成してから、逆順に出力します。'
        A = list(self)
        A.reverse()
        for v in A: yield v
    def __iter__(self) -> generator[T]:
        now = self._skip[0] >> 32
        while now:
            nxt, now_i = self._skip[now] >> 32, self._skip[now] & 0xFFFFFFFF
            yield self._val[now_i]
            now = nxt
    def clear(self) -> None:
        '配列を初期化します。'
        self._all_clear()
        
    #値の検索
    def bisect(self, value: T) -> int:
        '値がvalue以下の要素の個数を返します。'
        return self._SortedSet_bisect(value, True)
    def bisect_left(self, value: T) -> int:
        '値がvalue未満の要素の個数を返します。'
        return self._SortedSet_bisect(value, False)
    def bisect_right(self, value: T) -> int:
        '値がvalue以下の要素の個数を返します。'
        return self._SortedSet_bisect(value, True)
    def prev_value(self, value: T, allow_equal: bool = False) -> Optional[T]:
        '''
        値がvalueより真に小さい最大の要素を返します。存在しない場合、Noneを返します。
        allow_equal = Trueにした場合、value「以下」の最大要素の検索とします。
        '''
        return self._SortedSet_prev_val(value, allow_equal)
    def next_value(self, value: T, allow_equal: bool = False) -> Optional[T]:
        '''
        値がvalueより真に大きい最小の要素を返します。存在しない場合、Noneを返します。
        allow_equal = Trueにした場合、value「以上」の最小要素の検索とします。
        '''
        return self._SortedSet_next_val(value, allow_equal)

    #値の追加・削除
    def add(self, value: T) -> None:
        '集合内に値valueがなければ、値を追加します。既に集合内にあれば、何もしません。'
        self._SortedSet_add(value)
    def discard(self, value: T) -> None:
        '値valueを削除します。値が存在しなくても例外は発生しません。'
        self._SortedSet_discard(value)
    def remove(self, value: T) -> None:
        '値valueを削除します。値が存在しなかった場合、ValueErrorを返します。'
        if not self._SortedSet_discard(value):
            raise ValueError(f'SortedSet.remove(value): value not in list: {value = }')
    def pop(self, i: int = -1) -> T:
        'SortedSet[i]の要素を削除して返します。'
        if i < 0: i += self._len
        if self._len == 0:
            raise IndexError('pop from empty SortedSet')
        if not 0 <= i < self._len:
            raise IndexError('pop index out of range')
        v = self.__getitem__(i)
        self._SortedSet_discard(v)
        return v
