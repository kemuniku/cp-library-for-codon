# Lazy Segment Tree  

二項演算op、遅延の反映関数mapping、遅延の合成関数compositionの計算量を1回あたりO(1)として、配列に対する区間遅延作用・区間積取得をO(logN)で行います。  
以下、配列の要素の型をTnode・遅延の型をTlazyとします(使用上はcodonが自動で型推論します)。   
**すべての関数を通して、Tnode・Tlazyにあたる型は統一してください。** 

## 使い方  

`LazySegTree(op: Fop, e: Tnode, mapping: Fmap, composition: Fcomp, id_: Tlazy, N: int) -> None`    
`LazySegTree(op: Fop, e: Tnode, mapping: Fmap, composition: Fcomp, id_: Tlazy, A: generator[Tnode]) -> None`    
`LazySegTree(op: Fop, e: Tnode, mapping: Fmap, composition: Fcomp, id_: Tlazy, A: list[Tnode]) -> None`    
- 第6引数がNの場合、長さNの配列を確保し、配列を(作用値: 単位元e, 遅延: 遅延の単位元id_)で初期化します。
- 第6引数がAの場合、長さlen(A)の配列を確保し、配列を(作用値: A[i], 遅延: 遅延の単位元id_)で初期化します。
- opは二項演算です。**型はFopとしていますが、`Function`型にしてください**。  
(型にジェネリクスを用いているのは、codonの関数型推論エラーを回避するためです)     
`op(左子の作用値: Tnode, 右子の作用値: Tnode) -> 合成後の作用値: Tnode` となるような関数を渡してください。
- mappingは遅延の反映関数です。**型はFmapとしていますが、`Function`型にしてください。**  
`mapping(遅延: Tlazy, 作用値: Tnode) -> 反映後の作用値: Tnode` としてください。
- compositionは遅延の合成関数です、**型はFcompとしていますが、`Function`型にしてください。**   
`composition(新しい遅延: Tlazy, これまでの遅延: Tlazy) -> 合成後の遅延: Tlazy` としてください。  


`set(i: int, node_value: Tnode) -> None`
- A[i]の値を(作用値: node_value, 遅延: 遅延の単位元id_)に変更します。

`get(i: int) -> Tnode`
- A[i]の作用値を取得します。
- 計算量: O(logN)

`prod(Lt: int, Rt: int) -> Tnode`
- **半開区間**A[Lt, Rt)の積を取り、作用値を返します(A[Rt]を含みません)。  
Lt = Rt の場合、作用値の単位元eを返します。
- 制約: 0 ≤ Lt ≤ Rt ≤ N

`all_prod() -> Tnode`
- Aの全区間積、すなわちA[0, N)の積を取り、作用値を返します。
- 計算量: O(1)

`apply(i: int, lazy_op: Tlazy) -> None`   
`apply(Lt: int, Rt: int, lazy_op: Tlazy) -> None`
- `apply(i, lazy_op)`ではA[i]に遅延lazy_opを作用します。    
なお、3引数の`apply(i, i+1, lazy_op)`でも同様の操作が可能です。
- `apply(Lt, Rt, lazy_op)`ではLt ≤ k < Rtを満たすA[k]に対し、遅延lazy_opを作用します。   
制約: 0 ≤ Lt ≤ Rt ≤ N

`max_right(Lt: int, judge: Function[tuple[Tnode], bool]) -> int`

- `judge(作用値: Tnode) -> bool` の形の判定関数judgeを引数に取ります。   
ここで、judge(単位元e) = True および 区間積の単調性を要求します。   
judge(prod(Lt, Rt)) = True を満たす最大のRt(Lt ≤ Rt ≤ N)を返します。
- 制約: 0 ≤ Lt ≤ N


`min_left(Rt: int, judge: Function[tuple[Tnode], bool]) -> int`

- `judge(作用値: Tnode) -> bool` の形の判定関数judgeを引数に取ります。   
ここで、judge(単位元e) = True および 区間積の単調性を要求します。   
judge(prod(Lt, Rt)) = True を満たす最小のLt(0 ≤ Lt ≤ Rt)を返します。    
- 制約: 0 ≤ Rt ≤ N


## 参考文献  

- 大槻兼資 / 杉江祐哉 / 中村謙弘 著、AtCoder株式会社 高橋直大 監修   
  **『アルゴリズム実技検定 公式テキスト［上級］～［エキスパート］編』**    
  マイナビ出版, 2023   
  https://book.mynavi.jp/ec/products/detail/id=135840
