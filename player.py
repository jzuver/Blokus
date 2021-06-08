from piece import Piece
from tile import Tile
from board import Board
class Player:
    """
	The constructor
	game: a Game, the game the player is apart of
	color: a str, the color of the player
	"""

    def __init__(self, color="blank"):
        from game import Game

        self.color = color
        # intialize Pieces
        self.__pieces = Piece().createPieces(color)
        self.__selectedPiece = 0
        self.__playedLastPiece = False

    def setBoard(self, b: Board):
        self.__game = b

    def getBoard(self):
        return self.__game
    """
    toSelect: an int, the index in the array of pieces to select a new piece
    returns false if the index is out of bounds, true otherwise 
    """

    # def selectPiece(self, toSelect: int) -> bool:
    #     if self.__selectedPiece != 0:
    #         self.__pieces.append(self.__selectedPiece)
    #     if 0 <= toSelect < len(self.__pieces):
    #         # self.__pieces.append(self.__selectedPiece)
    #         #self.__selectedPiece = self.__pieces.pop(toSelect)
    #         #self.__pieces[toSelect] = 0
    #         return True
    #     else:
    #         return False

    def setPlayedLastPiece(self, b):
        self.__playedLastPiece = b

    def getPlayedLastPiece(self):
        return self.__playedLastPiece

    def getPlayedLastPiece(self):
        return self.__playedLastPiece

    def getSelectedPiece(self):
        return self.__selectedPiece

    def setSelectedPiece(self, piece):
        self.__selectedPiece = piece

    def setColor(self, c):
        self.color = c

    def getColor(self) -> str:
        return self.color

    def getPieces(self):
        return self.__pieces

    def printPieces(self):
        for i in range(len(self.getPieces())):
            pieceInQuestion = self.getPieces()[i]
            if pieceInQuestion != 0:
                print(self.getPieces()[i].printPiece(i))

    def getFinalScore(self, score : int):
        subtractPoints = 0
        for piece in self.__pieces:
            for tile in piece.getTiles():
                subtractPoints+=1
        finalScore = score - subtractPoints
        return finalScore

    """
	Does what the name of the method says to the selected piece
	"""

    def up(self) -> bool:
        return self.__selectedPiece.up()

    def down(self) -> bool:
        return self.__selectedPiece.down()

    def left(self) -> bool:
        return self.__selectedPiece.left()

    def right(self) -> bool:
        return self.__selectedPiece.right()

    def rotate(self) -> bool:
        return self.__selectedPiece.rotate()

    def flip(self) -> bool:
        return self.__selectedPiece.flip()

    """
	Returns the piece that is selected and selects the new piece at index 0
	"""

    def place(self):
        toReturn = self.__selectedPiece
        if len(self.getPieces()) == 0:
            self.__selectedPiece = Piece.decoy(Piece, self.color)

            self.__playedLastPiece = True
            return toReturn

        return toReturn

    def outOfMoves(self):
        available = self.__game.getAvailableSpots(self.color)
        validMoves = []  # list[list[Piece, rotations, flips, x, y]] eg [[PieceA (memory address), 2, 1, 2, 5], [PieceB, 1, 0, 10 3]]
        for piece in self.getPieces():
            for i in range(4):
                for coord in available:
                    running = True
                    checked = []
                    flips = 0
                    piece.setCol(coord[0])
                    piece.setRow(coord[1])
                    coords = self.tileCheck(piece, piece.getCenter(), checked, 0, 0)
                    for c in coords:
                        validMoves.append([piece, i, flips, c[0], c[1]])
                    piece.setCol(10)
                    piece.setRow(10)
                piece.rotate()
        return len(validMoves) == 0

    def tileCheck(self, piece: Piece, tile: Tile, checked: [Tile], xOffset, yOffset):  # list[list[x, y]]
        validMoves = []
        col = piece.setCol(piece.getCol() + xOffset)
        row = piece.setRow(piece.getRow() + yOffset)
        checked.append(tile)
        if self.__game.isValidSelection(piece):
            validMoves.append([piece.getCol(), piece.getRow()])
        up = []
        down = []
        right = []
        left = []
        if tile.getUp() != 0 and tile.getUp() not in checked:
            up = self.tileCheck(piece, tile.getUp(), checked, 0, -1)
        if tile.getDown() != 0 and tile.getDown() not in checked:
            down = self.tileCheck(piece, tile.getDown(), checked, 0, 1)
        if tile.getRight() != 0 and tile.getRight() not in checked:
            right = self.tileCheck(piece, tile.getRight(), checked, 1, 0)
        if tile.getLeft() != 0 and tile.getLeft() not in checked:
            left = self.tileCheck(piece, tile.getLeft(), checked, -1, 0)
        for li in [up, down, left, right]:
            for coord in li:
                validMoves.append(coord)
        if col:
            piece.setCol(piece.getCol() - xOffset)
        if row:
            piece.setRow(piece.getRow() - yOffset)
        return validMoves
    """
	Returns a string representation of all the pieces available to the player
	"""

    def __str__(self) -> str:
        out = ""
        for s in self.__pieces:
            out += s + "\n"
        return s
