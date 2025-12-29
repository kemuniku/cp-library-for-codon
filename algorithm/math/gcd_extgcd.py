#最大公約数
gcd = lambda x, y: gcd(y, x % y) if y else abs(x)

#拡張ユークリッドの互除法
def ext_gcd(a: int, b: int) -> tuple[int, int, int]:
    '''
    g == a * x + b * y を満たす(g, x, y)を返します。
    
    a == b == 0 の場合、(g, x, y) = (0, 1, 0) とします。
    そうでない場合、(g, x, y)は以下の条件を満たします。
    (1) g == gcd(a, b) > 0
    (2) abs(x) <= max(1, abs(b // g))
    (3) abs(y) <= max(1, abs(a // g))
    '''
    if b == 0:
        return (a, 1, 0) if a >= 0 else (- a, - 1, 0)
    g, x, y = ext_gcd(b, a % b)
    return g, y, x - (a // b) * y
