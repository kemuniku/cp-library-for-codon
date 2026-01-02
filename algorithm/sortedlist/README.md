# SortedList / SortedSet

SkipListを用いた順序付き(多重)集合です。  
Nを集合の大きさとして、多くの操作を時間計算量 **期待O(logN)・最悪O(N)** で行います。  
空間計算量は期待O(N)・最悪O(NlogN)です。    

なお筆者の経験上、tatyamさんのcodon版SortedSetのほうが高速に動作します。  
tatyamさんの実装は以下のURLからご覧ください。  
https://github.com/tatyam-prime/SortedSet/tree/main/codon

## SortedSet

SkipListを用いた順序付き集合です。**要素の重複は認めません。**

### 使い方

`SortedSet() -> None`  
`SortedSet(A: generator[T]) -> None`  
`SortedSet(A: list[T]) -> None`
- SortedSetを宣言します。  
引数が`generator`あるいは`list`の場合、重複要素を取り除いてSortedSetに追加します。

```python
len(SortedSet)
str(SortedSet)
bool(SortedSet)
```
- 計算量: `len` `bool`はO(1), `str`はO(N)

```python
SortedSet[i]
del SortedSet[i]
value in SortedSet
```
- `[i]`はSortedSet内で **0-indexedで**i番目に小さい要素を出力します。  
- 期待計算量: O(logN)

```
for v in SortedSet
reversed(SortedSet)
SortedSet.clear()
```
- `for v in SortedSet`では値の昇順に、`reversed`では降順に列挙します。
- `clear`は配列を初期化します。初期化後もこれまでと同じ型Tしか受け付けないので注意してください。
- 計算量: O(N)

`bisect(value: T) -> int`  
`bisect_left(value: T) -> int`  
`bisect_right(value: T) -> int`
- `bisect`と`bisect_right`では、集合内で値がvalue**以下**の要素の個数を返します。 
- `bisect_left`では、集合内で値がvalue**未満**の要素の個数を返します。
- 計算量: 期待O(logN)

`prev_value(value: T, allow_equal: bool = False) -> Optional[T]`  
`next_value(value: T, allow_equal: bool = False) -> Optional[T]`
- `prev_value`では、x < value (**valueより真に小さい**) を満たす最大の要素xを返します。  
`allow_equal`をTrueにすると、xの条件を x ≤ value (**value以下**) にします。
- `next_value`では、x > value (**valueより真に大きい**) を満たす最小の要素xを返します。  
`allow_equal`をTrueにすると、xの条件を x ≥ value (**value以上**) にします。
- どちらも共通して、**条件を満たす値xが存在しない場合はNoneを返します**。
- 返り値は`Optional`型です。  
codonのタプルは`T`と`Optional[T]`を異なる型と認識するので、タプルにこの要素を入れる前には型`T`となるように再度の型指定を行ってください。
- 期待計算量: O(logN)




`add(value: T) -> None`

`discard(value: T) -> None`

`remove(value: T) -> None`

`pop(i: int = -1) -> T`






