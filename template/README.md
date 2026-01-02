# Template

codonの標準機能を拡張・改変するテンプレート集です。  

## [map 入力受取](./map_input.py)

- `N, M = map(int, input().split()` のような右辺mapの構文に対応します。
- アンパッキングは末尾のみ可能です。  
`N, *A = map(int, input().split())` には対応しますが、   
`*A, N = map(int, input().split())` はエラーを返します。    
この場合、右辺を`list`にキャストしてください。

## [int 除算方向変更](./int_py_floordiv.py)

- `int`と`Int[N]`の除算方向を、Python・PyPy3の負の無限大丸めに変更します。  
- floordiv`//`と、mod`%`の演算に変更を加えます。変更結果の例は後述します。
- 変更を行うと、除算の実行時間が5%ほど遅くなります。   
また、`Int[N]`で除算ができるのはN ≤ 128に限ります。
- `divmod`はこの変更の影響を受けません。

```python: codonが変更前、Pythonが除算方向変更後
print( 20 //  3,  20 %  3)  #codon: ( 6,  2), Python: ( 6,  2)
print(-20 //  3, -20 %  3)  #codon: (-6, -2), Python: (-7,  1)
print( 20 // -3,  20 % -3)  #codon: (-6,  2), Python: (-7, -1)
print(-20 // -3, -20 % -3)  #codon: ( 6, -2), Python: ( 6, -2)
```

## [int bit_length, bit_countを追加](./int_bit_length_count.py)

- `int.bit_length()`と`int.bit_count()`を追加します。   
- PyPy3の同名関数は低速でしたが、こちらは実測上高速です。

## [int ハッシュ値変更](./int_hash_splitmix64.py)

## [float 出力桁数変更](./float_str_precision.py)

## [pow 機能拡張](./pow_extended.py)





