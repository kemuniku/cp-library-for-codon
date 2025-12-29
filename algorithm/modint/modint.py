#modint for codon
from random import getrandbits as _ModIntCore_random_getrandbits
_ModIntCore_random_base: int = _ModIntCore_random_getrandbits(63)
@tuple
class _ModIntCore:
    '''
    modint for codon
    自動でmodを取る整数クラスです。
    使用方法が特殊なため、下記の使用方法を必ず確認してください。

    ■制約
    - 値n: int型 (Int[N], UInt[N] はキャスト不可)
    - 法mod: int型, 1 <= mod <= 3_037_000_500

    ■使用方法
    (法modの値ごとに、_ModIntCoreを継承した子クラスの宣言が必要です)
    以下のテンプレを @tuple の行からコピーし、
    クラス名(modint)と法(MOD)の値を書き換えて宣言してください。

    ■テンプレ(3行)
    @tuple
    class modint(Static[_ModIntCore]):
        mod = MOD  #ここに値を入れてください
    '''
    mod = 1  #mod: int = 1  のように型ヒントをつけるとエラー
    n: int
    def _inv_mod(n: int, m: int) -> int:
        assert n >= 0 and m >= 1
        a, b, x, y = n, m, 1, 0
        while b:
            q: int = a // b
            a, b, x, y = b, a - q * b, y, x - q * y
        if a != 1:
            raise ValueError(f'{n}はmod {m}で逆元を持ちません。')
        return x + m if (x ^ m) < 0 else x
    def __init__(self, n: int) -> None:
        if n < 0:
            n %= self.mod
            self.n = n + self.mod if n < 0 else n
        else:
            self.n = n % self.mod if n >= self.mod else n
    #表示・変換・比較
    def __str__(self) -> str:
        return str(self.n)
    def __repr__(self) -> str:
        return str(self.n)  #整数値だけを返したい場合はこちら
        #return f'{self.__class__.__name__}({self.n} mod {self.mod})'
    def __int__(self) -> int:
        return self.n
    def __bool__(self) -> bool:
        return self.n != 0
    def __pos__[T](self: T) -> T:  #(+ modint)
        return self
    def __neg__[T](self: T) -> T:  #(- modint)
        return self if self.n == 0 else self.__class__(self.mod - self.n)
    def __hash__(self) -> int:  #Reference: https://prng.di.unimi.it/splitmix64.c
        z: UInt[64] = UInt[64](self.n ^ _ModIntCore_random_base)
        z += UInt[64](0x9e3779b97f4a7c15)
        z = (z ^ (z >> UInt[64](30))) * UInt[64](0xbf58476d1ce4e5b9)
        z = (z ^ (z >> UInt[64](27))) * UInt[64](0x94d049bb133111eb)
        return int(z ^ (z >> UInt[64](31)))
    def __eq__(self, other) -> bool:  #modint == other
        return self.n == int(other)
    def __ne__(self, other) -> bool:  #modint != other
        return self.n != int(other)
    #演算: 足し算
    def __add__[T](self: T, other: T) -> T:  #modint + other
        n: int = self.n + other.n
        return self.__class__(n - self.mod if n >= self.mod else n)
    def __add__[T](self: T, other: UInt) -> T:
        return self.__add__(int(other))
    def __add__[T](self: T, other: Int) -> T:
        return self.__add__(int(other))
    def __add__[T](self: T, other: int) -> T:
        if not 0 <= other < self.mod:
            other %= self.mod
            if other < 0:
                other += self.mod
        other += self.n
        return self.__class__(other - self.mod if other >= self.mod else other)
    def __radd__[T](self: T, other) -> T:  #other + modint
        return self.__add__(int(other))
    #演算: 引き算
    def __sub__[T](self: T, other: T) -> T:  #modint - other
        n: int = self.n - other.n
        return self.__class__(n + self.mod if n < 0 else n)
    def __sub__[T](self: T, other: UInt) -> T:
        return self.__sub__(int(other))
    def __sub__[T](self: T, other: Int) -> T:
        return self.__sub__(int(other))
    def __sub__[T](self: T, other: int) -> T:
        if not 0 <= other < self.mod:
            other %= self.mod
            if other < 0:
                other += self.mod
        other: int = self.n - other
        return self.__class__(other + self.mod if other < 0 else other)
    def __rsub__[T](self: T, other) -> T:  #other - modint
        n: int = int(other)
        if not 0 <= n < self.mod:
            n %= self.mod
            if n < 0:
                n += self.mod
        n -= self.n
        return self.__class__(n + self.mod if n < 0 else n)
    #演算: かけ算
    def __mul__[T](self: T, other: T) -> T:  #modint * other
        return self.__class__(self.n * other.n % self.mod)
    def __mul__[T](self: T, other: UInt) -> T:
        return self.__class__(int(other) % self.mod * self.n % self.mod)
    def __mul__[T](self: T, other: Int) -> T:
        return self.__mul__(int(other))
    def __mul__[T](self: T, other: int) -> T:
        if not 0 <= other < self.mod:
            other %= self.mod
            if other < 0:
                other += self.mod
        return self.__class__(self.n * other % self.mod)
    def __rmul__[T](self: T, other) -> T:  #other * modint
        return self.__mul__(int(other))
    #演算: 割り算
    def __truediv__[T](self: T, other: T) -> T:  #modint / other
        if other.n == 0:
            raise ZeroDivisionError(f'ゼロ除算が発生しました。{self.n} / {other.n}')
        return self.__class__(self.n * _ModIntCore._inv_mod(other.n, self.mod) % self.mod)
    def __truediv__[T](self: T, other: UInt) -> T:
        return self.__truediv__(int(other))
    def __truediv__[T](self: T, other: Int) -> T:
        return self.__truediv__(int(other))
    def __truediv__[T](self: T, other: int) -> T:
        if not 0 <= other < self.mod:
            other %= self.mod
            if other < 0:
                other += self.mod
        if other == 0:
            raise ZeroDivisionError(f'ゼロ除算が発生しました。{self.n} / {other}')
        return self.__class__(self.n * _ModIntCore._inv_mod(other, self.mod) % self.mod)
    def __rtruediv__[T](self: T, other) -> T:  #other / modint
        if self.n == 0:
            raise ZeroDivisionError(f'ゼロ除算が発生しました。{self.n} / {other}')
        n: int = int(other)
        if not 0 <= n < self.mod:
            n %= self.mod
            if n < 0:
                n += self.mod
        return self.__class__(n * _ModIntCore._inv_mod(self.n, self.mod) % self.mod)
    #演算: 累乗・逆元
    def __pow__[T](self: T, other: T) -> T:  #modint ** other
        return self.__pow__(other.n)
    def __pow__[T](self: T, other: UInt) -> T:
        return self.__pow__(int(other))
    def __pow__[T](self: T, other: Int) -> T:
        return self.__pow__(int(other))
    def __pow__[T](self: T, other: int) -> T:
        if other == 0 or self.mod == 1:
            return self.__class__(0 if self.mod == 1 else 1)
        if other > 0:
            b, e, v = self.n, other, 1
        else:
            b, e, v = _ModIntCore._inv_mod(self.n, self.mod), - other, 1
        while e:
            if e & 1:
                v: int = v * b % self.mod
            b: int = b * b % self.mod
            e >>= 1
        return self.__class__(v)
    def inv[T](self: T) -> T:  #modint ** -1
        return self.__class__(_ModIntCore._inv_mod(self.n, self.mod))
    #演算: ビットシフト
    def __lshift__[T](self: T, other: T) -> T:  #modint << other
        return self.__lshift__(other.n)
    def __lshift__[T](self: T, other: UInt) -> T:
        return self.__lshift__(int(other))
    def __lshift__[T](self: T, other: Int) -> T:
        return self.__lshift__(int(other))
    def __lshift__[T](self: T, other: int) -> T:
        if other < 0:
            raise ValueError(f'負の左シフトはできません。{self.n} << {other}')
        elif other == 0 or self.n == 0:
            return self
        else:
            return self.__class__(self.n * pow(2, other, self.mod) % self.mod)
    def __rshift__[T](self: T, other: T) -> T:  #modint >> other
        return self.__rshift__(other.n)
    def __rshift__[T](self: T, other: UInt) -> T:
        return self.__rshift__(int(other))
    def __rshift__[T](self: T, other: Int) -> T:
        return self.__rshift__(int(other))
    def __rshift__[T](self: T, other: int) -> T:
        if other < 0:
            raise ValueError(f'負の右シフトはできません。{self.n} >> {other}')
        elif other == 0:
            return self
        elif self.mod & 1 == 0:
            raise ValueError(f'右シフトエラー: 2はmod {self.mod}で逆元を持ちません。')
        elif self.n == 0:
            return self
        else:
            i: int = (self.mod + 1) >> 1  #2の逆元をO(1)で計算
            if other > 1:
                i: int = pow(i, other, self.mod)
            return self.__class__(self.n * i % self.mod)
    #その他: 禁止演算
    def __floordiv__[T](self: T, other) -> T:
        raise TypeError('floordiv(//)演算は禁止です。truediv(/)を使ってください。')
    def __rfloordiv__[T, U](self: T, other: U) -> U:
        raise TypeError('floordiv(//)演算は禁止です。truediv(/)を使ってください。')
    def __mod__[T](self: T, other) -> T:
        raise TypeError('mod(%)演算は禁止です。')
    def __rmod__[T, U](self: T, other: U) -> U:
        raise TypeError('mod(%)演算は禁止です。')
