# Li Chao Tree

最小値クエリを行うx座標の幅をXとして、線分追加・最小値取得をO(log^2 X)で行います。    
以下、x座標の型をTx(**整数に限る**)、y座標の計算に使う型をTyとします。  
また、INFを型Tyで表せる最大の値とします。  
INFの例として、Tyが`int`なら $2^{63} - 1$ 、`float`なら`float('inf')`、`Int[N]`なら $2^{N - 1} - 1$ です。   




## 使い方

`LiChaoTree(min_x: Tx, max_x: Tx) -> None`
- Li Chao Treeを宣言します。
- min_x, max_xは最小値計算に用いるx座標の区間の最小値・最大値です。   
すべてのxの入力は、閉区間[min_x, max_x]に収まることを要求します。
- 制約: min_x ≤ max_x, 型は整数型(`int`, `Int[N]`, `UInt[N]` のどれか)

`add_line(a: Ty, b: Ty) -> None`    
`add_line(a: Ty, b: Ty, xL: Tx, xR: Tx) -> None`
- `add_line(a, b)`(2引数)は、直線 y = ax + b を追加します。
- `add_line(a, b, xL, xR)`(4引数)は、閉区間[xL, xR]に 線分 y = ax + b を追加します。  
ただし、xL ≤ min_x かつ max_x ≤ xR の場合、直線追加とみなして処理します。
- 制約
   - xL ≤ xR
   - **a ≠ INF かつ b ≠ INF** (INF: 型Tyで表現できる最大の値)
   - 追加区間内の任意のx座標で、ax + bが型Tyにおいてオーバーフローしない
- 計算量: 直線追加 O(logX), 線分追加 O(log^2 X)

`fold(x: Tx) -> Ty`
- 座標xにおける、現在までに追加した線分の最小値を求めます。      
- 線分が存在しない場合、INF(型Tyで表現できる最大の値)を返します。
- 制約: min_x ≤ x ≤ max_x
- 計算量: O(logX

## 更新履歴

2026/01/03 コードを全面的に改修しました。型ジェネリクスにより、多倍長整数に対応しました。

