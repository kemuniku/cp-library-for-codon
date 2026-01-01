# modint  

自動でmodを取る整数クラスです。  
**使用方法が特殊なので注意してください。**   

## 使い方(クラスの定義)

```python
@tuple
class modint(Static[_ModIntCore]):
    mod = MOD
```
- **他のライブラリと異なり、modintは静的継承を用いて宣言します。**
- `@tuple`から続く上記の3行をコピーし、
  - クラス名: テンプレで`modint`となる部分 
  - 法mod: テンプレで`MOD`となる部分

  の2箇所を任意に書き換えて宣言してください。
- 制約: 1 ≤ mod ≤ 3_037_000_500 (およそ $3.0×10^9$), **法modはint型**

## 使い方(modint内部)

以下、クラス名を`modint`とします。  

`modint(n: int) -> None`
- 法modの下で、整数nをmodintにキャストします。
- **nは`int`型しか受け付けません。`Int[N]`や`UInt[N]`といった型をmodintに直接キャストすることはできません。**
- 制約: **nは`int`型**

```python
str(modint)
int(modint)
bool(modint)
hash(modint)
+ modint
- modint
modint == other
modint != other
```
- `str`と`int`の返り値は 0 ≤ n < mod を満たします。
- ハッシュの計算式は基数乱択 + SplitMix64で変更する方式に変更しています。  
従って、int(modint) = hash(modint) **とは限りません。**
- `==`と`!=`は例外的に、異なるクラス名のmodint同士でも比較できます。

```python
modint + other
other + modint
modint - other
other - modint
modint * other
other * modint
modint / other
other / modint
modint += other
modint -= other
modint *= other
modint /= other
```
- **ACLと異なり、除算はfloordiv `//` ではなくtruediv `/` です。**   
(floordiv `//` と mod `%` の演算はエラーとなります)
- 制約
   - otherの型は(`int`, `Int`, `UInt`, **自身と同じクラスの`modint`**)のどれか
   - $-2^{63}$ ≤ other < $2^{63}$ (otherは **`int`の表現範囲内**)
   - `/`演算では、割られる数は法modにおいて逆元を有する
- 計算量: `+` `-` `*`はO(1)、`/`はO(log mod)

```python
modint ** other
inv(modint)
modint << other
modint >> other
```
- `**`演算は負にも対応しています。  
例として、`modint ** -1`は`inv(modint)`と同じ値になります。  
ただし、`pow`関数は使えません(`pow(modint, other)`は非対応です)。
- `inv(modint)`は法modにおける逆元を返します。定義できない場合はエラーとなります。
- `<<`は`2 ** other`倍し、`>>`は`2 ** other`で割ります。  
ここで、`>>`は奇数modであることを要求します。偶数modの場合はエラーとなります。
- `modint / 2`の計算量はO(log mod)ですが、`modint >> 1`はO(1)です。
- 制約
   - otherの型は(`int`, `Int`, `UInt`, **自身と同じクラスの`modint`**)のどれか
   - $-2^{63}$ ≤ other < $2^{63}$ (otherは **`int`の表現範囲内**)
   - `modint ** (負整数)`と`inv`では、modintは法modにおいて逆元を有する
   - `<<`と`>>`では、otherは非負整数
   - `>>`では、法modは奇数
- 計算量
   - `** (非負整数)`, `<<`, `>>`: O(log other)
   - `** (負整数)`: O(log mod + log abs(other))
   - `inv`: O(log mod)













