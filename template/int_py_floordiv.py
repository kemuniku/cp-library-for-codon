#int同士の除算結果をPythonの負の無限大丸めに合わせる
@extend
class int:
    @pure
    @llvm
    def _floordiv_int_int(self: int, other: int) -> int:
        %0 = sdiv i64 %self, %other
        ret i64 %0
    @overload
    def __floordiv__(self, other: int):
        d = self._floordiv_int_int(other)
        m = self - d * other
        if m and ((other ^ m) < 0):
            d -= 1
        return d
    @pure
    @llvm
    def _mod_int_int(self: int, other: int) -> int:
        %0 = srem i64 %self, %other
        ret i64 %0
    @overload
    def __mod__(self, other: int) -> int:
        m = self._mod_int_int(other)
        if m and ((other ^ m) < 0):
            m += other
        return m

#Int[N](N <= 128)同士の除算結果をPythonの負の無限大丸めに合わせる
@extend
class Int:
    def __floordiv__(self, other: Int[N]) -> Int[N]:
        if N > 128:
            compile_error("division is not supported on Int[N] when N > 128")
        d = self._floordiv(other)
        m = self - d * other
        if m and ((other ^ m) < Int[N](0)):
            d -= Int[N](1)
        return d
    def __mod__(self, other: Int[N]) -> Int[N]:
        if N > 128:
            compile_error("modulus is not supported on Int[N] when N > 128")
        m = self._mod(other)
        if m and ((other ^ m) < Int[N](0)):
            m += other
        return m
