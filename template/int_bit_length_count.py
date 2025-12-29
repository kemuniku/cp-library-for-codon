#int.bit_length, int.bit_countに対応
@extend
class int:
    def bit_length(self): 
        return 64 - abs(self).__ctlz__()
    def bit_count(self):
        return abs(self).__ctpop__()
