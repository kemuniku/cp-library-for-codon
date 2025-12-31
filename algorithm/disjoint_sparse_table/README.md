# Disjoint Sparse Table

配列の長さをN、二項演算opの計算量を1回あたりO(1)とします。  
時間・空間O(NlogN)の前計算の下、配列の区間積取得をO(1)で行います。  

## 使い方  

`DisjointSparseTable(op: F, A: list[T]) -> None`
- Sparse Tableを配列Aで初期化します。
- opは二項演算です。**型はFとしていますが、`Function`型にしてください。**  
(型にジェネリクスを用いているのは、codonの関数型推論エラーを回避するためです)   
`op(左子の作用値: T, 右子の作用値: T) -> 合成後の作用値: T` となるような関数を渡してください。
- 計算量: 時間・空間 O(NlogN)

`prod(Lt: int, Rt: int) -> T`
- **半開区間** A[Lt, Rt)の積を返します(A[Rt]を含みません)。
- 制約: 0 ≤ Lt < Rt ≤ N **(Lt = Rt の入力を禁止します)**
- 計算量: O(1) 
