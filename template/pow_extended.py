#巨大mod時のオーバーフローを回避  pow(base, -1, mod)に対応
def _pow_extended():
    _builtin_pow = pow
    def _codon_pow(base, exp):
        return _builtin_pow(base, exp)
    @overload
    def _codon_pow(base: int, exp: int, mod: int) -> int:
        '''
        codon用に pow(base, exp, mod) を拡張した関数です。
        1. (abs(mod) - 1) ** 2 >= 1 << 63 の場合に発生していたオーバーフローを回避しました。
        2. pow(base: int, exp: 負整数, mod: int) による逆元計算に対応しました。

        返り値の符号は mod の符号に一致します。
        いずれかの引数に INF_MIN := -1 << 63 を渡した場合の動作は未定義です。
        '''
        if mod == 0:
            raise ValueError('pow() 3rd argument cannot be 0')
        if mod == 1 or mod == -1:
            return 0
        if exp < 0:  #拡張ユークリッドの互除法
            a, b, x, y = base, mod, 1, 0
            while b:
                q = a // b
                a, b, x, y = b, a - q * b, y, x - q * y
            if a != 1 and a != -1:
                raise ValueError('base is not invertible for the given modulus')
            b128, m128 = Int[128](x), Int[128](mod)
            if a == -1:
                b128 = - b128
            exp = - exp
        else:
            b128, m128 = Int[128](base), Int[128](mod)
        v128 = Int[128](1)
        while exp:
            if exp & 1 == 1:
                v128 = v128 * b128 % m128
            b128 = b128 * b128 % m128
            exp >>= 1
        v = int(v128)
        return v + mod if v != 0 and (0 < v) != (0 < mod) else v
    return _codon_pow
pow = _pow_extended()
