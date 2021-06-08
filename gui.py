import pygame
import sys
from pygame.locals import *
from piece import Piece
from game import Game
from tile import Tile

REDRAW = pygame.USEREVENT + 1 #Triggered every 5 miiliseconds
SELECT_PIECE = REDRAW + 1 #Triggered on a click of a piece in the hand
PLAY_PIECE = SELECT_PIECE + 1 #Triggered on a click of a tile on the board
ROTATE_PIECE = SELECT_PIECE + 1 #Triggered on right click
FLIP_PIECE = ROTATE_PIECE + 1 #Triggered on a middle click
RIGHT_CLICK = 3
MIDDLE_CLICK = 2
BOARD_X_OFFSET = 60
BOARD_Y_OFFSET = 60
SCREEN_X = 750
SCREEN_Y = 850
TILE_SIZE = 30
#Initialization
game = Game()
player = game.getPlayer()
opponent1 = game.getOpponent(0)
opponent2 = game.getOpponent(1)
opponent3 = game.getOpponent(2)
pieces = player.getPieces()
player.setSelectedPiece(pieces[0])
board = game.getBoard()
selectedPieceScreenCoords = (TILE_SIZE// 2 + BOARD_X_OFFSET + 10 * TILE_SIZE, TILE_SIZE// 2 + BOARD_Y_OFFSET + 10 * TILE_SIZE)
selectedPieceScreenCoords = (400, 400)
selectedPiece = player.getSelectedPiece()
pygame.init()
screen = pygame.display.set_mode([SCREEN_X, SCREEN_Y])
pygame.display.set_caption('Blokus')
pieceIndex = 0
gameOver = False
def main():
    global game
    global pygame
    global player
    global board
    global selectedPiece
    global selectedPieceBoardCoords
    global selectedPieceScreenCoords
    global pieces
    global pieceIndex
    global gameOver

    turnCounter = 0
    currentTurn = 0
    gameIntro(screen)

    running = True
    while running:
        screen.fill((190, 190, 190))
        updateEverything()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == SELECT_PIECE:
                pass
            elif event.type == pygame.KEYDOWN:
                if event.key==K_LEFT:
                    if pieceIndex > 0:
                        selectedPiece = pieces[pieceIndex-1]
                        pieceIndex-=1

                elif event.key==K_RIGHT:
                    if pieceIndex < len(pieces)-1:
                        selectedPiece = pieces[pieceIndex+1]
                        pieceIndex+=1

            elif event.type == PLAY_PIECE:
                pass
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT_CLICK:
                selectedPiece.rotate()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == MIDDLE_CLICK:
               selectedPiece.flip()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Left Click
                if event.button == 1 and board.isValidSelection(selectedPiece):
                    screenX = event.pos[0]
                    screenY = event.pos[1]
                    if screenX < BOARD_X_OFFSET or screenX >= BOARD_X_OFFSET + TILE_SIZE * 20 or screenY < BOARD_Y_OFFSET or screenY >= BOARD_Y_OFFSET + TILE_SIZE * 20:
                        break
                    if selectedPiece in pieces:
                        pieces.remove(selectedPiece)
                    if not player.getPlayedLastPiece():
                        board.updateGrid(selectedPiece)
                    if len(player.getPieces()) == 0:
                        player.setPlayedLastPiece(True)
                        selectedPiece = Piece.decoy(Piece, player.getColor())
                        gameOver = True
                    else:
                        selectedPiece = pieces[0]
                    pieceIndex = 0
                    turnCounter+=1
                    currentTurn = turnCounter%4
                    if player.outOfMoves():
                        player.setPlayedLastPiece(True)

                if (player.getPlayedLastPiece() == True):
                        turnCounter+=1

                elif event.button == 2: #Middle Click
                    pass
                elif event.button == 3: #Right click
                    pass

            #Check for location and determine appropriate action, ie play, select, or nothing
            elif event.type == pygame.MOUSEMOTION:
                screenX = event.pos[0]
                screenY = event.pos[1]
                if screenX < BOARD_X_OFFSET or screenX >= BOARD_X_OFFSET + TILE_SIZE * 20 or screenY < BOARD_Y_OFFSET or screenY >= BOARD_Y_OFFSET + TILE_SIZE * 20:
                    break
                boardCoords = screenCoordsToBoardCoords(screenX, screenY)
                if not selectedPiece.setCol(boardCoords[0]):
                    boardCoords = (selectedPieceBoardCoords[0], boardCoords[1])
                if not selectedPiece.setRow(boardCoords[1]):
                    boardCoords = (boardCoords[0], selectedPieceBoardCoords[1])
                if boardCoords != (-1, -1):
                    selectedPieceBoardCoords = boardCoords
                selectedPieceScreenCoords = boardCoordsToScreenCoords(selectedPieceBoardCoords[0], selectedPieceBoardCoords[1])
                selectedPiece.setCol(selectedPieceBoardCoords[0])
                selectedPiece.setRow(selectedPieceBoardCoords[1])

            if currentTurn != 0:
                # ADD DELAY
                opponent = game.getOpponent(currentTurn - 1)
                opponent.setBoard(game.getBoard())
                pieceToPlay = None
                if not opponent.getPlayedLastPiece():
                    pieceToPlay = opponent.choosePiece()
                if pieceToPlay == None:
                    opponent.setPlayedLastPiece(True)
                    turnCounter += 1
                    currentTurn = turnCounter % 4
                else:
                    game.getBoard().updateGrid(pieceToPlay)
                    turnCounter+=1
                    currentTurn = turnCounter%4

        pygame.display.flip()
    pygame.quit()
def updateEverything():

    #Draw everything again
    drawBoard()

    #Drawing the hovering piece
    tileList = drawPiece(selectedPieceScreenCoords[0], selectedPieceScreenCoords[1], selectedPiece, TILE_SIZE)
    for tile in tileList:
        screen.blit(tile[0], tile[1])
    #Drawing Player Pieces
    tileList = drawPiecesSelection(SCREEN_X//2, SCREEN_Y - BOARD_Y_OFFSET - BOARD_Y_OFFSET//2, player.getPieces())
    for tile in tileList:
        screen.blit(tile[0], tile[1])

def drawBoard():
    #Draw the board
    grid = board.getGrid()
    rows = board.getRows()
    cols = board.getColumns()
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 0:
                if (c%2 == 0 and r%2 == 0) or (c%2 != 0 and r%2 != 0):
                    pygame.draw.rect(screen, (220,220,220), (BOARD_X_OFFSET+TILE_SIZE*c, BOARD_Y_OFFSET+TILE_SIZE*r, TILE_SIZE, TILE_SIZE))
                else:
                    pygame.draw.rect(screen, (255, 255, 255), (BOARD_X_OFFSET+TILE_SIZE*c, BOARD_Y_OFFSET+TILE_SIZE*r, TILE_SIZE, TILE_SIZE))
            # If there's a tile in the space then we need to get the color (part of a piece)
            if grid[r][c] != 0:
                if grid[r][c].getColor() == "Green":
                    pygame.draw.rect(screen, (0, 255, 0), (BOARD_X_OFFSET+TILE_SIZE*c, BOARD_Y_OFFSET+TILE_SIZE*r, TILE_SIZE, TILE_SIZE))
                elif grid[r][c].getColor() == "Blue":
                    pygame.draw.rect(screen, (0, 0, 255), (BOARD_X_OFFSET+TILE_SIZE*c, BOARD_Y_OFFSET+TILE_SIZE*r, TILE_SIZE, TILE_SIZE))
                elif grid[r][c].getColor() == "Yellow":
                    pygame.draw.rect(screen, (255, 255, 0), (BOARD_X_OFFSET+TILE_SIZE*c, BOARD_Y_OFFSET+TILE_SIZE*r, TILE_SIZE, TILE_SIZE))
                elif grid[r][c].getColor() == "Red":
                    pygame.draw.rect(screen, (255, 0, 0), (BOARD_X_OFFSET+TILE_SIZE*c, BOARD_Y_OFFSET+TILE_SIZE*r, TILE_SIZE, TILE_SIZE))
    for r in range(rows+1):
        for c in range(cols+1):
            pygame.draw.line(screen, (0, 0, 0), (BOARD_X_OFFSET+TILE_SIZE*c, BOARD_Y_OFFSET+TILE_SIZE*r), (BOARD_X_OFFSET+TILE_SIZE*c, 2*BOARD_Y_OFFSET+TILE_SIZE ))
            pygame.draw.line(screen, (0, 0, 0), (BOARD_X_OFFSET, BOARD_Y_OFFSET+TILE_SIZE*r), (BOARD_Y_OFFSET +TILE_SIZE*20, BOARD_X_OFFSET+TILE_SIZE*r))

    # Display player and opponent scores at respective board corners
    myfont = pygame.font.SysFont('Boulder', 20)
    playerScore = game.getScore(player.getColor())
    oppOneScore = game.getScore(opponent1.getColor())
    oppTwoScore = game.getScore(opponent2.getColor())
    oppThreeScore = game.getScore(opponent3.getColor())

    if player.getPlayedLastPiece() == True:
        displayText = "Final Score (you): " + str(player.getFinalScore(playerScore))
        textPlayer = myfont.render(displayText, False, (0, 0, 0))
        screen.blit(textPlayer, (10, SCREEN_Y-185))
    else:
        displayText = "Green Score (you): " + str(playerScore)
        textPlayer = myfont.render(displayText, False, (0, 0, 0))
        screen.blit(textPlayer, (10, SCREEN_Y-185))

    if opponent1.getPlayedLastPiece() == True:
        displayText = "Final Score: " + str(opponent1.getFinalScore(oppOneScore))
        textPlayer = myfont.render(displayText, False, (0, 0, 0))
        screen.blit(textPlayer, (10, SCREEN_Y-810))
    else:
        displayText = "Red Score: " + str(oppOneScore)
        textPlayer = myfont.render(displayText, False, (0, 0, 0))
        screen.blit(textPlayer, (10, SCREEN_Y-810))

    if opponent2.getPlayedLastPiece() == True:
        displayText = "Final Score: " + str(opponent2.getFinalScore(oppTwoScore))
        textPlayer = myfont.render(displayText, False, (0, 0, 0))
        screen.blit(textPlayer, (SCREEN_X-140, SCREEN_Y-810))
    else:
        displayText = "Blue Score: " + str(oppTwoScore)
        textPlayer = myfont.render(displayText, False, (0, 0, 0))
        screen.blit(textPlayer, (SCREEN_X-140, SCREEN_Y-810))

    if opponent3.getPlayedLastPiece() == True:
        displayText = "Final Score: " + str(opponent3.getFinalScore(oppThreeScore))
        textPlayer = myfont.render(displayText, False, (0, 0, 0))
        screen.blit(textPlayer, (SCREEN_X-140, SCREEN_Y-185))
    else:
        displayText = "Yellow Score: " + str(oppThreeScore)
        textPlayer = myfont.render(displayText, False, (0, 0, 0))
        screen.blit(textPlayer, (SCREEN_X-140, SCREEN_Y-185))

    # Game Over

    if player.getPlayedLastPiece() == True and opponent1.getPlayedLastPiece() == True and opponent2.getPlayedLastPiece() == True and opponent3.getPlayedLastPiece() == True:
        gameOver = True
        winnerID = game.getWinner()
        if winnerID == 0:
            winner = "You are"
        elif winnerID == 1:
            winner = "Red is"
        elif winnerID == 2:
            winner = "Blue is"
        elif winnerID == 3:
            winner = "Yellow is"

        displayText = "Game Over! " + winner + " the winner!"
        textPlayer = myfont.render(displayText, False, (0, 0, 0))
        screen.blit(textPlayer, (290, SCREEN_Y-810))


def drawCoords():
    #Draw the coords of the selected piece
    pass
def drawPiece(x : int, y : int, piece, tileSize):
    #Draw the Piece with the x and y at the center of the center tile
    tiles = piece.getTiles()
    center = piece.getCenter()
    out = []
    for tile in tiles:
        out.append(drawTile(x+tileSize*(tile.getCol()-center.getCol()), y+tileSize*(tile.getRow()-center.getRow()), tile.getColor(), tileSize))
    return out
def drawTile(x : int, y : int, color : str, tileSize):
    tile = pygame.Surface((tileSize, tileSize))
    if color == "Red" :
        tile.fill((255, 0,0))
    elif color == "Green":
        # if the player played their last piece, make
        # the dummy piece transparent
        if player.getPlayedLastPiece():
            tile.set_alpha(0)
        tile.fill((0,255,0))
    elif color == "Yellow":
        tile.fill((255, 211, 0))
    elif color == "Blue":
        tile.fill((0, 0, 255))
    #Draw the tile with the x and y at the center of the tile
    return (tile, (x-tileSize//2, y-tileSize//2))
def drawPoints():
    #Draw the points
    pass
def drawPiecesSelection(x : int, y : int, pieces):
    #Draw all pieces available for player and opponents
    # x and y should be the center of the center tile of the middle of the list
    #[(surf, x, y)]
    out = []
    top = pieces[:len(pieces)//2]
    bottom = pieces[len(pieces)//2:]
    for yOffset in (-40, 50):
        if yOffset == -40:
            l = top
        else:
            l = bottom
        left = len(l) // 2
        leftX = x
        right = len(l) // 2 + 1
        rightX = x
        if (len(l) > 0):
            out.extend(drawPiece(x, y + yOffset, l[left], TILE_SIZE//2))
            left -= 1
            while left >= 0 or right < len(l):
                if left >= 0:
                    #Determining how much space the piece to the left took
                    toRight = l[left + 1]
                    leftmost = toRight.getTiles()[0]
                    for tile in toRight.getTiles():
                        if tile.getCol() < leftmost.getCol():
                            leftmost = tile
                    #Determing how much space this piece will take
                    rightmost = l[left].getTiles()[0]
                    for tile in l[left].getTiles():
                        if tile.getCol() > rightmost.getCol():
                            rightmost = tile
                    leftX = leftX - TILE_SIZE - (TILE_SIZE//2)*(toRight.getCenter().getCol() - leftmost.getCol())
                    leftX = leftX - (TILE_SIZE//2)*(rightmost.getCol() - l[left].getCenter().getCol())
                    out.extend(drawPiece(leftX, y + yOffset, l[left], TILE_SIZE//2))
                    left -= 1
                if right < len(l):
                    toLeft = l[right - 1]
                    rightmost = toLeft.getTiles()[0]
                    for tile in toLeft.getTiles():
                        if tile.getCol() > rightmost.getCol():
                            rightmost = tile
                    # Determing how much space this piece will take
                    leftmost = l[right].getTiles()[0]
                    for tile in l[right].getTiles():
                        if tile.getCol() < leftmost.getCol():
                            leftmost = tile
                    rightX = rightX + TILE_SIZE + (TILE_SIZE // 2) * (rightmost.getCol() - toLeft.getCenter().getCol())
                    rightX = rightX + (TILE_SIZE//2)*(l[right].getCenter().getCol() - leftmost.getCol())
                    out.extend(drawPiece(rightX, y + yOffset, l[right], TILE_SIZE//2))
                    right += 1
        else:
            return []
    return out
def playPiece():
    #Plays a piece
    pass
def rotatePiece():
    #Rotates a piece
    pass
def flipPiece():
    #Flips a piece
    pass
def screenCoordsToBoardCoords(x : int, y : int):
    #Translates the screen coordinates of the mouse to a cooardinate location on the board
    #returns a list [x, y]
    if x < BOARD_X_OFFSET or y < BOARD_Y_OFFSET or x > TILE_SIZE*20+BOARD_X_OFFSET or y > TILE_SIZE*20+BOARD_Y_OFFSET:
        return (-1, -1)
    else:
        return ((x-BOARD_X_OFFSET)//TILE_SIZE,  (y-BOARD_Y_OFFSET)//TILE_SIZE)
def boardCoordsToScreenCoords(x : int, y : int):
    #Translates the coordinates of the board to coordinates on the screen
    #returns a list [x, y]
    if x < 0 or y < 0 or x >= 20 or y >= 20:
        return (0, 0)
    else:
        return (x*TILE_SIZE+BOARD_X_OFFSET+15, y*TILE_SIZE+BOARD_X_OFFSET+15)

def gameIntro(screen):
    # white color
    color = (255, 255, 255)
    # light shade of the button
    color_light = (170, 170, 170)
    # dark shade of the button
    color_dark = (100, 100, 100)
    # stores the width of the
    # screen into a variable
    width = screen.get_width()
    # stores the height of the
    # screen into a variable
    height = screen.get_height()
    # defining a font
    smallfont = pygame.font.SysFont('Corbel', 35)
    largeFont = pygame.font.SysFont('Arial', 45)
    # rendering a text written in
    # this font
    textQuit = smallfont.render('Quit', True, color)
    textStart = smallfont.render("Start", True, color)
    # image
    logo = pygame.image.load('blokus.png')
    # buttons
    quitButton = [width / 3.5 + 55, height / 2, 140, 40]
    startButton = [width / 3.5 + 55, height / 2 + 60, 140, 40]
    BUTTONWIDTH = width / 3.5
    run = True
    while run:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                # checks if a mouse is clicked
            if ev.type == pygame.MOUSEBUTTONDOWN:
                # if the mouse is clicked on the
                # button the game is terminated
                if width / 3.5 + 55 <= mouse[0] <= width / 2 + 200 and height / 2 + 60 <= mouse[1] <= height / 2 + 100:
                    pygame.quit()
                    sys.exit()
                if width / 3 <= mouse[0] <= width / 2 + 140 and height / 2 <= mouse[1] <= height / 2 + 40:
                    run = False
                # fills the screen with a color
        screen.fill((60, 25, 60))
        # stores the (x,y) coordinates into
        # the variable as a tuple
        mouse = pygame.mouse.get_pos()
        # if mouse is hovered on a button it
        # changes to lighter shade
        if width / 3 <= mouse[0] <= width / 2 + 140 and height / 2 <= mouse[1] <= height / 2 + 40:
            pygame.draw.rect(screen, color_light, quitButton)
        else:
            pygame.draw.rect(screen, color_dark, quitButton)
        if width / 3.5 + 55 <= mouse[0] <= width / 2 + 200 and height / 2 + 60 <= mouse[1] <= height / 2 + 100:
            pygame.draw.rect(screen, color_light, startButton)
        else:
            pygame.draw.rect(screen, color_dark, startButton)
            # superimposing the text onto our button
        screen.blit(logo, (width / 3.5, height / 4))
        screen.blit(textStart, (BUTTONWIDTH + 65, height / 2 + 3))
        screen.blit(textQuit, (BUTTONWIDTH + 65, height / 2 + 63))
        # .blit(test2, (width / 2 - 50, height / 4))
        # updates the frames of the game
        pygame.display.update()
main()
