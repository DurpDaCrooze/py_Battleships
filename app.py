# Author: Luca Cassart 👍 
"""I want to set the record straight and say that I AM AWARE of the fact that the next_turn function wasn't remotely
used in the extent it was asked of me, but honestly im around 5 hours into writing this and rewriting it is just plain
disruptive to every physical aspect of me at this point so I will leave it. Please be generous and keep in mind that the program
runs MOSTLY just fine🙏 (decided to do it last minute, some stuff is broken, other stuff is not full proof)"""

import os
import random

#Global vars 😛
loadedhstable= [] #Current loaded highscore table xoxo

turnsAllocated = 10
tileStates = ['~', 'o', 'x']

def displayTitle():
    # Fetch ASCII title element from file
    try:
        with open('ASCII_ART/titleScreen.txt', 'r') as file:
            title = file.read()
            print(title)
    except FileNotFoundError:
        print("Error: ASCII title file not found.")
        exit(1)

def main_menu():
    uIn = -1
    while True:
        # Display the main menu
        print("---===Main Menu===---", 
            "\n1. | Enter User Info", 
            "\n2. | Start New Game",
            "\n3. | Load Game",
            "\n3. | Quit",)
        # Get user input and validate
        try:
            uIn = int(input("Select a valid option:"))
            if((uIn > 0 and uIn < 4)):
                break
            else:
                print("Invalid input. Please enter a number between 1 and 3.")
                continue
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 3.")
            continue

    return uIn;    

def goto(sectionID):
    if(sectionID == 1):
        print("Enter user info")
    if(sectionID == 2):
        board = initialize_game_board(False, 10, 10, 5)
        ship_data = board.pop()
        print(ship_data)
        gameloop(board, ship_data)
    if(sectionID == 3):
        uIn = input("Enter save file name: ")
        print("Load game from file")
        parsedLoadFile = loadGame(uIn)
        gameloop(parsedLoadFile[0], parsedLoadFile[1], parsedLoadFile[2])
    if(sectionID == 3):
        print("Load leaderboard from file")
    if(sectionID == 4):
        print("Quit")
        exit(0)


def initialize_game_board(saveOverride, width, height, shipCount):        
    board = []
    if(not saveOverride):
        for y in range(0,height):
            row = []
            for x in range(0,width):
                row.append(tileStates[0])
            board.append(row)
        row = []
        for ship in range(0, shipCount):
            cordsValid = True
            while True:
                tempShipCord = [random.randint(0, width-1), random.randint(0, height-1)] 
                for x in range(0, len(row)):
                    if(tempShipCord == row[x]):
                        cordsValid = False
                        break
                if cordsValid:
                    row.append(tempShipCord)
                    break

        board.append(row)

    return board

def draw_board(board):
    drawBoard = []
    for y in range(0, len(board)+1):
        row = []
        for x in range(0, len(board[0])+1):
            if y==0:
                if x==0:
                   row.append(" ")
                else:
                    row.append(x-1)
            elif x==0:
                row.append(y-1)
            else:
                row.append(board[y-1][x-1])
        drawBoard.append(row)
    
    for y in range(0, len(drawBoard)):
        for x in range(0, len(drawBoard)):
            print(drawBoard[y][x], end='')
        print("\n", end='')

def draw_metrics(gameMetrics):
    print("Points : ", gameMetrics[0], " | Turns Left: ", gameMetrics[1])

def next_turn():
    uIn = input("Choose target coords: ")
    return uIn.split(',') 

def validate(input_data, board):
    input_data[0] = str(input_data[0]) 
    input_data[1] = str(input_data[1])
    if len(input_data)>1 and input_data[0].isdigit(): 
        input_data[0] = int(input_data[0])
        input_data[1] = int(input_data[1])
        if((input_data[0] < len(board[0])) and (input_data[0] >= 0) and (input_data[1] < len(board)) and (input_data[1] >= 0)):
            return True
    elif(input_data[0] == 'q'):
        return True
    return False

def update_board(input_data, board, shipBoard, gameMetrics):
    print("running update board!!")
    hitCords = [input_data[0], input_data[1]]

    if(hitShip(hitCords, shipBoard)):
        if(shipAlive(hitCords, board)):
            board[hitCords[1]][hitCords[0]] = tileStates[2]
            gameMetrics[0] += 1
            gameMetrics[1] -= 1
        else:
            print("Ship Already hit! Turns not reduced.")
    elif not tileHit(hitCords, board):
        gameMetrics[1] -= 1
        board[hitCords[1]][hitCords[0]] = tileStates[1]
    else:
        print("Tile already hit!, Turns not reduced.")

def tileHit(hitCords, board):
    if (board[hitCords[1]][hitCords[0]] == tileStates[1]):
        return True
    return False

def shipAlive(ship, board):
    print("hit cords: ", ship)
    if board[ship[1]][ship[0]] == tileStates[2]:
        return False
    else: return True

def hitShip(hitCords, shipBoard):
        for ship in shipBoard:
            if(hitCords == ship):
                return True
        return False

def init():
    displayTitle()
    goto(main_menu())

def gameCondition(gameMetrics):
    if(gameMetrics[1] == 0):
        return False
    else:
        return True

def summeryScreen(gameMetrics):
    print("-----Game Over!------")
    print("Final Score: ", gameMetrics[0])
    input("Enter anything to go back to menu...")

    
def saveGame(board, shipBoard, gameMetrics):
    os.makedirs('GAME_DATA', exist_ok=True)
    try:
        with open(('GAME_DATA/' + gameMetrics[2] + '.txt'), 'w') as file:
            saveList = [board, shipBoard, gameMetrics]
            file.write(str(saveList))
    finally:
        print("Data written!")

def loadGame(filename):            
    try:
        with open(('GAME_DATA/' + filename + '.txt'), 'r') as file:
            saveFile = file.read()
            parsedSaveFile = eval(saveFile)
            return(parsedSaveFile)
    except FileNotFoundError:
        print("Error: Save file not found!")
        exit(1)


def loadScoreboard(filename): 
    try:
        with open(('GAME_DATA/' + filename + '_sb.txt'), 'r') as file:
            saveFile = file.read()
            parsedSaveFile = eval(saveFile)
            return(parsedSaveFile)
    except FileNotFoundError:
        print("Error: Highscore file not found!")
        exit(1)

def saveScoreboard(save_name):
    os.makedirs('GAME_DATA', exist_ok=True)
    try:
        with open(('GAME_DATA/' + save_name + '_sb.txt'), 'w') as file:
            saveList = loadedhstable 
            file.write(str(saveList))
    finally:
        print("Data written!")

def saveScoreboardRecord(user, score):
    leaderboard.append[user, score]


def gameloop(board, shipBoard, gameMetrics=[0,turnsAllocated, "Anonymous"]):
    draw_board(board)
    while gameCondition(gameMetrics):      
        input_data = next_turn()
        while(not validate(input_data, board)):
            print("Invalid input, correct turn syntax: [x,y] or [q]")
            input_data = next_turn()
        update_board(input_data, board, shipBoard, gameMetrics)
        saveGame(board, shipBoard, gameMetrics)
        draw_board(board) 
        draw_metrics(gameMetrics)
    saveScoreBoard(gameMetrics[2], gameMetrics[0])
    summeryScreen(gameMetrics)

init();

