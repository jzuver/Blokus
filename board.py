# Board Class

from tile import Tile
from piece import Piece


class Board:
    def __init__(self, rows, columns):
        self.__columns = columns
        self.__rows = rows
        self.__pieces = []
        self.__grid = []
        self.__initializeBoard()

    def __initializeBoard(self):
        for row in range(self.__rows):
            self.__grid.append([])
            for column in range(self.__columns):
                self.__grid[row].append(0)
        # add one tile in each corner for all four players
        self.__grid[19][0] = Tile(0, 0, 0, 0, "Green", 19, 0)
        self.__grid[0][0] = Tile(0, 0, 0, 0, "Red", 0, 0)
        self.__grid[0][19] = Tile(0, 0, 0, 0, "Blue", 0, 19)
        self.__grid[19][19] = Tile(0, 0, 0, 0, "Yellow", 19, 19)

    # Create string representation of the board
    def __str__(self) -> str:
        board = ""
        for r in range(self.__rows):
            if r < 10:
                board += " "+str(r)
            else:
                board += str(r)
            for c in range(self.__columns):
                if self.__grid[r][c] == 0:  # condition if r,c coordinate is empty
                    board += " . "
                else:  # condition there is a tile there
                    board += " " + self.__grid[r][c].getColor().lower()[0] + " "
            board += "\n"
        board += "\n   0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18 19"
        return board

    # Get pieces played on the board
    def getPiecesPlayed(self):  # -> [Piece]:
        return self.__pieces

    def getPiece(self, center: Tile):  # -> Piece:
        for piece in self.__pieces:
            # NOTE: this is down under the assumption that Tile has an overloaded comparision operator
            # that compares the coordinates of tiles
            if piece.getCenter().equals(center):
                return piece
            else:
                return None

    # playPiece function updates the board's grid
    # NOTE: assumes that piece has a getTiles function that returns a list of tiles
    # Piece knows where it is from the center tile, tile has a coordinate (row, column)
    def updateGrid(self, selectedPiece: Piece) -> bool:
        if selectedPiece is not None and selectedPiece.getCenter().getRow() < 0 or selectedPiece.getCenter().getRow() > self.__rows:
            return False
        if selectedPiece is not None and selectedPiece.getCenter().getCol() < 0 or selectedPiece.getCenter().getCol() > self.__columns:
            return False
        else:
            for tile in selectedPiece.getTiles():
                if self.__grid[tile.getRow()][tile.getCol()] == 0:
                    self.__grid[tile.getRow()][tile.getCol()] = tile
                else:
                    return False
            self.__pieces.append(selectedPiece)
            return True

    def getGrid(self) -> [[int]]:
        return self.__grid

    # Finds all available spots for a player
    def getAvailableSpots(self, color) -> [[int]]:
        available = []
        for x in range(self.__columns):
            for y in range(self.__rows):
                if self.__grid[x][y] != 0 and self.__grid[x][y].getColor() == color:
                    for i in range(x - 1, x + 2):
                        for j in range(y - 1, y + 2):
                            if i < 0 or i >= 20 or j < 0 or j >= 20:
                                continue
                            if self.__grid[i][j] == 0 and [i, j] not in available:
                                available.append([j, i])
        return available
    def isValidSelect(self, piece) ->bool:
        isValid = True
        for tile in piece.getTiles():
            x = tile.getCol()
            y = tile.getRow()
            if self.getGrid()[y][x] != 0:
                isValid = False
            if x < 0 or x > 19:
                isValid = False
            if y < 0 or y > 19:
                isValid = False

        return isValid
    def isValidSelection(self, piece: Piece) -> bool:
        for tile in piece.getTiles():
            if tile.getCol() < 0 or tile.getRow() < 0 or tile.getCol() > 19 or tile.getRow() > 19:
                return False
        check = self.__checkTile(piece.getRow(), piece.getCol(), piece.getCenter(), [], piece.getCenter().getColor())
        return check[0] and check[1]

    def __checkTile(self, row : int, col : int, tile: Tile, checked: [Tile], color: str) -> [bool]:
        checked.append(tile)
        if self.__grid[row][col] != 0:
            return [False, False]
        up = [True, False]
        down = [True, False]
        left = [True, False]
        right = [True, False]

        if tile.getUp() != 0 and tile.getUp() not in checked:
            up = self.__checkTile(row - 1, col, tile.getUp(), checked, color)
        if tile.getDown() != 0 and tile.getDown() not in checked:
            down = self.__checkTile(row + 1, col, tile.getDown(), checked, color)
        if tile.getRight() != 0 and tile.getRight() not in checked:
            right = self.__checkTile(row, col + 1, tile.getRight(), checked, color)
        if tile.getLeft() != 0 and tile.getLeft() not in checked:
            left = self.__checkTile(row, col - 1, tile.getLeft(), checked, color)

        around = False
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if i < 0 or i >= 20 or j < 0 or j >= 20:
                    continue
                if self.__grid[i][j] != 0 and self.__grid[i][j].getColor() == color:
                    around = True
        return [up[0] and down[0] and left[0] and right[0], up[1] or down[1] or left[1] or right[1] or around]

    def getRows(self):
        return self.__rows

    def getColumns(self):
        return self.__columns

    # # Select tile on board, updates tile on the board
    # def selectTile(self, row, column) -> Tile:
    #     if row <= 0 or row > self.rows:
    #         print("Invalid row")
    #         return False
    #     if column <= 0 or column > self.columns:
    #         print("Invalid column")
    #         return False
    #     else: 
    #         if (self.__tiles[row][column].containsPiece() == True):
    #             print("There is a piece played on this space")
    #             return False
    #         else:
    #             self.__tiles[row][column].setSelected(True)
    #             return True

    # # deselect tile on board, updates tile on the board
    # def deselectTile(self, row, column) -> Tile:
    #     if row <= 0 or row > self.rows:
    #         print("Invalid row")
    #         return False
    #     if column <= 0 or column > self.columns:
    #         print("Invalid column")
    #         return False
    #     else: 
    #         if (self.__tiles[row][column].getSelected() == True):
    #             self.__tiles[row][column].setSelected(False)
    #             return True
    #         else:
    #             print("Space not selected")
    #             return False
