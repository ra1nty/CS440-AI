import os
import sys
import pdb
import copy
import random

mazeWorld = [[0, -1, 0, 0, 0, 0],
             [0, 0, 0, -999, -1, 0],
             [0, 0, 0, -999, 0, 3],
             [0, 0, 0, -999, 0, 0],
             [0, 0, 0, 0, 0, 0],
             [1, -1, 0, -999, -1, -1]]

starting = (4, 1)


intended = 0.8
right = 0.1
left = 0.1
discount = 0.99

UP = 0
DOWN = 2
LEFT = 1
RIGHT = 3

lookup = dict()
lookup[UP] = "up"
lookup[DOWN] = "down"
lookup[LEFT] = "left"
lookup[RIGHT] = "right"


terminalMazeWorld = mazeWorld

def rewardFunc(y, x):
    if terminalMazeWorld[y][x] == 0:
        return -0.04
    elif terminalMazeWorld[y][x] == -999:
        return 0
    else:
        return terminalMazeWorld[y][x]

def policyIteration():
    actions = list()

    for i in range(len(terminalMazeWorld)):
        temp = list()
        for j in range(len(terminalMazeWorld[i])):
            if terminalMazeWorld[i][j] is -999 or terminalMazeWorld[i][j] is not -0.4:
                temp.append(random.randrange(0, 4))
            else:
                temp.append(-1)
        actions.append(temp)

    noChange = False
    values = list()
    values.append(copy.deepcopy(terminalMazeWorld))
    t = 1

    while noChange == False:
        noChange = True
        curr = copy.deepcopy(terminalMazeWorld)
        prev = values[t - 1]

        for i in range(len(terminalMazeWorld)):
            for j in range(len(terminalMazeWorld[i])):
                squares = getSurrounding(i, j, actions[i][j])
                total = 0.0

                for square in squares:
                    y = square[0]
                    x = square[1]
                    if y < len(mazeWorld) and y >= 0 and x < len(mazeWorld[0]) and x >= 0:
                        if not terminalMazeWorld[y][x] == -999:
                            total += square[2] * (prev[i][j])

                total *= discount
                total += rewardFunc(i, j)
                Qbest = total
                ais = getActions((i, j))

                for a in ais:
                    total = 0.0
                    for action in a:
                        y = action[0]
                        x = action[1]

                        if y < len(mazeWorld) and y >= 0 and x < len(mazeWorld[0]) and x >= 0:
                            if not terminalMazeWorld[y][x] == -999:
                                total += (action[2] * (prev[y][x]))

                    total *= discount
                    total += rewardFunc(i, j)

                    if total > Qbest:
                        if a[0][3] == actions[i][j]:
                            continue
                        actions[i][j] = a[0][3]
                        Qbest = total
                        noChange = False

                curr[i][j] = total

        for i in range(len(mazeWorld)):
            for j in range(len(mazeWorld[i])):
                print str(curr[i][j])[0:5] + "|",
            print ""
        for i in range(len(mazeWorld)):
            for j in range(len(mazeWorld[i])):
                move = actions[i][j]
                if mazeWorld[i][j] is not 0:
                    if mazeWorld[i][j] == -999:
                        print "W  |",
                    else:
                        print str(mazeWorld[i][j])[0:2].ljust(3) + "|",
                elif move == LEFT:
                    print "<- |",
                elif move == RIGHT:
                    print "-> |",
                elif move == UP:
                    print "^  |",
                else:
                    print "v  |",
            print ""

        pdb.set_trace()
        values.append(curr)

    print "\n\n"
    for i in range(len(mazeWorld)):
        for j in range(len(mazeWorld[i])):
            move = actions[i][j]
            if mazeWorld[i][j] is not 0:
                if mazeWorld[i][j] == -999:
                    print "W  |",
                else:
                    print str(mazeWorld[i][j])[0:2].ljust(3) + "|",
            elif move == LEFT:
                print "<- |",
            elif move == RIGHT:
                print "-> |",
            elif move == UP:
                print "^  |",
            else:
                print "v  |",
        print ""
    return actions

def getSurrounding(y, x, action):
    surroundings = list()

    if action == UP:
        surroundings = [(y - 1, x, intended), (y, x - 1, right), (y, x + 1, left)]
    elif action == DOWN:
        surroundings = [(y + 1, x, intended), (y, x - 1, right), (y, x + 1, left)]
    elif action == LEFT:
        surroundings = [(y, x - 1, intended), (y + 1, x, right), (y - 1, x, left)]
    else:
        surroundings = [(y, x + 1, intended), (y, x - 1, right), (y, x + 1, left)]

    return surroundings

def getActions(node):
    actions = list()
    x = node[1]
    y = node[0]

    actions.append([(y - 1, x, intended, UP), (y, x + 1, right), (y, x - 1, left)])
    actions.append([(y + 1, x, intended, DOWN), (y, x + 1, right), (y, x - 1, left)])
    actions.append([(y, x + 1, intended, RIGHT), (y - 1, x, right), (y + 1, x, left)])
    actions.append([(y, x - 1, intended, LEFT), (y - 1, x, right), (y + 1, x, left)])

    return actions
