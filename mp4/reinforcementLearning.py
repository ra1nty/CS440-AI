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

def state(x, y):
    return y * len(mazeWorld) + x

def learningRate(time):
    return 60/(59.0 + time)

def reward(y, x):
    if mazeWorld[y][x] == 0:
        return -0.4
    elif mazeWorld[y][x] == -999:
        return 0
    else:
        return mazeWorld[y][x]

def evalFunc(q, n):
    return q

def initializeQLookup():
    for i in range(len(mazeWorld)):
        for j in range(len(mazeWorld[i])):
            for k in range(0, 4):
                if not mazeWorld[i][j] == -999:
                    QLookup[(state(j, i), k)] = reward(i, j)

def initializeMoveSet(moves):
    for i in range(len(mazeWorld)):
        for j in range(len(mazeWorld[i])):
            for k in range(4):
                if not mazeWorld[i][j] == -999:
                    moves[(state(i, j), k)] = 0.0

def initializeMoveCount(moves):
    for i in range(len(mazeWorld)):
        for j in range(len(mazeWorld[i])):
            for k in range(4):
                if not mazeWorld[i][j] == -999:
                    moves[(state(i, j), k)] = 0

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

    if y < len(mazeWorld) and y >= 0 and x < len(mazeWorld[0]) and x >= 0:
        if mazeWorld[y][x] == -999:
            pdb.set_trace()
            y = s[0]
            x = s[1]
    else:
        y = s[0]
        x = s[1]

    return state(x, y)

def reinforcementLearning():
    moveSet = dict()
    moveCount = dict()
    initializeMoveSet(moveSet)
    initializeMoveCount(moveCount)
    initializeQLookup()

    currState = starting
    iteration = 0
    QUpdate = lambda state, action, nextstate, maxAction, time: QLookup[(state, action)] + learningRate(time) * (reward(state) + discount * (QLookup[(nextstate, maxAction)] - QLookup[(state, action)]))

    while iteration < 100000:
        maxAction = 0
        nextState = 0
        nextMaxAction = 0

        tempMax = 0
        maxVal = -99999
        tempNextState = 0

        # Find next max state
        for action in range(4):
            tempNextState = performAction(currState, action)
            try:
                tempMax = evalFunc(QLookup[(tempNextState, action)], moveCount[(tempNextState, action)])
            except Exception:
                pdb.set_trace()
            if tempMax > maxVal:
                maxVal = tempMax
                maxAction = action
                nextState = tempNextState

        tempMax = 0
        maxVal = -99999
        tempNextState = 0

        # Find next max action

        for action in range(4):
            tempNextState = performAction(nextState, action)
            tempMax = evalFunc(QLookup[(tempNextState, action)], moveCount[(tempNextState, action)])
            if tempMax > maxVal:
                maxVal = tempMax
                nextMaxAction = action

        moveCount[(tempNextState, action)] += 1
        QLookup[(state, action)] = QUpdate(state(currState[0], currState[1]), maxAction, nextState, nextMaxAction, iteration)

        iteration += 1

    pass

