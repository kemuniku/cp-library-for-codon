# string

文字列アルゴリズム全般のライブラリです。   

## [suffix array, LCP array](./suffix_array_lcp.py)  

suffix array, LCP arrayを構築します。  

### 使い方  

`SuffixArray.suffix_array(S: str) -> list[int]`
`SuffixArray.suffix_array(S: list[str]) -> list[int]`
`SuffixArray.suffix_array(A: list[int]) -> list[int]`
- SA-IS法でsuffix arrayを構築します。
- Qを「S[i:](A[i:])を0 ≤ i < Nに対して列挙し、ソートした長さNの配列」とします。  
このとき、0 ≤ i < Nについて、S[i:](A[i:]) = Q[k]を満たす唯一のk(0 ≤ k < N)を返します。
- 計算量
  - `S: str` または `S: list[str]` の時: N = len(S), d = 128  
  - `A: list[int]` の時: N = len(A), d = max(A) - min(A)  
  
  として、O(N + d) か O(NlogN) の小さい方

`SuffixArray.LCP_array(A, SA: list[int]) -> list[int]`
- N = len(A), `SA`をAのsuffix arrayとして、LCP arrayをO(N)で構築します。
- 返り値は長さNの配列で、A[SA[i]:]とA[SA[i + 1]:]の最長共通接頭辞(0 ≤ i < N - 1)を返します。i = N - 1の時は0とします。
- 制約: SAは長さNの配列で、Aのsuffix array
- 計算量: O(N)

(編集中)
