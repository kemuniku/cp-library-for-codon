#floor sum for codon
#Reference: https://qiita.com/AkariLuminous/items/3e2c80baa6d5e6f3abe9
def floor_sum[T](n: T, m: T, a: T, b: T) -> T:
    '''
    sum( floor( (ai + b) / m ) for i in range(n) ) をO(log m)で求めます。
    制約: 0 < m, 型は整数, ai + bがオーバーフローしない
    '''
    zero: T = n ^ n
    one: T = - ~ zero
    assert zero < m, f'mが正整数ではありません。{m = }'
    if n <= zero:
        return zero
    ans: T = zero
    while True:
        if not zero <= a < m:
            a_div, a = divmod(a, m)
            ans += ( ((n - one) >> one) * n if n & one else (n - one) * (n >> one) ) * a_div
        if not zero <= b < m:
            b_div, b = divmod(b, m)
            ans += n * b_div
        y_max: T = a * n + b
        if y_max < m:
            return ans
        else:
            y_div, y_mod = divmod(y_max, m)
            n, m, a, b = y_div, a, m, y_mod
