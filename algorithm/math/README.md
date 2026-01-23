# math  

数学アルゴリズム全般のライブラリです。

## 更新履歴

2026/01/23
 - floor_sumのコードを調整しました。  
m < 0でも動作するように変更しています。

## [isqrt](./isqrt.py)

floor(√n) を求めます。

### 使い方

`isqrt(n: int) -> int`
- $m^2$ ≤ n < $(m+1)^2$を満たす非負整数mを求めます。
- 制約: 0 ≤ n
- 計算量: おそらく O(log wordsize) = O(1)

## [gcd / extgcd](./gcd_extgcd.py)

最大公約数のライブラリです。  


### 使い方

`gcd(x, y)`
- xとyの最大公約数を求めます。ただし、gcd(0, 0) = 0とします。
- 制約: xとyの型が一致する、x % yの演算が可能
- 計算量: O(log min(x, y))

`ext_gcd(a: int, b: int) -> tuple[int, int, int]`
- g = ax + by を満たす(g, x, y)の組を返します。
- a = b = 0 の場合、(0, 0, 0)を返します。    
そうでない場合、`(g: int, x: int, y: int)`の形式でタプルを返します。  
ここで、g, x, yは以下の条件を満たします。
    - g = gcd(a, b) > 0
    - abs(x) ≤ max(1, abs(b / g))
    - abs(y) ≤ max(1, abs(a / g))
- 計算量: O(log min(a, b))

## [中国剰余定理](./crt.py)

n ≡ R[i] mod M[i] をすべて満たす最小の非負整数nを求めます。  

### 使い方

`CRT(R: list[int], M: list[int]) -> tuple[int, int]`
- 0 ≤ i < len(R) = len(M) を満たすすべてのiに対し、 n ≡ R[i] mod M[i] を満たす最小の非負整数nを求めます。
- 条件を満たすnが存在する場合、lcm(M)をMの最小公倍数として (n, lcm(M)) を返します。ここで、 0 ≤ n < lcm(M) を満たします。  
len(R) = len(M) = 0 の場合、(0, 1)を返します。
- 条件を満たすnが存在しない場合、(0, 0)を返します。
- 制約: len(R) = len(M), 0 < M[i], lcm(M) < $2^{63}$
- 計算量: O(len(R) * log(lcm(M)))



## [floor sum](./floor_sum.py)

sum( floor( (ai + b) / m ) for i in range(n) ) を求めます。  
ここで、floor(x)はx以下最大の整数とします。
例として floor(3.0) = floor(3.1) = 3, floor(-2.0) = floor(-1.9) = -2 です。

### 使い方

`floor_sum(n: T, m: T, a: T, b: T) -> T`
- sum( floor( (ai + b) / m ) for i in range(n) ) を求めます(nは区間に含みません)。  
**n ≤ 0 の場合、0を返します**。
- 制約
    - m ≠ 0 (2026/01/23 変更)
    - 型Tは(`int`, `Int[N]`, UInt[N]`)のいずれかで、除算が可能
    - x = max( abs(n), abs(m), abs(a), abs(b) ) としたとき、 $x^2 + x$ が型Tの表現範囲内に収まる(2026/01/23 変更)。   
      特に、**答えがオーバーフローしない**。
- 計算量: O(log m)
















