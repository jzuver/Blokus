from piece import Piece
from board import Board
BOARD_SIDE = 20
class Game:
    def __init__(self):
        from board import Board
        from piece import Piece
        from tile import Tile
        from player import Player
        from opponent import Opponent
        self.__player = Player("Green")
        self.__board = Board(BOARD_SIDE, BOARD_SIDE)
        self.__opponents = [Opponent("Red"), Opponent("Blue"), Opponent("Yellow")]
        self.__winning = 0
        self.__winner = 0
        self.__scores = [0, 0, 0, 0] # [player, opp1, opp2, opp3]
        self.__turnCounter = 0
        self.__player.setBoard(self.__board)

    # updates the player score and if they are winning after the update, updates relevant fields
    def updateScore(self, p, i):
        scores = self.__scores
        winning = self.__winning
        winner = self.__winner
        self.__scores[p] += i
        for i in scores:
            if scores[i] > winning:
                winning = scores[i]
                winner = p
    def getWinner(self):
        finalScores = []
        finalScorePlayer = self.__player.getFinalScore(self.__scores[0])
        finalScore1 = self.__opponents[0].getFinalScore(self.__scores[1])
        finalScore2 = self.__opponents[1].getFinalScore(self.__scores[2])
        finalScore3 = self.__opponents[2].getFinalScore(self.__scores[3])
        finalScores.append(finalScorePlayer)
        finalScores.append(finalScore1)
        finalScores.append(finalScore2)
        finalScores.append(finalScore3)
        i = 0
        check = finalScores[i]
        while i < len(finalScores)-1:
            i+=1
            if finalScores[i] > check:
                check = finalScores[i]
                self.__winner = i

        return self.__winner

    # if returns true, it is currently the players turn, false = opponnents turn
    def currentTurn(self, override=None):
        if override is not None:
            self.__turnCounter -= 1
            return True
        ret = self.__turnCounter
        self.__turnCounter = (self.__turnCounter + 1) % 4
        return ret

    def getBoard(self):
        return self.__board

    def getPlayer(self):
        return self.__player

    def getOpponent(self, i : int):
        return self.__opponents[i]

    """
    Method to get current score of player or opponent, by color
    """
    def getScore(self, color: str):
        if color == "Green":
            scoreIndex = 0
        elif color == "Red":
            scoreIndex = 1
        elif color == "Blue":
            scoreIndex = 2
        elif color == "Yellow":
            scoreIndex = 3

        self.__scores[scoreIndex] = 0
        for r in range(self.__board.getRows()):
            for c in range(self.__board.getColumns()):
                if self.__board.getGrid()[r][c] != 0 and self.__board.getGrid()[r][c].getColor() == color:
                    self.__scores[scoreIndex] += 1
        return self.__scores[scoreIndex]

def inputMessage():
    print("w to move piece up")
    print("a to move piece left")
    print("s to move piece down")
    print("d to move piece right")

def main():
    from piece import Piece
    g = Game()
    print("welcome to Blokus!")
    gameOn = True
    repeat = False
    while gameOn:
        # display the board to user, as well as player and opponent scores
        print(g.getBoard().__str__())
        print("Player score: " + str(g.getScore("Green")))
        print("Red score: " + str(g.getScore("Red")))
        print("Blue score: " + str(g.getScore("Blue")))
        print("Yellow score: " + str(g.getScore("Yellow")))
        # if it is the players turn
        currentTurn = g.currentTurn()
        if currentTurn == 0:
            player = g.getPlayer()
            g.getPlayer().printPieces()
            stillSelect = True
            while stillSelect:
                playerInput = input("Select Number Piece to Play (you are GREEN):")
                playerInput = int(playerInput)
                while g.getPlayer().getPieces()[playerInput] == 0:
                    playerInput = input("Select Number Piece to Play (you are GREEN):")
                    playerInput = int(playerInput)
                    continue
                stillSelect = False
                row = None
                col = None
                player.selectPiece(playerInput)
                pieceToPlay = player.getSelectedPiece()
                outBounds = True
                while outBounds:
                    outBounds = False
                    row = int(input("Enter desired Row of CENTER TILE OF PIECE:"))
                    col = int(input("Enter desired Col of CENTER TILE OF PIECE:"))
                    if pieceToPlay.setRow(row) == False:
                        print("Piece out of bounds along the y-axis")
                        outBounds = True
                        continue
                    if pieceToPlay.setCol(col) == False:
                        print("Piece out of bounds along the x-axis")
                        outBounds = True
                        continue
                # check to see if place on board is already taken, place piece on board if not
                if g.getBoard().isValidSelection(pieceToPlay):
                    g.getBoard().updateGrid(pieceToPlay)
                else:
                    print("Place on board is already taken try again!")
                    g.getPlayer().getPieces()[playerInput] = pieceToPlay
                    stillSelect = True
        else:
            opponent = g.getOpponent(currentTurn - 1)
            opponent.setBoard(g.getBoard())
            pieceToPlay = opponent.choosePiece()
            if pieceToPlay == None:
                print("The " + opponent.getColor() + " player is out of moves")
            else:
                g.getBoard().updateGrid(pieceToPlay)
