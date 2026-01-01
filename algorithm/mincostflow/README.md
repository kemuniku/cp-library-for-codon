# 最小費用流

N頂点M辺の**整数容量の**最小費用流を、流量をFとしてO(F(N + M)logN)で求めます。    
ただし、コストが負の辺がある場合はO(NM)が追加でかかります。コストの負閉路がある場合は計算できません。  
以下、辺のコストの型をTとします(使用上はcodonが自動で型推論します)。  
**すべての関数を通して、Tにあたる型は統一してください。**

## 使い方  

`MCFGraph(N: int) -> None`
- N頂点0辺の有向グラフを作成します。
- 制約: 0 ≤ N < $2^{30}$

`add_edge(now: int, nxt: int, cap: int, cost: T) -> None`
- 頂点nowから頂点nxtに向かう、容量cap・流量1あたりのコストcostの辺を追加します。
- 制約
  - 0 ≤ cap, **capはint型**
  - **costは型Tで表現できる最大の値より真に小さい**  
(例として、Tが`int`ならcost < $2^{63}-1$、Tが`float`ならcost < `float('inf')`を要求します)

`get_edge(i: int) -> tuple[int, int, int, int, T]`
- **0-indexedで**i番目に追加した順辺の辺情報を取得します。
- `(now: int, nxt: int, cap: int, flow: int, cost: T)` のタプルで返します。  
これはi番目の辺が頂点nowから頂点nxtに向かう容量cap・単位流量あたりのコストcostの辺で、now → nxtの方向に流量flowが流れていることを示します。  
ここで、0 ≤ now,nxt < N, 0 ≤ flow ≤ cap を満たします。
- 制約: 0 ≤ i < M

`edges() -> list[tuple[int, int, int, int, T]]`
- これまでに追加した順辺の本数をMとして、i = 0, 1, ･･･, M - 1 の順に、**0-indexedで**i番目に追加した順辺の辺情報を列挙します。  
- i番目のリストの要素は `(now: int, nxt: int, cap: int, flow: int, cost: T)` のタプルです。  
これはi番目の辺が頂点nowから頂点nxtに向かう容量cap・単位流量あたりのコストcostの辺で、now → nxtの方向に流量flowが流れていることを示します。    
ここで、0 ≤ now,nxt < N, 0 ≤ flow ≤ cap を満たします。



`flow(St: int, Gl: int) -> tuple[int, T]`   
`flow(St: int, Gl: int, flow_limit: int) -> tuple[int, T]`  
- 頂点Stから頂点Glにフローを流し、(合計流量: int, 合計コスト: T)のタプルを返します。
- `flow(St, Gl)`では、頂点Stから頂点Glにフローを**流せるだけ**流します。
- `flow(St, Gl, flow_limit)`では、**flow_limitを流量上限として**フローを流します。   
追加制約: 0 ≤ flow_limit
- 制約
  - 0 ≤ St,Gl < N, St ≠ Gl
  - 合計コストは型Tの表現範囲に収まる
  - 初期グラフにコストの負閉路が存在しない
- 計算量
  - 合計流量をFとして、**O(F(N + M)logN) か O(F(N^2 + M)) の小さい方**  
  - 初期グラフにコストが負の辺が存在するなら、追加でO(NM)
- 補足
  - 2026/01/01現在、最短路反復のダイクストラ法をセグメント木で実装しています。  
    これはタプルが遅いPyPy3での最適化を目的とした実装ですが、codonの場合はheapqを用いるほうが高速かと思われます。  
  - ただし、密グラフでも計算量がO(F(N^2 + M))で抑えられるのはセグメント木によるものです。  
  従って、**もしも今後内部実装がheapqに変更された場合、密グラフの計算量が悪化します。使用するライブラリのバージョンに注意してください。**

`slope(St: int, Gl: int) -> list[tuple[int, T]]`  
`slope(St: int, Gl: int, flow_limit: int) -> list[tuple[int, T]]`  
- 頂点Stから頂点Glにフローを流し、コストの変曲点ごとに最小コストを列挙します。  
- `slope(St, Gl)`では、頂点Stから頂点Glにフローを**流せるだけ**流します。
- `slope(St, Gl, flow_limit)`では、**flow_limitを流量上限として**フローを流します。    
追加制約: 0 ≤ flow_limit
- 返り値のリストの要素は `(変曲点の流量: int, この流量での最小コスト: T)` のタプルです。    
先頭の要素は(0, 0)で、末尾の要素は(最大流量, このときの最小コスト)です。
- 制約・計算量: `flow`関数と同様
