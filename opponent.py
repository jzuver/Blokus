from player import Player
from piece import Piece
from tile import Tile
import random


class Opponent(Player):
    """
    The constructor
    game: a Game, the game the player is apart of
    player: a Player, so Opponent can have access to same fields and functions as Player 
    color: a str, the color of the opponent, id
    """

    def __init__(self, color: str):
        self.__optimalMove = Piece()
        self.__optimalBlock = Piece()
        super().__init__(color)


    # choosePiece uses isValidSelection
    def choosePiece(self) -> Piece:
        available = self.getBoard().getAvailableSpots(self.color)
        validMoves = []  # list[list[Piece, rotations, flips, x, y]] eg [[PieceA (memory address), 2, 1, 2, 5], [PieceB, 1, 0, 10 3]]
        for piece in self.getPieces():
            for i in range(4):
                for coord in available:
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

        if len(validMoves) > 0:
            move = validMoves[random.randint(0, len(validMoves) - 1)]
            piece = move[0]
            piece.setCol(10)
            piece.setRow(10)
            self.getPieces().remove(piece)
            for r in range(move[1]):
                piece.rotate()
            # waiting on flip
            # if move[2] == 1:
            #    piece.flip()
            piece.setCol(move[3])
            piece.setRow(move[4])

            return piece
        return None

