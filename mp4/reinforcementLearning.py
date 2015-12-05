import os
import sys
import copy
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
DOWN = 2
LEFT = 1
RIGHT = 3

INT_MIN = -99999

def state(x, y):
    return y * len(mazeWorld) + x

def learningRate(time):
    return 60/(59.0 + time)

def reward(x, y):
    if mazeWorld[y][x] == 0:
        return -0.4
    elif mazeWorld[y][x] == -999:
        return -999
    else:
        return mazeWorld[y][x]

def evalFunc(q, n):
    return q

def tupleFromState(s):
    return (s/len(mazeWorld), s % len(mazeWorld))

def initializeQLookup():
    for i in range(len(mazeWorld)):
        for j in range(len(mazeWorld[i])):
            for k in range(4):
               # if not mazeWorld[i][j] == -999:
                QLookup[(state(j, i), k)] = reward(j, i)

def initializeMoveSet(moves):
    for i in range(len(mazeWorld)):
        for j in range(len(mazeWorld[i])):
            for k in range(4):
               # if not mazeWorld[i][j] == -999:
                moves[(state(j, i), k)] = 0.0

def initializeMoveCount(moves):
    for i in range(len(mazeWorld)):
        for j in range(len(mazeWorld[i])):
            for k in range(4):
               # if not mazeWorld[i][j] == -999:
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
            y = s[0]
            x = s[1]
    else:
        y = s[0]
        x = s[1]


    # Return the state
    return state(x, y)

def checkEnd(s):
    x = s[1]
    y = s[0]
    if not mazeWorld[y][x] == -999 and not mazeWorld[y][x] == 0:
        return 1
    return 0

def reinforcementLearning():
    moveSet = dict()
    moveCount = dict()
    initializeMoveSet(moveSet)
    initializeMoveCount(moveCount)
    initializeQLookup()

    currState = starting
    iteration = 0

    # s - number
    # action - number
    # nextstate - tuple
    # maxAction - number
    # time - number

    episodes = 0

    while episodes < 870:
        maxCurrAction = 0
        maxVal = INT_MIN

        # Find the max action at current state
        for action in range(4):
            tempNextState = performAction(currState, action)
            tempVal = QLookup[(state(currState[1], currState[0]), action)]
            if tempVal > maxVal:
                maxVal = tempVal
                maxCurrAction = action

        maxNextAction = 0
        maxVal = INT_MIN
        maxNextState = tupleFromState(performAction(currState, maxCurrAction))

        for action in range(4):
            tempNextState = performAction(maxNextState, action)
            tempVal = QLookup[(state(maxNextState[1], maxNextState[0]), action)]
            if tempVal > maxVal:
                maxVal = tempVal
                maxNextAction = action

        moveCount[(state(currState[1], currState[0]), action)] += 1
        QLookup[(state(currState[1], currState[0]), maxCurrAction)] = QLookup[(state(maxNextState[1], maxNextState[0]), maxCurrAction)] + learningRate(iteration) * (reward(currState[1], currState[0]) + discount * (QLookup[(state(maxNextState[1], maxNextState[0]), maxNextAction)]) - QLookup[(state(currState[1], currState[0]), maxCurrAction)])

#        print "Curr state (%d, %d)\nNext State (%d, %d)\nQLookup %f" % (currState[0], currState[1], maxNextState[0], maxNextState[1], QLookup[(state(currState[1], currState[0]), maxCurrAction)])
        currState = maxNextState

        iteration += 1
        endOrNah = checkEnd(currState)
        if endOrNah == 1:
            episodes += 1
            currState = starting
            iteration = 0

    for i in range(len(mazeWorld)):
        for j in range(len(mazeWorld[i])):
            maxAction = 0
            maxVal = INT_MIN

            for k in range(4):
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

    return

