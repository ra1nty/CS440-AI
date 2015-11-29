import os
import sys
from Queue import Queue
from sets import Set
import pdb
import copy

mazeWorld = [[0, -1, 0, 0, 0, 0],
             [0, 0, 0, -999, -1, 0],
             [0, 0, 0, -999, 0, 3],
             [0, 0, 0, -999, 0, 0],
             [0, 0, 0, 0, 0, 0],
             [1, -1, 0, -999, -1, -1]]

starting = (4, 1)

policies = dict()
intended = 0.8
right = 0.1
left = 0.1
discount = 0.99

UP = 0
DOWN = 2
LEFT = 1
RIGHT = 3

def main():
    valueIteration()

def valueIteration():
    t = 1
    values = list()
    values.append(copy.deepcopy(mazeWorld))

    while True:
        
        
        if converges(values[t], values[t - 1]):
            break
        t += 1

def converges(first, second):
    thresh = 0.01
    for i in range(len(first)):
        for j in range(len(first[i])):
            if abs(first[i][j] - second[i][j]) > thresh:
                return False
    return True

def getFutureStates(startX, startY, prev):
    memo = list()
    visited = Set()
    for i in range(len(mazeWorld)):
        temp = list()
        for j in range(len(mazeWorld[0])):
            temp.append(0)
        memo.append(temp)

    _getFutureStates(startX, startY, memo, visited, prev)
    return memo

def _getFutureStates(x, y, memo, visited, prev):
    pass

def getActions(y, x):
    actions = list()
    actions.append([(y - 1, x, intended, UP), (y, x - 1, left, LEFT), (y, x + 1, right, RIGHT)])
    actions.append([(y, x - 1, intended, LEFT), (y + 1, x - 1, left, DOWN), (y - 1, x - 1, right, UP)])
    actions.append([(y + 1, x, intended, DOWN), (y, x - 1, left, RIGHT), (y, x + 1, right, LEFT)])
    actions.append([(y, x + 1, intended, RIGHT), (y + 1, x, left, DOWN), (y - 1, x, right, UP)])
    return actions


def validAction(action):
    y = action[0]
    x = action[1]
    return (y < len(mazeWorld) and y > 0 and x < len(mazeWorld[0]) and x > 0)

if __name__ == "__main__":
    main()
