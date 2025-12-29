# Fenwick Tree

配列の一点加算・区間和取得をO(logN)で行います。  
以下、配列の要素の型をTとします(使用上はcodonが自動で型推論します)。  
**すべての関数を通して、Tにあたる型は統一してください。**  

## 使い方  

`FenwickTree(N) -> None`
- 長さNの配列Aを確保し、すべての要素を0で初期化します。

`build(A: generator[T]) -> None`  
`build(A: list[T]) -> None`  
- Fenwick Treeの配列を引数Aで初期化します。
- 制約: len(A) = N (assertは行いません)
- 計算量: 時間 O(N)

`add(i: int, value: T) -> None`
- A[i] += value の一点加算を行います。

`sum0(i: int) -> T`  
`sum(i: int) -> T`  
`sum(Lt: int, Rt: int) -> T`  
- 区間和を計算する関数です。**`sum`関数は1引数と2引数で機能が異なります。**  
- `sum0(i)` と `sum(i)` は、**閉区間** A[0, i]の総和を返します(A[i]を含みます)。  
i < 0 のときは0を返します。i ≥ N の場合はAssertionErrorとなります。    
制約: i < N
- `sum(Lt, Rt)` は、**半開区間** A[Lt, Rt)の総和を返します(A[Rt]を含みません)。    
Lt ≥ Rt のときは0を返します。Lt < 0 または N < Rt の場合はAssertionErrorとなります。     
制約: Lt ≥ 0, Rt ≤ N

`bisect(value: T) -> int`
- **配列Aのすべての要素が非負であることを要求します。**   
sum0(i) ≥ value を満たす最小の非負整数iを返します。存在しない場合、Nを返します。
- 制約: 0 ≤ k < N を満たすすべての整数kに対して、A[k] ≥ 0
- 計算量: O(logN)





