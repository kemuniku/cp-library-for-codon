# Wavelet Matrix  

静的な非負整数列Aに対する検索に特化したアルゴリズムです。    
N = len(A), M = max(A)として、構築O(NlogM)・検索操作の多くをO(logM)で行います。   
なお`bit_count`の実装上、 O(log wordsize) = O(log 64) の定数項がかかります。

## 使い方



`WaveletMatrix(A: list[int]) -> None`
- Wavelet Matrixに非負整数列Aを読み込みます。
- 制約: len(A) < $2^{29}$, **Aはint型の非負整数列**
- 計算量: 時間 O(NlogM)、空間 O(N)

`access(i: int) -> int`
- A[i]を取得します。
- 計算量: O(logM)

`rank(Lt: int, Rt: int, value: int) -> int`
- 半開区間A[Lt, Rt)内の値valueの出現回数を返します(A[Rt]は区間に含みません)。
- 制約: 0 ≤ Lt ≤ Rt ≤ N
- 計算量: O(logM)

`select(cnt: int, value: int) -> int`
- **0-indexedで**添字が小さい方からcnt番目に出現する値valueの添字を返します。  
Aにvalueがcnt + 1個以上存在しない場合、代わりにNを返します。
- 例として `A = [7, 8, 7, 9, 9]` とすると以下のような返り値になります。
   - `select(0, 7) = 0`
   - `select(1, 7) = 2`
   - `select(2, 7) = 5` (0-indexedで2番目の7は存在しないので、N = len(A) = 5 を返します)
- 制約: 0 ≤ cnt
- 計算量: O(logM)

`kth_min(Lt: int, Rt: int, k: int) -> int`
- `sorted(A[Lt: Rt])[k]` : 半開区間A[Lt, Rt)の、小さい方から**0-indexedで**k番目の要素を返します。
- 制約: 0 ≤ Lt ≤ Rt ≤ N, 0 ≤ k < Rt - Lt
- 計算量: O(logM)

`range_freq(Lt: int, Rt: int, vL: int, vR: int) -> int`
- vL ≤ A[i] < vR (Lt ≤ i < Rt) を満たすiの個数を返します。  
すなわち、半開区間A[Lt, Rt)における、vL以上vR未満の要素の個数を返します。
- 制約: 0 ≤ Lt ≤ Rt ≤ N
- 計算量: O(logM)

`prev_value(Lt: int, Rt: int, value: int) -> int`
- 半開区間A[Lt, Rt)のうち、x < value (**valueより真に小さい**) を満たす最大の要素xを返します。
- 条件を満たす値が存在しない場合、代わりに-1を返します。    
(SortedList等の`prev_value`の返り値と異なるので注意してください)
- 制約: 0 ≤ Lt ≤ Rt ≤ N
- 計算量: O(logM)

`next_value(Lt: int, Rt: int, value: int) -> int`
- 半開区間A[Lt, Rt)のうち、x > value (**valueより真に大きい**) を満たす最小の要素xを返します。
- 条件を満たす値が存在しない場合、代わりに-1を返します。    
(SortedList等の`next_value`の返り値と異なるので注意してください)
- 制約: 0 ≤ Lt ≤ Rt ≤ N
- 計算量: O(logM)

ここから下は、計算量がO(logM)ではない関数です。 


`topk_mode(Lt: int, Rt: int, k: int) -> list[tuple[int, int]]`
- 半開区間A[Lt, Rt)に含まれる要素を、頻度の降順(頻度が同じなら値の昇順)に上位k種類を並べたリストを返します。   　
- A[Lt, Rt)に含まれる要素の種類数が(1-indexedで)k種類に満たない場合はすべて列挙します。  
この際、返り値のリストの長さがk未満になります。
- 返り値は長さがk以下のリストで、`(要素の値, 区間内の頻度)`のタプルです。  
(ソートの優先順位と異なり、値が左側・頻度が右側となるように並びます)
- 制約: 0 ≤ Lt ≤ Rt ≤ N
- 計算量: O(k logN logM)

`intersect(L1: int, R1: int, L2: int, R2: int) -> list[tuple[int, int]]`
- 半開区間A[L1, R1)と半開区間A[L2, R2)の積集合を取ります。
- 返り値のリストは`(値, 頻度)`のタプルで、値の昇順に並びます。  
ここで頻度とは、A[L1, R1)とA[L2, R2)における値の出現回数の小さい側です。   
頻度が0となる要素は返り値に含みません。
- 制約: 0 ≤ L1 ≤ R1 ≤ N, 0 ≤ L2 ≤ R2 ≤ N
- 計算量: O(min(R1 - L1, R2 - L2) logM)

