# SortedList / SortedSet

SkipListを用いた順序付き(多重)集合です。  
Nを集合の大きさとして、多くの操作を時間計算量 **期待O(logN)・最悪O(N)** で行います。  
空間計算量は期待O(N)・最悪O(NlogN)です。    

なお筆者の経験上、tatyamさんのcodon版SortedSetのほうが高速に動作します。  
tatyamさんの実装は以下のURLからご覧ください。  
https://github.com/tatyam-prime/SortedSet/tree/main/codon

## [SortedSet](./sortedset.py)

SkipListを用いた順序付き集合です。**要素の重複は認めません。**  
以下、Nを集合の大きさとします。

### 使い方

`SortedSet() -> None`  
`SortedSet(A: generator[T]) -> None`  
`SortedSet(A: list[T]) -> None`
- SortedSetを宣言します。  
- 引数が`generator`あるいは`list`の場合、重複要素を取り除いてSortedSetに追加します。  
計算量: n = len(A) として、O(nlogn)

```python
len(SortedSet)
str(SortedSet)
bool(SortedSet)
```
- `len`では集合の大きさNを返します。
- 計算量: `len` `bool`はO(1), `str`はO(N)

```python
SortedSet[i]
del SortedSet[i]
value in SortedSet
```
- `[i]`はSortedSet内で **0-indexedで**i番目に小さい要素を出力します(0 ≤ i < N)。  
iが負の場合、 N + i番目に小さい要素を出力します(- N ≤ i < 0)。  
制約: - N ≤ i < N
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
`bisect_right(value: T) -> int`
- 集合内で値がvalue**以下**の要素の個数を返します。
- 期待計算量: O(logN)

`bisect_left(value: T) -> int`  
- 集合内で値がvalue**未満**の要素の個数を返します。
- 期待計算量: O(logN)

`prev_value(value: T, allow_equal: bool = False) -> Optional[T]`
- `prev_value`では、x < value (**valueより真に小さい**) を満たす最大の要素xを返します。  
`allow_equal`をTrueにすると、xの条件を x ≤ value (**value以下**) とします。
- 条件を満たす値xが存在しない場合はNoneを返します。
- 返り値は`Optional`型(型`T` または `None`を取る型)です。   
ここで、codonはまれに型`T`と「`Optional[T]`にキャストした型`T`」を異なる型として区別することがあります。    
もしも型推論エラーが起きた場合、`Optional[T]`で受け取った変数を型`T`に変換するステップを挟んでください。
- 期待計算量: O(logN)

`next_value(value: T, allow_equal: bool = False) -> Optional[T]`
- x > value (**valueより真に大きい**) を満たす最小の要素xを返します。    
`allow_equal`をTrueにすると、xの条件を x ≥ value (**value以上**) とします。
- 条件を満たす値xが存在しない場合はNoneを返します。
- 期待計算量: O(logN)




`add(value: T) -> None`
- 集合内に値valueがなければ、1個追加します。**既に集合内にあれば、何もしません。**
- 期待計算量: O(logN)

`discard(value: T) -> None`
- 集合内に値valueがあれば、削除します。集合内になければ、何もしません。
- 期待計算量: O(logN)

`remove(value: T) -> None`
- 集合内に値valueがあれば、削除します。集合内になければ、ValueErrorを返します。
- 制約: 集合内に値valueが存在する
- 期待計算量: O(logN)

`pop(i: int = -1) -> T`
- `SortedSet[i]`を削除し、削除した値を返します。
- 制約: - N ≤ i < N
- 期待計算量: O(logN)




## [SortedList](./sortedlist.py)

SkipListを用いた順序付き多重集合です。    
**要素の重複を認めますが、集合の大きさは $10^9$ 以下としてください。**    
以下、Nを集合の大きさとします。
- 制約: N ≤ $10^9$

### 使い方

`SortedList() -> None`    
`SortedList(A: generator[T]) -> None`    
`SortedList(A: list[T]) -> None`
- SortedListを宣言します。
- 引数が`generator`あるいは`list`の場合、すべての要素をSortedListに追加します。  
計算量: n = len(A) として、O(nlogn)

```python
len(SortedList)
str(SortedList)
bool(SortedList)
SortedList[i]
del SortedList[i]
value in SortedList
for v in SortedList
reversed(SortedList)
SortedList.clear()
```
- 機能・制約・計算量: SortedSetと同様

```python
bisect(value: T) -> int
bisect_left(value: T) -> int
bisect_right(value: T) -> int
prev_value(value: T, allow_equal: bool = False) -> Optional[T]
next_value(value: T, allow_equal: bool = False) -> Optional[T]
```
- 機能・制約・計算量: SortedSetと同様

`count(value: T) -> int`
- 集合内の値valueの個数を返します。
- 期待計算量: O(logN)

`add(value: T, amount: int = 1) -> None`
- 集合に値valueをamount個追加します。   
値は一度にまとめて追加できますが、**集合の大きさは $10^9$ 以下となるようにしてください。**
- 制約: 0 ≤ amount
- 期待計算量: O(logN)

`discard(value: T, amount: int = 1) -> None`
- 集合から値valueを max(0, amount) 個削除します。  
集合内の値valueの個数がamount個未満の場合、値valueをすべて削除します。
- 期待計算量: O(logN)

` remove(value: T, amount: int = 1) -> None`
- 集合から値valueをamount個削除します。  
集合内の値valueの個数がamount個未満の場合、ValueErrorを返します。
- 制約: 0 ≤ amount, 集合内に値valueはamount個以上存在する
- 期待計算量: O(logN)

`pop(i: int = -1) -> T`
- 機能・制約・計算量: SortedSetと同様


