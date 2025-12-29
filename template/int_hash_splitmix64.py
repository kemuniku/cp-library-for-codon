#int hash値をSplitMix64で変更する
#Reference: https://prng.di.unimi.it/splitmix64.c
from random import getrandbits as _int_hash_random_getrandbits
_int_hash_random_base: int = _int_hash_random_getrandbits(63)
@extend
class int:
    def __hash__(self) -> int:
        z: UInt[64] = UInt[64](self ^ _int_hash_random_base)
        z += UInt[64](0x9e3779b97f4a7c15)
        z = (z ^ (z >> UInt[64](30))) * UInt[64](0xbf58476d1ce4e5b9)
        z = (z ^ (z >> UInt[64](27))) * UInt[64](0x94d049bb133111eb)
        return int(z ^ (z >> UInt[64](31)))
