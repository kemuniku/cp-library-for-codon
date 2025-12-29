#floatの出力精度を有効数字15桁に変更
@extend
class float:
    def __str__(self): return f'{self:.15g}'
