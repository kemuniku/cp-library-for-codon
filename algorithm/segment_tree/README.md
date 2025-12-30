# Segment Tree

二項演算opの計算量を1回あたりO(1)として、配列の一点更新・区間積取得をO(logN)で行います。  
以下、配列の要素の型をTとします(使用上はcodonが自動で型推論します)。  
**すべての関数を通して、Tにあたる型は統一してください。**   

## 使い方   

`SegTree(op: F, e: T, N: int) -> None`  
`SegTree(op: F, e: T, A: generator[T]) -> None`  
`SegTree(op: F, e: T, A: list[T]) -> None`  
- 第3引数がNの場合、長さNの配列を確保し、配列を単位元eで初期化します。    
- 第3引数がAの場合、長さlen(A)の配列を確保し、配列を引数Aで初期化します。
- opは二項演算です。**型はFとしていますが、`Function`型にしてください**。  
  (型にジェネリクスを用いているのは、codonの関数型推論エラーを回避するためです)     
`op(左子の作用値: T, 右子の作用値: T) -> 合成後の作用値: T` となるような関数を渡してください。

`set(i: int, value: T) -> None`
- A[i]の値をvalueに変更します。

`get(i: int) -> T`
- A[i]の値を取得します。
- 計算量: O(1)

`prod(Lt: int, Rt: int) -> T`
- **半開区間** A[Lt, Rt)の積を返します(A[Rt]を含みません)。   
Lt = Rt の場合、単位元eを返します。
- 制約: 0 ≤ Lt ≤ Rt ≤ N

`all_prod() -> T`
- Aの全区間積、すなわち A[0, N)の積を返します。
- 計算量: O(1)  

`max_right(Lt: int, judge: Function[tuple[T], bool]) -> int`
- `judge(作用値: T) -> bool` の形の判定関数judgeを引数に取ります。    
ここで、judge(単位元e) = True および 区間積の単調性を要求します。   
judge(prod(Lt, Rt)) = True を満たす最大のRt(Lt ≤ Rt ≤ N)を返します。
- 制約: 0 ≤ Lt ≤ N

`min_left(Rt: int, judge: Function[tuple[T], bool]) -> int`
- `judge(作用値: T) -> bool` の形の判定関数judgeを引数に取ります。  
ここで、judge(単位元e) = True および 区間積の単調性を要求します。  
judge(prod(Lt, Rt)) = True を満たす最小のLt(0 ≤ Lt ≤ Rt)を返します。
- 制約: 0 ≤ Rt ≤ N






