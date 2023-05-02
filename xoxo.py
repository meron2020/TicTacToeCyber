import pygame
import time

display_width = 510
display_height = 660

# create the screen - the size of the background image
screen = pygame.display.set_mode((display_width, display_height))

# Title and Icon
pygame.display.set_caption("Tic-tac-toe")
icon = pygame.image.load('sunflower.png')
pygame.display.set_icon(icon)

# x and o and replay and background and score cover pictures
xPic = pygame.image.load('x.png')
oPic = pygame.image.load('o.png')
replayPic = pygame.image.load('replay.png')
img = pygame.image.load('background.png')
scoreCover = pygame.image.load('scoreCover.png')

# list of the places -what they contain: 0=empty, 1=x, 2=o
# spots = [1,2,3,4,5,6,7,8,9] <= the spots order in the list
spots = [0, 0, 0, 0, 0, 0, 0, 0, 0]

# 3d list of coordinates: arr[i][k][j] => i=0(top left) i=1(bottom right), k=row, j=column
coordinates = [
    [[(0, 165), (171, 165), (342, 165)], [(0, 330), (171, 330), (342, 330)], [(0, 497), (171, 497), (342, 497)]],
    [[(168, 327), (338, 327), (510, 327)], [(168, 493), (338, 493), (510, 493)], [(168, 660), (338, 660), (510, 660)]]]

# will be displayed as the score
xWins = 0
oWins = 0

# will help dettermen hwo gets to go first each round
goFirst = 0

# gameOver will be used to stop further actions once a player has won
gameOver = False
# count will be used to check whose turn it is
count = 0


def text_objects(text, font):
    textSurface = font.render(text, True, (139, 0, 0))
    return textSurface, textSurface.get_rect()


def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf', 30)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width / 2), (display_height / 5))
    screen.blit(TextSurf, TextRect)

    pygame.display.update()

# displays the score at the top left corner
def displayScore():
    global xWins
    global oWins
    largeText = pygame.font.Font('freesansbold.ttf', 20)
    text = "X: " + str(xWins) + "   O: " + str(oWins)
    TextSurf, TextRect = text_objects(text , largeText)
    #TextRect.center = (0, 0)
    screen.blit(TextSurf, TextRect)


# returns whether there is a winner in a given row(1/2/3).
def checkRow(row):
    if spots[row * 3 - 1] == spots[row * 3 - 2] == spots[row * 3 - 3] and spots[row * 3 - 1] != 0:
        # returns 1 (x) or 2 (o) depending on who won or 0 if there is no winner
        return spots[row * 3 - 1]
    return 0


# returns the num of the winner (1 for x and 2 for o) in a given column(1/2/3).
def checkColumn(column):
    if spots[column - 1] == spots[column + 2] == spots[column + 5] and spots[column - 1] != 0:
        # returns 1 (x) or 2 (o) depending on who won or 0 if there is no winner
        return spots[column - 1]
    return 0


# returns the num of the winner (1 for X and 2 for O or 0 if there is no winner) in the diagonal given
# - the diagonal that starts at the top left is 1 and the other is 2
def checkDiagonal(num):
    if num == 1:
        if spots[0] == spots[4] == spots[8] and spots[0] != 0:
            return spots[0]
        return 0
    if num == 2:
        if spots[2] == spots[4] == spots[6] and spots[2] != 0:
            return spots[2]
        return 0

# puts x or o image in given coordinates
def placePhoto(photo, position):
    screen.blit(photo, position)
    pygame.display.update()


# receives the number of the winners simbol: 1 (X) or 2 (O) and pops message of the win
def winnerMessage(num):
    global xWins
    global oWins
    if num == 1:
        message_display("CONGRATS! X WON!!!")
        xWins += 1
        placePhoto(scoreCover, (0, 0))
        displayScore()
    if num == 2:
        message_display("CONGRATS! O WON!!!")
        oWins += 1
        placePhoto(scoreCover, (0, 0))
        displayScore()
    # tie:
    if num == 3:
        message_display("ITS A TIE!")


#  returns the num of the winner ( 1 for X and 2 for O and 0 if there is no winner)
def checkWin():
    global goFirst
    # checks the rows and prints winner message if there is a winner and returns true if it found a winner
    if checkRow(1) != 0:
        winnerMessage(checkRow(1))
        goFirst += 1
        return True
    if checkRow(2) != 0:
        winnerMessage(checkRow(2))
        goFirst += 1
        return True
    if checkRow(3) != 0:
        winnerMessage(checkRow(3))
        goFirst += 1
        return True

    # checks the columns and prints winner message if there is a winner
    if checkColumn(1) != 0:
        winnerMessage(checkColumn(1))
        goFirst += 1
        return True
    if checkColumn(2) != 0:
        winnerMessage(checkColumn(2))
        goFirst += 1
        return True
    if checkColumn(3) != 0:
        winnerMessage(checkColumn(3))
        goFirst += 1
        return True

    # checks the diagonals and prints winner message if there is a winner
    if checkDiagonal(1) != 0:
        winnerMessage(checkDiagonal(1))
        goFirst += 1
        return True
    if checkDiagonal(2) != 0:
        winnerMessage(checkDiagonal(2))
        goFirst += 1
        return True

    # if tied
    notTied = False
    for i in spots:
        if i == 0:
            notTied = True
    if notTied == False:  # if there is a tie
        winnerMessage(3)
        goFirst += 1
        return True
    return False



def gameReset():
    #   resetting spots to empty
    i = 0
    while i < 9:
        spots.pop()
        i = i + 1
    while i > 0:
        spots.append(0)
        i = i - 1
    # resetting gameOver to False
    global count
    global gameOver
    gameOver = False
    # resetting count to goFirst so the person who went first last game will go second this time
    count = goFirst
    # Background image
    screen.blit(img, (0, 0))
    pygame.display.update()

    # placing replay image
    placePhoto(replayPic, (display_width - 50, 0))


# converts mouse position into spotNum for function playGame
def getSpotNum():
    x, y = pygame.mouse.get_pos()
    if 0 <= x <= 168 and 165 <= y <= 327:
        return 1
    if 171 <= x <= 338 and 165 <= y <= 327:
        return 2
    if 342 <= x <= 510 and 165 <= y <= 327:
        return 3
    if 0 <= x <= 168 and 330 <= y <= 493:
        return 4
    if 171 <= x <= 338 and 330 <= y <= 493:
        return 5
    if 342 <= x <= 510 and 330 <= y <= 493:
        return 6
    if 0 <= x <= 168 and 497 <= y <= 660:
        return 7
    if 171 <= x <= 338 and 497 <= y <= 660:
        return 8
    if 342 <= x <= 510 and 497 <= y <= 660:
        return 9
    # replay image
    if 460 <= x <= 510 and 0 <= y <= 50:
        return 10
    # if mouse is clicked on unused area
    return -1


# places the image in the right place and marks the spot taken in emptySpot array
def playGame(spotNum, count):
    if 1 <= spotNum <= 3:
        row = 0
        column = spotNum - 1
    if 4 <= spotNum <= 6:
        row = 1
        column = spotNum - 4
    if 7 <= spotNum <= 9:
        row = 2
        column = spotNum - 7

    if spotNum != -1 and spotNum != 10:  # if mouse is clicked on on of the spots
        # checking x,y separately
        x, y = pygame.mouse.get_pos()
        if (coordinates[0][row][column][0] <= x <= coordinates[1][row][column][0] and
            coordinates[0][row][column][1] <= y <= coordinates[1][row][column][1]) \
                and (spots[spotNum - 1] == 0):
            if count % 2 == 0:
                placePhoto(xPic, coordinates[0][row][column])
                spots[spotNum - 1] = 1
            else:
                placePhoto(oPic, coordinates[0][row][column])
                spots[spotNum - 1] = 2
            return True
        return False


# initialize the pygame
pygame.init()

# RGB - Red, Green, Blue
#    screen.fill((0,128,128))
# Background image
screen.blit(img, (0, 0))
pygame.display.update()

# placing replay image
placePhoto(replayPic, (display_width - 50, 0))

# Game Loop
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if mouse is clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            # if replay image is clicked
            if getSpotNum() == 10:
                gameReset()
                print(spots)  # testing
            if not gameOver:
                help = getSpotNum()
                if playGame(help, count):
                    count = count + 1
                gameOver = checkWin()

    pygame.display.flip()

# board squares positions:
# [0,0]: (0,165) => (168,327)    [0,1]: (171,165) => (338,327)   [0,2]: (342,165) => (510,327)
# [1,0]: (0,330) => (168,493)    [1,1]: (171,330) => (338,493)   [1,2]: (342,330) => (510,493)
# [2,0]: (0,497) => (168,660)    [2,1]: (171,497) => (338,660)   [2,2]: (342,497) => (510,660)
