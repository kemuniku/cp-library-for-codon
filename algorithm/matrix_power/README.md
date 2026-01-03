# 行列累乗

法MODの下、2次元リストに対する行列累乗を行います。


## 使い方

`matrix_power(MOD: int) -> None`
- 法MODを取り込みます。
- 制約: 1 ≤ MOD ≤ 3_037_000_500 (およそ $3.0×010^9$)

`eye(N: int) -> list[list[int]]`
- N行N列の単位行列を返します。`A[h][w] = (1 if h == w else 0)` を満たします。     
N = 0の時は `[]` を返します。
- 制約: N ≥ 0

`add(A: list[list[int]], B: list[list[int]]) -> list[list[int]]`
- H行W列の行列Aと、H行W列の行列Bから、H行W列の行列C := A + Bを新しく作成します。
- 返り値は 0 ≤ C[h][w] < MOD を満たします。
- 計算量: O(HW)

`mul(A: list[list[int]], B: list[list[int]]) -> list[list[int]]`
- H行X列の行列Aと、X行W列の行列Bから、H行W列の行列C := A * Bを新しく作成します。
- 返り値は 0 ≤ C[h][w] < MOD を満たします。
- 計算量: O(HWX)

` doubling_mul(A: list[list[int]], k: int) -> list[list[int]]`
- N行N列の正方行列Aから、N行N列の正方行列C := A ** kを新しく作成します。   
k = 0の場合、N行N列の単位行列を返します。
- 返り値は 0 ≤ C[h][w] < MOD を満たします。
- 制約: k ≥ 0
- 計算量: O(N^3 logk)




