class Tile:

    def __init__(self, up=0, right=0, down=0, left=0, color="blank", row=10, col=10):
        self.up = up
        self.right = right
        self.down = down
        self.left = left
        self.color = color
        self.row = row
        self.col = col

    def getUp(self):
        return self.up

    def getRight(self):
        return self.right

    def getDown(self):
        return self.down

    def getLeft(self):
        return self.left

    def getColor(self):
        return self.color

    def getRow(self):
        return self.row

    def getCol(self):
        return self.col

    def setUp(self, u):
        self.up = u

    def setRight(self, r):
        self.right = r

    def setDown(self, d):
        self.down = d

    def setLeft(self, l):
        self.left = l

    def setColor(self, c):
        self.color = c

    def setRow(self, r):
        self.row = r

    def setCol(self,c):
        self.col = c
