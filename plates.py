class Plate():
    def __init__(self, x, y):
        self.clicked = False
        self.amount = 1
        self.mine = False
        self.opened = False
        self.flag = False
        self.x = x
        self.y = y
        # self.size = size

    def getHasMine(self):
        return self.mine

    def getHasFlag(self):
        return self.flag

    def getAmount(self):
        return self.amount
