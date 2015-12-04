import copy
import os
import sys
from Queue import Queue
from sets import Set
import pdb
from gridWorld import mazeWorld, UP, DOWN, LEFT, RIGHT, right, intended, left, discount

STOP = 1

def rewardFunc(y, x):
    if mazeWorld[y][x] == 0:
        return -0.04
    elif mazeWorld[y][x] == -999:
        return 0
    else:
        return mazeWorld[y][x]

# mazeWorld = updateMazeWorld(mazeWorld)

def valueIteration():
    t = 1
    values = list()
    values.append(copy.deepcopy(mazeWorld))
    moves = list()

    while True:
        terminals = list()
        curr = copy.deepcopy(values[t - 1])
        currMoves = copy.deepcopy(values[t-1])

        for y in range(len(mazeWorld)):
            for x in range(len(mazeWorld[y])):
                if STOP == 1:
                    if values[t-1][y][x] is not 0 and values[t-1][y][x] is not -999:
                        terminals.append((y, x))
                else:
                    if values[t - 1][y][x] is not -999:
                        terminals.append((y,x))

        for terminal in terminals:
            surroundingBlocks = getSurroundingBlocks(terminal)

            for block in surroundingBlocks:
                actions = getActions(block)
                prev = values[t - 1]
                maxAction = -9999
                bestAction = -1

                for actionSet in actions:
                    total = 0.0

                    for action in actionSet:
                        y = action[0]
                        x = action[1]

                        if y < len(mazeWorld) and y >= 0 and x < len(mazeWorld[0]) and x >= 0:
                            if not mazeWorld[y][x] == -999:
                                total += (action[2] * (prev[action[0]][action[1]]))

                    if total > maxAction:
                        bestAction = actionSet
                        maxAction = total
                curr[block[0]][block[1]] = rewardFunc(block[0], block[1]) + discount * maxAction
                currMoves[block[0]][block[1]] = bestAction[0][3]

        values.append(curr)
        moves.append(currMoves)


        if converged(values[t], values[t - 1]):
            break

        t += 1
    for i in range(len(mazeWorld)):
        for j in range(len(mazeWorld[i])):
            if values[t-1][i][j] == -999:
                print "~~~W~~~".ljust(6) + "|",
            else:
                print str(values[t-1][i][j]).ljust(6)[0:6] + " |",
        print ""

    for i in range(len(mazeWorld)):
        for j in range(len(mazeWorld[i])):
            move = moves[t-1][i][j]
            if STOP == 0 and mazeWorld[i][j] == -999:
                print "W  |",
            elif STOP == 1 and mazeWorld[i][j] is not 0:
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

def converged(first, second):
    thresh = 0.0001
    for i in range(len(first)):
        for j in range(len(first[i])):
            if abs(first[i][j] - second[i][j]) > thresh:
                return False
    return True

def getSurroundingBlocks(block):
    blocks = list()
    yA = block[0]
    xA = block[1]

    for y in range(yA - 1, yA + 2):
        for x in range(xA - 1, xA + 2):
            if x == xA and y == yA:
                continue
            if y < len(mazeWorld) and y >= 0 and x < len(mazeWorld[0]) and x >= 0:
                if STOP == 1:
                    if mazeWorld[y][x] is 0 and mazeWorld[y][x] is not -999:
                        blocks.append((y, x))
                else:
                    if mazeWorld[y][x] is not -999:
                        blocks.append((y,x))

    return blocks

"""
Only return valid actions
"""
def getActions(node):
    actions = list()
    x = node[1]
    y = node[0]

    actions.append([(y - 1, x, intended, UP), (y, x + 1, right), (y, x - 1, left)])
    actions.append([(y + 1, x, intended, DOWN), (y, x + 1, right), (y, x - 1, left)])
    actions.append([(y, x + 1, intended, RIGHT), (y - 1, x, right), (y + 1, x, left)])
    actions.append([(y, x - 1, intended, LEFT), (y - 1, x, right), (y + 1, x, left)])

    return actions
