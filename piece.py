from tile import Tile
BOARD_SIDE = 20

class Piece:
    __x : int
    __y : int

    """
    Represents a single piece. Holds all tiles in the piece in a list, keeps track of center
    tile for use in rotation/flipping
    """

    def __init__(self, color=0, t1=None, t2=None, t3=None, t4=None, t5=None):
        self.args = [t1, t2, t3, t4, t5]
        self.tiles = []  # list containing the tiles that make up the piece
        self.center = None  # tile to rotate around
        self.row = BOARD_SIDE//2
        self.col = BOARD_SIDE//2

        for tile in self.args:  # add all passed in tiles to list
            if tile is not None:
                self.tiles.append(tile)
                tile.setColor(color)

    # getters/Setters
    def getRow(self):
        return self.row

    def getCol(self):
        return self.col

    def setRow(self, row):
        checked = []
        if (self.__tileBoundCheck(self.center, row, self.col, checked)):
            self.row = row
            self.updatePositions()
            return True
        return False

    def setCol(self, col):
        checked = []
        if (self.__tileBoundCheck(self.center, self.row, col, checked)):
            self.col = col
            self.updatePositions()
            return True
        return False

    def __tileBoundCheck(self, tile: Tile, row, col, checked) -> bool:
        checked.append(tile)
        if (col >= 0 and col < BOARD_SIDE and row >= 0 and row < BOARD_SIDE):
            up = True
            down = True
            right = True
            left = True
            if tile.getUp() != 0 and tile.getUp() not in checked:
                up = self.__tileBoundCheck(tile.getUp(), row - 1, col, checked)
            if tile.getDown() != 0 and tile.getDown() not in checked:
                down = self.__tileBoundCheck(tile.getDown(), row + 1, col, checked)
            if tile.getRight() != 0 and tile.getRight() not in checked:
                right = self.__tileBoundCheck(tile.getRight(), row, col + 1, checked)
            if tile.getLeft() != 0 and tile.getLeft() not in checked:
                left = self.__tileBoundCheck(tile.getLeft(), row, col - 1, checked)
            return up and down and left and right

    def setCenter(self, c):
        self.center = c

    def getCenter(self):
        return self.center

    def getTiles(self):
        return self.tiles

    """
    Method to rotate the piece one-quarter, clockwise
    """
    def rotate(self):
            stack = []
            center = self.getCenter()
            # load center tile into stack, followed by all its immediate neighbors
            stack.append(center)
            if center.getUp() != 0:
                stack.append(center.getUp())
            if center.getRight() != 0:
                stack.append(center.getRight())
            if center.getDown() != 0:
                stack.append(center.getDown())
            if center.getLeft() != 0:
                stack.append(center.getLeft())

            # start with the outer layer, rotate any tiles that connect to it that ARE NOT THE CENTER
            while len(stack) != 0:
                top = 0
                right = 0
                left = 0
                down = 0
                t = stack.pop()
                top = t.getUp()
                right = t.getRight()
                down = t.getDown()
                left = t.getLeft()
                skip = 0
                if t != center:
                    if t.getUp() != 0 and t.getUp() != center:
                        t.setRight(top)
                        skip = 1
                        t.setUp(0)
                        top.setLeft(t)
                        top.setDown(0)
                    if t.getRight() != 0 and t.getRight() != center and skip == 0:
                        skip = 0
                        t.setDown(right)
                        skip = 1
                        t.setRight(0)
                        right.setUp(t)
                        right.setLeft(0)

                    if t.getDown() != 0 and t.getDown() != center and skip == 0:
                        skip = 0
                        t.setLeft(down)
                        skip = 1
                        t.setDown(0)
                        down.setRight(t)
                        down.setUp(0)
                    if t.getLeft() != 0 and t.getLeft() != center and skip == 0:
                        skip = 0
                        t.setUp(left)
                        skip = 1
                        t.setLeft(0)
                        left.setDown(t)
                        left.setRight(0)
                # for the center tile, if an edge is not 0, then rotate all the tiles
                if t == center:
                    if top != 0:
                        t.setRight(top)
                        t.setUp(0)
                        top.setLeft(t)
                        if top.getDown() == center:
                            top.setDown(0)

                    if right != 0:
                        t.setDown(right)
                        # if the right tile has already been updated, dont over-write it
                        if right == t.getRight():
                            t.setRight(0)
                        right.setUp(t)
                        if right.getLeft() == center:
                            right.setLeft(0)
                    if down != 0:
                        t.setLeft(down)
                        if down == t.getDown():
                            t.setDown(0)
                        down.setRight(t)
                        if down.getUp() == center:
                            down.setUp(0)
                    if left != 0:
                        t.setUp(left)
                        if left == t.getLeft():
                            t.setLeft(0)
                        left.setDown(t)
                        if left.getRight() == center:
                            left.setRight(0)

            outOfBounds = False
            for tile in self.tiles:
                if tile.getCol() < 0 or tile.getRow() < 0 or tile.getCol() > 19 or tile.getRow() > 19:
                    outOfBounds = True

            counter = 0
            while counter < 3 and outOfBounds:
                stack = []
                center = self.getCenter()
                # load center tile into stack, followed by all its immediate neighbors
                stack.append(center)
                if center.getUp() != 0:
                    stack.append(center.getUp())
                if center.getRight() != 0:
                    stack.append(center.getRight())
                if center.getDown() != 0:
                    stack.append(center.getDown())
                if center.getLeft() != 0:
                    stack.append(center.getLeft())

                # start with the outer layer, rotate any tiles that connect to it that ARE NOT THE CENTER
                while len(stack) != 0:
                    top = 0
                    right = 0
                    left = 0
                    down = 0
                    t = stack.pop()
                    top = t.getUp()
                    right = t.getRight()
                    down = t.getDown()
                    left = t.getLeft()
                    skip = 0
                    if t != center:
                        if t.getUp() != 0 and t.getUp() != center:
                            t.setRight(top)
                            skip = 1
                            t.setUp(0)
                            top.setLeft(t)
                            top.setDown(0)
                        if t.getRight() != 0 and t.getRight() != center and skip == 0:
                            skip = 0
                            t.setDown(right)
                            skip = 1
                            t.setRight(0)
                            right.setUp(t)
                            right.setLeft(0)

                        if t.getDown() != 0 and t.getDown() != center and skip == 0:
                            skip = 0
                            t.setLeft(down)
                            skip = 1
                            t.setDown(0)
                            down.setRight(t)
                            down.setUp(0)
                        if t.getLeft() != 0 and t.getLeft() != center and skip == 0:
                            skip = 0
                            t.setUp(left)
                            skip = 1
                            t.setLeft(0)
                            left.setDown(t)
                            left.setRight(0)
                    # for the center tile, if an edge is not 0, then rotate all the tiles
                    if t == center:
                        if top != 0:
                            t.setRight(top)
                            t.setUp(0)
                            top.setLeft(t)
                            if top.getDown() == center:
                                top.setDown(0)

                        if right != 0:
                            t.setDown(right)
                            # if the right tile has already been updated, dont over-write it
                            if right == t.getRight():
                                t.setRight(0)
                            right.setUp(t)
                            if right.getLeft() == center:
                                right.setLeft(0)
                        if down != 0:
                            t.setLeft(down)
                            if down == t.getDown():
                                t.setDown(0)
                            down.setRight(t)
                            if down.getUp() == center:
                                down.setUp(0)
                        if left != 0:
                            t.setUp(left)
                            if left == t.getLeft():
                                t.setLeft(0)
                            left.setDown(t)
                            if left.getRight() == center:
                                left.setRight(0)
                counter += 1

            self.updatePositions()

    def flip(self):
        stack = []
        center = self.getCenter()
        # load center tile into stack, followed by all its immediate neighbors
        stack.append(center)
        if center.getUp() != 0:
            stack.append(center.getUp())
        if center.getRight() != 0:
            stack.append(center.getRight())
        if center.getDown() != 0:
            stack.append(center.getDown())
        if center.getLeft() != 0:
            stack.append(center.getLeft())

        # start with the outer layer, rotate any tiles that connect to it that ARE NOT THE CENTER
        while len(stack) != 0:
            top = 0
            right = 0
            left = 0
            down = 0
            t = stack.pop()
            top = t.getUp()
            right = t.getRight()
            down = t.getDown()
            left = t.getLeft()
            skip = 0
            if t != center:
                if t.getRight() != 0 and t.getRight() != center and skip == 0:
                    skip = 0
                    t.setLeft(right)
                    skip = 1
                    t.setRight(0)
                    right.setRight(t)
                    right.setLeft(0)

                if t.getLeft() != 0 and t.getLeft() != center and skip == 0:
                    skip = 0
                    t.setRight(left)
                    skip = 1
                    t.setLeft(0)
                    left.setLeft(t)
                    left.setRight(0)

            if t == center:
                if right != 0:
                    t.setLeft(right)
                    right.setRight(t)
                    if right.getLeft() == center:
                        right.setLeft(0)
                    t.setRight(0)

                if left != 0:
                    t.setRight(left)
                    left.setLeft(t)

                    if left.getRight() == center:
                        left.setRight(0)
                    if t.getLeft() == t.getRight():
                        t.setLeft(0)
        self.updatePositions()

    """
        Method to update the row and col coordinates for every tile in a piece. Takes in the coordinates for the 
        center tile as arguments, and adjusts the coordinates for every other tile in the piece accordingly
    """

    def updatePositions(self):  # takes in the new row and column values of the CENTER TILE
        stack = []
        center = self.getCenter()
        # load center tile into stack, followed by all its immediate neighbors
        stack.append(center)
        if center.getUp() != 0:
            stack.append(center.getUp())
        if center.getRight() != 0:
            stack.append(center.getRight())
        if center.getDown() != 0:
            stack.append(center.getDown())
        if center.getLeft() != 0:
            stack.append(center.getLeft())
        while len(stack) > 0:
            T = stack.pop(0)
            c = self.getCenter()
            # update center, work outwards
            if T == c:
                T.setRow(self.row)
                T.setCol(self.col)
            # centers direct neighbors
            if T.getRight() == c:
                T.setRow(c.getRow())
                T.setCol(c.getCol() - 1)
            if T.getLeft() == c:
                T.setRow(c.getRow())
                T.setCol(c.getCol() + 1)
            if T.getUp() == c:
                T.setRow(c.getRow() + 1)
                T.setCol(c.getCol())
            if T.getDown() == c:
                T.setRow(c.getRow() - 1)
                T.setCol(c.getCol())
            # third layer
            right = -1
            left = -1
            up = -1
            down = -1

            if T.getRight() != c and T.getRight() != 0 and T != c:
                right = T.getRight()
            if T.getLeft() != c and T.getLeft() != 0 and T != c:
                left = T.getLeft()
            if T.getUp() != c and T.getUp() != 0 and T != c:
                up = T.getUp()
            if T.getDown() != c and T.getDown() != 0 and T != c:
                down = T.getDown()
            if right != -1:
                right.setRow(T.getRow())
                right.setCol(T.getCol() + 1)
            if left != -1:
                left.setRow(T.getRow())
                left.setCol(T.getCol() - 1)
            if up != -1:
                up.setRow(T.getRow() - 1)
                up.setCol(T.getCol())
            if down != -1:
                down.setRow(T.getRow() + 1)
                down.setCol(T.getCol())

    """
    Method to print out the pieces the player currently has in the console version
    """

    def printPiece(self, p: int):  # p is the index of the piece in the players pieces list
        print = "" + str(p) + "\n"
        if p == 0:
            print += "x"
        if p == 1:
            print += "xx"
        if p == 2:
            print += "xx\n"
            print += " x\n"
        if p == 3:
            print += "xxx"
        if p == 4:
            print += "xx\n"
            print += "xx"
        if p == 5:
            print += " x \n"
            print += "xxx"
        if p == 6:
            print += "xxxx"
        if p == 7:
            print += "  x\n"
            print += "xxx"
        if p == 8:
            print += " xx\n"
            print += "xx "
        if p == 9:
            print += "x   \n"
            print += "xxxx"
        if p == 10:
            print += " x \n"
            print += " x \n"
            print += "xxx"
        if p == 11:
            print += "x  \n"
            print += "x  \n"
            print += "xxx"
        if p == 12:
            print += " xxx\n"
            print += "xx  "
        if p == 13:
            print += "  x\n"
            print += "xxx\n"
            print += "x  "
        if p == 14:
            print += "x\n"
            print += "x\n"
            print += "x\n"
            print += "x\n"
            print += "x\n"
        if p == 15:
            print += "x \n"
            print += "xx\n"
            print += "xx\n"
        if p == 16:
            print += " xx \n"
            print += "xx \n"
            print += "x  \n"
        if p == 17:
            print += "xx\n"
            print += "x \n"
            print += "xx\n"
        if p == 18:
            print += " xx\n"
            print += "xx \n"
            print += " x \n"
        if p == 19:
            print += " x \n"
            print += "xxx\n"
            print += " x \n"
        if p == 20:
            print += " x \n"
            print += "xxxx\n"
        print += "\n_______"

        return print

    """
    Methods to create the pieces. Each method first
    creates tile objects, then sets edges accordingly
    (0 (default) if the edge is empty, otherwise the tile object it shares an edge with if it has a neighbor)
    the tiles used to create a piece object, which is then returned.
    """
    def decoy(self, color):
        t1 = Tile()
        piece = Piece(color, t1)
        piece.setCenter(t1)
        return piece

    def pieceA(self, color):
        t1 = Tile()
        piece = Piece(color, t1)
        piece.setCenter(t1)
        piece.setCol(10)
        piece.setRow(10)
        return piece

    def pieceB(self, color):
        t1 = Tile()
        t2 = Tile()
        t1.setRight(t2)
        t2.setLeft(t1)
        piece = Piece(color, t1, t2)
        piece.setCenter(t1)
        piece.setCol(10)
        piece.setRow(10)
        return piece

    def pieceC(self, color):
        t1 = Tile()
        t2 = Tile()
        t3 = Tile()
        t1.setRight(t2)
        t2.setLeft(t1)
        t2.setDown(t3)
        t3.setUp(t2)
        piece = Piece(color, t1, t2, t3)
        piece.setCenter(t2)
        piece.setCol(10)
        piece.setRow(10)
        return piece

    def pieceD(self, color):
        t1 = Tile()
        t2 = Tile()
        t3 = Tile()
        t1.setRight(t2)
        t2.setLeft(t1)
        t2.setRight(t3)
        t3.setLeft(t2)
        piece = Piece(color, t1, t2, t3)
        piece.setCenter(t2)
        piece.setCol(10)
        piece.setRow(10)
        return piece

    def pieceE(self, color):
        t1 = Tile()
        t2 = Tile()
        t3 = Tile()
        t4 = Tile()
        t1.setRight(t2)
        t2.setLeft(t1)
        t1.setDown(t3)
        t2.setDown(t4)
        t4.setUp(t2)
        t3.setUp(t1)
        t3.setRight(t4)
        t4.setLeft(t3)
        piece = Piece(color, t1, t2, t3, t4)
        piece.setCenter(t1)
        piece.setCol(10)
        piece.setRow(10)
        return piece

    def pieceF(self, color):
        t1 = Tile()
        t2 = Tile()
        t3 = Tile()
        t4 = Tile()
        t1.setDown(t3)
        t2.setRight(t3)
        t3.setLeft(t2)
        t3.setUp(t1)
        t3.setRight(t4)
        t4.setLeft(t3)
        piece = Piece(color, t1, t2, t3, t4)
        piece.setCenter(t3)
        piece.setCol(piece.getCenter().getCol())
        piece.setRow(piece.getCenter().getRow())
        return piece

    def pieceG(self, color):
        t1 = Tile()
        t2 = Tile()
        t3 = Tile()
        t4 = Tile()
        t1.setRight(t2)
        t2.setLeft(t1)
        t2.setRight(t3)
        t3.setLeft(t2)
        t3.setRight(t4)
        t4.setLeft(t3)
        piece = Piece(color, t1, t2, t3, t4)
        piece.setCenter(t2)
        piece.setCol(10)
        piece.setRow(10)
        return piece

    def pieceH(self, color):
        t1 = Tile()
        t2 = Tile()
        t3 = Tile()
        t4 = Tile()
        t1.setDown(t4)
        t2.setRight(t3)
        t3.setLeft(t2)
        t3.setRight(t4)
        t4.setLeft(t3)
        t4.setUp(t1)
        piece = Piece(color, t1, t2, t3, t4)
        piece.setCenter(t3)
        piece.setCol(10)
        piece.setRow(10)
        return piece

    def pieceI(self, color):
        t1 = Tile()
        t2 = Tile()
        t3 = Tile()
        t4 = Tile()
        t1.setRight(t2)
        t2.setLeft(t1)
        t2.setUp(t3)
        t3.setDown(t2)
        t3.setRight(t4)
        t4.setLeft(t3)
        piece = Piece(color, t1, t2, t3, t4)
        piece.setCenter(t2)
        piece.setCol(10)
        piece.setRow(10)
        return piece

    def pieceJ(self, color):
        t1 = Tile()
        t2 = Tile()
        t3 = Tile()
        t4 = Tile()
        t5 = Tile()
        t1.setDown(t2)
        t2.setUp(t1)
        t2.setRight(t3)
        t3.setLeft(t2)
        t3.setRight(t4)
        t4.setLeft(t3)
        t4.setRight(t5)
        t5.setLeft(t4)
        piece = Piece(color, t1, t2, t3, t4, t5)
        piece.setCenter(t3)
        piece.setCol(10)
        piece.setRow(10)
        return piece

    def pieceK(self, color):
        t1 = Tile()
        t2 = Tile()
        t3 = Tile()
        t4 = Tile()
        t5 = Tile()
        t1.setRight(t2)
        t2.setLeft(t1)
        t2.setUp(t4)
        t2.setRight(t3)
        t3.setLeft(t2)
        t4.setDown(t2)
        t4.setUp(t5)
        t5.setDown(t4)
        piece = Piece(color, t1, t2, t3, t4, t5)
        piece.setCenter(t2)
        piece.setCol(10)
        piece.setRow(10)
        return piece

    def pieceL(self, color):
        t1 = Tile()
        t2 = Tile()
        t3 = Tile()
        t4 = Tile()
        t5 = Tile()
        t1.setDown(t2)
        t2.setUp(t1)
        t2.setDown(t3)
        t3.setUp(t2)
        t3.setRight(t4)
        t4.setLeft(t3)
        t4.setRight(t5)
        t5.setLeft(t4)
        piece = Piece(color, t1, t2, t3, t4, t5)
        piece.setCenter(t3)
        piece.setCol(10)
        piece.setRow(10)
        return piece

    def pieceM(self, color):
        t1 = Tile()
        t2 = Tile()
        t3 = Tile()
        t4 = Tile()
        t5 = Tile()
        t1.setRight(t2)
        t2.setLeft(t1)
        t2.setUp(t3)
        t3.setDown(t2)
        t3.setRight(t4)
        t4.setLeft(t3)
        t4.setRight(t5)
        t5.setLeft(t4)
        piece = Piece(color, t1, t2, t3, t4, t5)
        piece.setCenter(t3)
        piece.setCol(10)
        piece.setRow(10)
        return piece

    def pieceN(self, color):
        t1 = Tile()
        t2 = Tile()
        t3 = Tile()
        t4 = Tile()
        t5 = Tile()
        t1.setDown(t4)
        t2.setDown(t5)
        t2.setRight(t3)
        t3.setLeft(t2)
        t3.setRight(t4)
        t4.setLeft(t3)
        t4.setUp(t1)
        t5.setUp(t2)
        piece = Piece(color, t1, t2, t3, t4, t5)
        piece.setCenter(t3)
        piece.setCol(10)
        piece.setRow(10)
        return piece

    def pieceO(self, color):
        t1 = Tile()
        t2 = Tile()
        t3 = Tile()
        t4 = Tile()
        t5 = Tile()
        t1.setDown(t2)
        t2.setUp(t1)
        t2.setDown(t3)
        t3.setUp(t2)
        t3.setDown(t4)
        t4.setUp(t3)
        t4.setDown(t5)
        t5.setUp(t4)
        piece = Piece(color, t1, t2, t3, t4, t5)
        piece.setCenter(t3)
        piece.setCol(10)
        piece.setRow(10)
        return piece

    def pieceP(self, color):
        t1 = Tile()
        t2 = Tile()
        t3 = Tile()
        t4 = Tile()
        t5 = Tile()
        t1.setDown(t2)
        t2.setUp(t1)
        t2.setRight(t3)
        t2.setDown(t4)
        t3.setLeft(t2)
        t3.setDown(t5)
        t4.setUp(t2)
        t4.setRight(t5)
        t5.setUp(t3)
        t5.setLeft(t4)
        piece = Piece(color, t1, t2, t3, t4, t5)
        piece.setCenter(t2)
        piece.setCol(10)
        piece.setRow(10)
        return piece

    def pieceQ(self, color):
        t1 = Tile()
        t2 = Tile()
        t3 = Tile()
        t4 = Tile()
        t5 = Tile()
        t1.setUp(t2)
        t2.setDown(t1)
        t2.setRight(t3)
        t3.setLeft(t2)
        t3.setUp(t4)
        t4.setDown(t3)
        t4.setRight(t5)
        t5.setLeft(t4)
        piece = Piece(color, t1, t2, t3, t4, t5)
        piece.setCenter(t3)
        piece.setCol(10)
        piece.setRow(10)
        return piece

    def pieceR(self, color):
        t1 = Tile()
        t2 = Tile()
        t3 = Tile()
        t4 = Tile()
        t5 = Tile()
        t1.setRight(t2)
        t1.setDown(t3)
        t2.setLeft(t1)
        t3.setUp(t1)
        t3.setDown(t4)
        t4.setUp(t3)
        t4.setRight(t5)
        t5.setLeft(t4)
        piece = Piece(color, t1, t2, t3, t4, t5)
        piece.setCenter(t3)
        piece.setCol(10)
        piece.setRow(10)
        return piece

    def pieceS(self, color):
        t1 = Tile()
        t2 = Tile()
        t3 = Tile()
        t4 = Tile()
        t5 = Tile()
        t1.setUp(t2)
        t2.setDown(t1)
        t2.setLeft(t3)
        t3.setRight(t2)
        t2.setUp(t4)
        t4.setDown(t2)
        t4.setRight(t5)
        t5.setLeft(t4)
        piece = Piece(color, t1, t2, t3, t4, t5)
        piece.setCenter(t2)
        piece.setCol(10)
        piece.setRow(10)
        return piece

    def pieceT(self, color):
        t1 = Tile()
        t2 = Tile()
        t3 = Tile()
        t4 = Tile()
        t5 = Tile()
        t1.setDown(t3)
        t2.setRight(t3)
        t3.setUp(t1)
        t3.setRight(t4)
        t3.setDown(t5)
        t3.setLeft(t2)
        t4.setLeft(t3)
        t5.setUp(t3)
        piece = Piece(color, t1, t2, t3, t4, t5)
        piece.setCenter(t3)
        piece.setCol(10)
        piece.setRow(10)
        return piece

    def pieceU(self, color):
        t1 = Tile()
        t2 = Tile()
        t3 = Tile()
        t4 = Tile()
        t5 = Tile()
        t1.setRight(t2)
        t2.setLeft(t1)
        t2.setUp(t3)
        t3.setDown(t2)
        t2.setRight(t4)
        t4.setLeft(t2)
        t4.setRight(t5)
        t5.setLeft(t4)
        piece = Piece(color, t1, t2, t3, t4, t5)
        piece.setCenter(t2)
        piece.setCol(10)
        piece.setRow(10)
        return piece

    """
    Method to create all of the pieces, store them in a list, and return the list
    """

    def createPieces(self, color):
        piecesList = []

        a = self.pieceA(color)
        piecesList.append(a)
        b = self.pieceB(color)
        piecesList.append(b)
        c = self.pieceC(color)
        piecesList.append(c)
        d = self.pieceD(color)
        piecesList.append(d)
        e = self.pieceE(color)
        piecesList.append(e)
        f = self.pieceF(color)
        piecesList.append(f)
        g = self.pieceG(color)
        piecesList.append(g)
        h = self.pieceH(color)
        piecesList.append(h)
        i = self.pieceI(color)
        piecesList.append(i)
        j = self.pieceJ(color)
        piecesList.append(j)
        k = self.pieceK(color)
        piecesList.append(k)
        l = self.pieceL(color)
        piecesList.append(l)
        m = self.pieceM(color)
        piecesList.append(m)
        n = self.pieceN(color)
        piecesList.append(n)
        o = self.pieceO(color)
        piecesList.append(o)
        p = self.pieceP(color)
        piecesList.append(p)
        q = self.pieceQ(color)
        piecesList.append(q)
        r = self.pieceR(color)
        piecesList.append(r)
        s = self.pieceS(color)
        piecesList.append(s)
        t = self.pieceT(color)
        piecesList.append(t)
        u = self.pieceU(color)
        piecesList.append(u)

        return piecesList
