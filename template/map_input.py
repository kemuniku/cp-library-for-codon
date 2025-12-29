#map入力受取(疑似対応)
@extend
class Generator:
    def __getitem__(self: Generator[T], _: int) -> T:
        if self.done(): raise StopIteration()
        return self.next()
    def __getitem__(self: Generator[T], key: slice) -> list[T]:
        assert key.stop is None, (
            '''本拡張では、末尾以外でのアンパッキングはできません。
            例として、 N, *A = generator には対応しますが *A, N = generator は非対応です。
            右辺をlistにキャストした、 list(generator) に変更してください。''')
        return list(self)
    def __contains__(self: Generator[T], key: T) -> bool:
        return key in list(self)
