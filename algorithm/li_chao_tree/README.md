# Li Chao Tree

最小値クエリを行うx座標の幅をXとして、線分追加・最小値取得をO(log^2 X)で行います。   
**現在調整中です。**

## 使い方

`Li_Chao_Tree(min_x: int, max_x: int) -> None`
- Li Chao Treeを宣言します。
- min_x, max_xは線分追加・最小値計算を行うx座標の区間の最小値・最大値です。   
すべてのxの入力は、閉区間[min_x, max_x]に収まることを要求します。
- 制約: min_x ≤ max_x
- note: min_x, max_xの定義を「最小値計算を行うx座標の閉区間」に変更予定

`add_line(a: int, b: int, xL: int, xR: int) -> None`
- 閉区間[xL, xR]に線分 y = ax + b を追加します。
- xL ≤ min_x, xR ≥ max_x を指定すると直線追加になります。
- 制約
   - max(min_x, xL) ≤ min(max_x, xR)
   - a ≠ $2^{63}-1$ かつ b ≠ $2^{63} - 1$
   - x = (min_x または max_x) のときにax + bがオーバーフローしない
- 計算量: 直線追加 O(logX), 線分追加 O(log^2 X)
- note: 制約を xL ≤ xR に修正予定, `add_line(a: int, b: int)` をオーバーロードして直線追加専用の関数を作成予定

`fold(x: int) -> int`
- 座標xにおける、現在までに追加した線分の最小値を求めます。      
線分が存在しない場合、$2^{63}-1$を返します。
- 制約: min_x ≤ x ≤ max_x
- 計算量: O(logX)
- note: 返り値をintから型ジェネリクス(多倍長対応)に変更予定

