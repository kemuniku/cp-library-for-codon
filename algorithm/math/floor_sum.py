#floor sum for codon
def floor_sum[T](n: T, m: T, a: T, b: T) -> T:
    '''
    sum(floor( (a * i + b) / m ) for i in range(n)) を求めます。
    ここで、floor(x)はx以下最大の整数を返す関数です。
    n <= 0 の時の返り値は0とします。

    制約:
     - m != 0
     - x = max( abs(n), abs(m), abs(a), abs(b) ) としたとき、
       x ** 2 + xがTの表現範囲内に収まる(答えがオーバーフローしない)
     - Tは128bit以下の整数型
    計算量: O(log max(n, m, a, b))
    '''
    zero: T = n ^ n
    one: T = - ~ zero
    assert m != zero, f'ゼロ除算はできません。{n = }, {m = }, {a = }, {b = }'
    if m < zero:
        m, a, b = - m, - a, - b
    ans: T = zero
    while True:
        if n <= zero:
            return ans
        if not zero <= a < m:
            div_a, rem_a = divmod(a, m)
            if n & one == zero:
                ans += div_a * (n >> one) * (n - one)
            else:
                ans += div_a * n * ((n - one) >> one)
            a: T = rem_a
        if not zero <= b < m:
            div_b, rem_b = divmod(b, m)
            ans += div_b * n
            b: T = rem_b
        #div_y, rem_y = divmod(an + b, m) オーバーフロー注意
        div_n, rem_n = divmod(n, m)
        div_y, rem_y = divmod(a * rem_n, m)
        div_y += a * div_n
        if rem_y >= m - b:
            div_y += one
            rem_y: T = rem_y - (m - b)
        else:
            rem_y += b
        n, m, a, b = div_y, a, m, rem_y



