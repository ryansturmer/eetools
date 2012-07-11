e6 = [100.0, 150.0, 220.0, 330.0, 470.0, 680.0]
e12 = [100.0, 120.0, 150.0, 180.0, 220.0, 270.0, 330.0, 390.0, 470.0, 560.0, 680.0, 820.0]
e24 = [100.0, 110.0, 120.0, 130.0, 150.0, 160.0, 180.0, 200.0, 220.0, 240.0, 270.0, 300.0, 330.0, 360.0, 390.0, 430.0, 470.0, 510.0, 560.0, 620.0, 680.0, 750.0, 820.0, 910.0]
e48 = [100.0, 105.0, 110.0, 115.0, 121.0, 127.0, 133.0, 140.0, 147.0, 154.0, 162.0, 169.0, 178.0, 187.0, 196.0, 205.0, 215.0, 226.0, 237.0, 249.0, 261.0, 274.0, 287.0, 301.0, 316.0, 332.0, 348.0, 365.0, 383.0, 402.0, 422.0, 442.0, 464.0, 487.0, 511.0, 536.0, 562.0, 590.0, 619.0, 649.0, 681.0, 715.0, 750.0, 787.0, 825.0, 866.0, 909.0, 953.0]
e96 = [100.0, 102.0, 105.0, 107.0, 110.0, 113.0, 115.0, 118.0, 121.0, 124.0, 127.0, 130.0, 133.0, 137.0, 140.0, 143.0, 147.0, 150.0, 154.0, 158.0, 162.0, 165.0, 169.0, 174.0, 178.0, 182.0, 187.0, 191.0, 196.0, 200.0, 205.0, 210.0, 215.0, 221.0, 226.0, 232.0, 237.0, 243.0, 249.0, 255.0, 261.0, 267.0, 274.0, 280.0, 287.0, 294.0, 301.0, 309.0, 316.0, 324.0, 332.0, 340.0, 348.0, 357.0, 365.0, 374.0, 383.0, 392.0, 402.0, 412.0, 422.0, 432.0, 442.0, 453.0, 464.0, 475.0, 487.0, 499.0, 511.0, 523.0, 536.0, 549.0, 562.0, 576.0, 590.0, 604.0, 619.0, 634.0, 649.0, 665.0, 681.0, 698.0, 715.0, 732.0, 750.0, 768.0, 787.0, 806.0, 825.0, 845.0, 866.0, 887.0, 909.0, 931.0, 953.0, 976.0]

class ValueList(object):

    def __init__(self, data):
        self.data = sorted(data)

    def nearest(self, value):
        pass

    def nearest_above(self, value):
        pass

    def nearest_below(self, value):
        pass

    def __iter__(self):
        return iter(self.data)


