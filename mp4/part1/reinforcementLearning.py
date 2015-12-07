import os
import sys
import copy
import random
import numpy as np
import matplotlib.pyplot as plt
from gridWorld import *
from math import sqrt

QLookup = dict()

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
LEFT = 1
DOWN = 2
RIGHT = 3

INT_MIN = -99999
stateLookup = dict()
stateLookup[UP] = "up"
stateLookup[DOWN] = "down"
stateLookup[LEFT] = "left"
stateLookup[RIGHT] = "right"

def state(x, y):
    return y * len(mazeWorld) + x

def learningRate(time):
    return 60/(59.0 + time)

def reward(x, y):
    if mazeWorld[y][x] == 0:
        return -0.4
    elif mazeWorld[y][x] == -999:
        return 0
    else:
        return mazeWorld[y][x]

def exploration(q, n):
    if n > 100:
        return random.random()
    return q

def tupleFromState(s):
    return (s/len(mazeWorld), s % len(mazeWorld))

def initializeQLookup():
    for i in range(len(mazeWorld)):
        for j in range(len(mazeWorld[i])):
            for k in range(4):
                if not mazeWorld[i][j] == -999:
                    QLookup[(state(j, i), k)] = 0.0

def initializeMoveSet(moves):
    for i in range(len(mazeWorld)):
        for j in range(len(mazeWorld[i])):
            for k in range(4):
                if not mazeWorld[i][j] == -999:
                    moves[(state(j, i), k)] = 0.0

def initializeMoveCount(moves):
    for i in range(len(mazeWorld)):
        for j in range(len(mazeWorld[i])):
            for k in range(4):
                if not mazeWorld[i][j] == -999:
                    moves[(state(j, i), k)] = 0

def performAction(s, action):
    x = s[1]
    y = s[0]

    if action == UP:
        y -= 1
    elif action == DOWN:
        y += 1
    elif action == LEFT:
        x -= 1
    else:
        x += 1

    # Clamp values in mazeworld
    if (y < len(mazeWorld) and y >= 0 and x < len(mazeWorld[0]) and x >= 0):
        if mazeWorld[y][x] == -999:
        # if it's a wall reset it to the initial move
            x = s[1]
            y = s[0]
    else:
        x = s[1]
        y = s[0]


    # Return the state
    return state(x, y)

def checkEnd(s):
    x = s[1]
    y = s[0]
    if not mazeWorld[y][x] == -999 and not mazeWorld[y][x] == 0:
        return 1
    return 0

def rootmeansquare(valueIter, reinforcement, time):
    tempVal = 0.0
    a = 0
    tempMax = INT_MIN

    for i in range(len(mazeWorld)):
        for j in range(len(mazeWorld[i])):
            if mazeWorld[i][j] == 0:
                for action in range(4):
                    temp = reinforcement[(state(j, i), action)]
                    if temp > tempMax:
                        tempMax = temp
                        a = action

                if mazeWorld[i][j] == 0:
                    tempVal += pow((reinforcement[(state(j, i), a)] - valueIter[i][j]), 2)

    tempVal *= 0.5
    tempVal = sqrt(tempVal)
    return tempVal

def reinforcementLearning(val):
    moveSet = dict()
    moveCount = dict()
    initializeMoveSet(moveSet)
    initializeMoveCount(moveCount)
    initializeQLookup()

    currState = starting
    iteration = 0
    rmse = list()
    maxRMSE = INT_MIN

    # s - number
    # action - number
    # nextstate - tuple
    # maxAction - number
    # time - number

    episodes = 0
    maxE = 10000

    while episodes < maxE:
        maxCurrAction = 0
        maxVal = INT_MIN

        # Find the max action at current state
        for action in range(4):
            # tempNextState = performAction(currState, action)
            tempVal = exploration(QLookup[(state(currState[1], currState[0]), action)], moveCount[(state(currState[1], currState[0]), action)])
            if tempVal > maxVal:
                maxVal = tempVal
                maxCurrAction = action

        maxNextAction = 0
        maxVal = INT_MIN
        tempRand = random.random()

        if tempRand <= 0.8:
            maxCurrAction = maxCurrAction
        elif tempRand <= 0.9:
            if maxCurrAction == UP:
                maxCurrAction = LEFT
            elif maxCurrAction == RIGHT:
                maxCurrAction = UP
            elif maxCurrAction == LEFT:
                maxCurrAction = DOWN
            else:
                maxCurrAction = RIGHT
        else:
            if maxCurrAction == UP:
                maxCurrAction = RIGHT
            elif maxCurrAction == RIGHT:
                maxCurrAction = DOWN
            elif maxCurrAction == LEFT:
                maxCurrAction = UP
            else:
                maxCurrAction = LEFT

        maxNextState = tupleFromState(performAction(currState, maxCurrAction))

        if not maxNextState == currState:
            for action in range(4):
                # tempNextState = performAction(maxNextState, action)
                tempVal = QLookup[(state(maxNextState[1], maxNextState[0]), action)]
                if tempVal > maxVal:
                    maxVal = tempVal
                    maxNextAction = action

        """
        arrStuff = list()

        for i in range(len(mazeWorld)):
            for j in range(len(mazeWorld[i])):
                temp = ""
                tempBool = False
                if mazeWorld[i][j] == -999:
                    temp = "           \n     W     \n             \n"
                elif not mazeWorld[i][j] == 0:
                    temp = "           \n     %d     \n             \n" % (mazeWorld[i][j])
                else:
                    for action in range(4):
                        if tempBool == True:
                            if action == LEFT or action == RIGHT:
                                continue
                        if action == UP:
                            temp += "    %s    \n" % (str(QLookup[(state(j, i), action)])[0:4])
                        elif action == DOWN:
                            temp += "    %s    \n" % (str(QLookup[(state(j, i), action)])[0:4])
                        elif action == LEFT or action == RIGHT:
                            tempBool = True
                            temp += "%s    %s\n" % (str(QLookup[(state(j, i), LEFT)])[0:4], str(QLookup[(state(j, i), RIGHT)])[0:4])
                arrStuff.append(temp)
            print ""

        for i in range(len(mazeWorld)):
            for j in range(len(mazeWorld[i])):
                print arrStuff[0],
                arrStuff.pop(0)
            print ""
        pdb.set_trace()
        """

        """
        for i in range(len(mazeWorld)):
            for j in range(len(mazeWorld[i])):
                if currState == (i, j):
                    print "~~~X~~~".ljust(6) + "|",
                elif mazeWorld[i][j] == -999:
                    print "~~~W~~~".ljust(6) + "|",
                else:
                    print str(mazeWorld[i][j]).ljust(6)[0:6] + " |",
            print ""
        """

        #pdb.set_trace()
        moveCount[(state(currState[1], currState[0]), action)] += 1
        QLookup[(state(currState[1], currState[0]), maxCurrAction)] = QLookup[(state(currState[1], currState[0]), maxCurrAction)] + learningRate(iteration) * (reward(maxNextState[1], maxNextState[0]) + discount * (QLookup[(state(maxNextState[1], maxNextState[0]), maxNextAction)]) - QLookup[(state(currState[1], currState[0]), maxCurrAction)])

#        print "Curr state (%d, %d)\nNext State (%d, %d)\nQLookup %f" % (currState[0], currState[1], maxNextState[0], maxNextState[1], QLookup[(state(currState[1], currState[0]), maxCurrAction)])
        currState = maxNextState

        iteration += 1
        endOrNah = checkEnd(currState)
        if endOrNah == 1:
            episodes += 1
            currState = starting
            rmse.append(rootmeansquare(val, QLookup, iteration))
            if rmse[len(rmse) - 1] > maxRMSE:
                maxRMSE = rmse[len(rmse) - 1]

    maxRMSE *= 1.1
    plt.plot(range(maxE), rmse)
    plt.title("RMSE Values")
    plt.xlabel("Episodes")
    plt.ylabel("RMSE value")
    plt.axis([0, maxE, 0, maxRMSE])
    plt.show()

    for i in range(len(mazeWorld)):
        for j in range(len(mazeWorld[i])):
            if mazeWorld[i][j] == -999:
                print "~~~W~~~".ljust(6) + "|",
            else:
                maxVal = INT_MIN
                maxAction = 0
                for action in range(4):
                    if QLookup[(state(j, i), action)] > maxVal:
                        maxVal = QLookup[(state(j, i), action)]
                print str(maxVal).ljust(6)[0:6] + " |",
        print ""

    for i in range(len(mazeWorld)):
        for j in range(len(mazeWorld[i])):
            maxAction = 0
            maxVal = INT_MIN

            for k in range(4):
                if mazeWorld[i][j] == -999:
                    continue
                tempVal = QLookup[(state(j, i), k)]
                if tempVal > maxVal:
                    maxVal = tempVal
                    maxAction = k


            if mazeWorld[i][j] is not 0:
                if mazeWorld[i][j] == -999:
                    print "W |",
                else:
                    print "%s |" % (str(mazeWorld[i][j]).ljust(1)),
            elif maxAction == UP:
                print "^ |",
            elif maxAction == DOWN:
                print "v |",
            elif maxAction == LEFT:
                print "<-|",
            else:
                print "->|",
        print ""

    """
    for i in range(len(mazeWorld)):
        for j in range(len(mazeWorld[i])):
            for k in range(4):
                if mazeWorld[i][j] is not 0:
                    if mazeWorld[i][j] == -999:
                        print "W |",
                        break
                    else:
                        print "%s |" % (str(mazeWorld[i][j]).ljust(1)),
                        break
                print "(%d, %d) action %s: %f" % (i, j, stateLookup[k], QLookup[(state(j, i), k)])
            print ""
    """

    # print QLookup

    return

