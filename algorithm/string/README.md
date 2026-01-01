# string

文字列アルゴリズム全般のライブラリです。   

## [suffix array, LCP array](./suffix_array_lcp.py)  

suffix array, LCP arrayを構築します。  

### 使い方  

`SuffixArray.suffix_array(S: str) -> list[int]`  
`SuffixArray.suffix_array(S: list[str]) -> list[int]`  
`SuffixArray.suffix_array(A: list[int]) -> list[int]`
- SA-IS法でsuffix arrayを構築します。
- Qを「S[i:] (または A[i:]) を0 ≤ i < Nに対して列挙し、ソートした長さNの配列」とします。  
このとき、0 ≤ i < Nについて、S[i:] (または A[i:]) = Q[k]を満たす唯一のk(0 ≤ k < N)を返します。
- 計算量
  - `S: str` または `S: list[str]` の時: N = len(S), d = 128  
  - `A: list[int]` の時: N = len(A), d = max(A) - min(A)  
  
  として、O(N + d) か O(NlogN) の小さい方

`SuffixArray.LCP_array(A, SA: list[int]) -> list[int]`
- N = len(A), SAをAのsuffix arrayとして、LCP arrayをO(N)で構築します。
- 返り値は長さNの配列で、A[SA[i]:]とA[SA[i + 1]:]の最長共通接頭辞(0 ≤ i < N - 1)を返します。   
i = N - 1の時は例外的に0とします。
- 制約: SAは長さNの配列で、Aのsuffix array
- 計算量: O(N)


## [Z algorithm](./z_algorithm.py)  

AとA[i:]の最長共通接頭辞を列挙します。

### 使い方

`Z_algorithm(A) -> list[int]`
- N = len(A)とします。
すべての 0 ≤ i < N に対し、AとA[i:]の最長共通接頭辞を求めます。
- 制約: Aは`str`または`list`
- 計算量: O(N)


## [Manacher algorithm](./manacher.py)

Sの最長回文長を列挙します。  

### 使い方

`manacher(S) -> list[int]`
- N = len(S) として、Sの最長回文長を示す長さ2N - 1の配列Aを返します。
  - A[2 * i]: S[i]を中心とする、奇数長の最長回文長(0 ≤ i < N)
  - A[2 * i + 1]: S[i]とS[i + 1]の間を中心とする、偶数長の最大回文長(0 ≤ i < N - 1)
- 制約: Sは`str`または`list`
- 計算量: O(N)

## [Rolling Hash](./rolling_hash.py)

法を mod = $2^{61}-1$ で固定したローリングハッシュのライブラリです。  

### 使い方  

`RollingHash(base: int = -1) -> None`
- ローリングハッシュの基数を登録します。
- 0 ≤ base < mod の場合、基数を引数baseとします。  
そうでない場合、コンパイル時に乱択した0以上mod未満の定数を登録します。

`hash(A) -> int`
- 基数base・法modとしたときのAのハッシュ値を計算します。
- 制約
   - Aの型は(`str`, `list[str]`, `list[int]`)のどれか
   - Aが`list[int]`の場合、0 ≤ A[i] < mod (0 ≤ i < N)
- 計算量: O(N)

`rolling_hash(A, k: int) -> list[int]`
- 0 ≤ i ≤ N - k に対し、A[i: i + k]のハッシュ値を列挙します。
- 制約
   - Aの型は(`str`, `list[str]`, `list[int]`)のどれか
   - Aが`list[int]`の場合、0 ≤ A[i] < mod (0 ≤ i < N)
   - 0 ≤ k ≤ N
- 計算量: O(N)

`build(A) -> None`
- 文字列または配列Aを取り込みます。
- 制約
   - Aの型は(`str`, `list[str]`, `list[int]`)のどれか
   - Aが`list[int]`の場合、0 ≤ A[i] < mod (0 ≤ i < N)
- 計算量: O(N)

`fold(Lt: int, Rt: int) -> int`
- **`build(A)`で取り込んだ文字列(配列)Aに対し、** A[Lt: Rt]のハッシュをO(1)で取得します。  
Lt ≥ Rt の場合、ハッシュ値を0とします。  
- 制約: **`build(A)`を実行済み**、0 ≤ Lt, Rt ≤ N
- 計算量: O(1)





