# 畳み込み (NTT)  

2つの整数列の mod P における畳み込みをO(NlogN + Nlog64)で行います。  
(64はCPUの64bitワードに基づく定数であり、`bit_length`の計算量評価にかかります)

## 使い方

`convolution(P: int, primitive_root: int = 0) -> None`
- 法となる素数Pを設定します。
- Pの原子根のひとつが既に分かっている場合、1 ≤ primitive_root < P となるように引数を入力してください。   
そうでない場合、primitive_root ≤ 0 または P ≤ primitive_root となるように引数を決定してください。自動で計算します。
- 制約
  - 2 <= P <= 2_147_483_648(およそ $2.1 × 10^9$), Pは素数
  - 1 ≤ primitive_root < Pの場合、primitive_rootはPの原子根のひとつ
- 計算量
  - O(log^2 P)
  - primitive_root ≤ 0 または P ≤ primitive_root の場合、追加でO(√P)


`convolve(F: list[int], G: list[int]) -> list[int]`
- 配列Fと配列Gを畳み込んだ配列Hを**新しく作成して**返します。
- len(F) = 0 または len(G) = 0 の場合、空配列 `[]` を返します。    
そうでない場合、Hは長さ len(F) + len(G) - 1 の整数列です。   
0 ≤ i < len(F) + len(G) - 1 に対して以下を満たします。  
  - H[i] = sum(F[k] * G[i - k] % P for k in range(i + 1)) % P (畳み込みの定義)
  - **0 ≤ H[i] < P (除算仕様はPython・PyPyと一致します)**
- 制約: FとGの要素はどちらも`int`型 **(modintは不可)**, HはNTT可能な長さに収まる
- 計算量: N = len(F) + len(G) - 1として、 O(NlogN + Nlog64)    
(実装上、`bit_length`の計算量がO(log wordsize) = O(log 64)です)

`find_primitive_root(P: int) -> int`
- 素数Pの原始根のひとつを返します。なお、有名素数は原始根を埋め込んであります。
- 制約: 2 ≤ P, Pは素数
- 計算量: O(√P + log^2 P)

`DFT(A: list[int], required_len: int) -> list[int]`
- DFTしたい配列Aと、畳み込み結果に必要な配列の長さ required_len を渡します。   
N = (required_len 以上の最小の2冪) として、Aを末尾ゼロ埋めしてからDFTを施した、長さNの配列Bを**新しく作成して**返します。    
Bの要素は **-P < B[i] < P を満たします(codonの除算仕様に従います)**。  
N < len(A) の場合、Aの先頭N要素だけを切り出し、それ以降を無視してDFTします。  
- 制約: NはNTT可能な長さに収まる
- 計算量: O(NlogN)

`IDFT(A: list[int]) -> list[int]`
- DFTした配列AにIDFTを施し、**破壊的変更を加えた配列Aを**返します。  
実行後の配列Aは**0 ≤ A[i] < Pを満たします(除算仕様はPython・PyPyと一致します)**。  
- 制約: AはDFT表現の配列で、長さは2冪
- 計算量: O(NlogN)











