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
    moves = list()

    while True:
        terminals = list()
        curr = copy.deepcopy(values[t - 1])
        currMoves = copy.deepcopy(values[t-1])

        for y in range(len(mazeWorld)):
            for x in range(len(mazeWorld[y])):
                if values[t-1][y][x] is not 0 and values[t-1][y][x] is not -999:
                    terminals.append((y, x))

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
                                total += (action[2] * (discount * prev[action[0]][action[1]]))

                    if total > maxAction:
                        bestAction = actionSet
                        maxAction = total
                curr[block[0]][block[1]] = maxAction
                currMoves[block[0]][block[1]] = bestAction[0][3]

        values.append(curr)
        moves.append(currMoves)

        for i in range(len(mazeWorld)):
            for j in range(len(mazeWorld[i])):
                if curr[i][j] == -999:
                    print "W |",
                else:
                    print str(curr[i][j]) + "|",
            print ""

        for i in range(len(mazeWorld)):
            for j in range(len(mazeWorld[i])):
                move = currMoves[i][j]
                if move == LEFT:
                    print "<- |",
                elif move == RIGHT:
                    print "-> |",
                elif move == UP:
                    print "^  |",
                else:
                    print "v  |",
            print ""
        pdb.set_trace()

        if converged(values[t], values[t - 1]):
            break

        t += 1

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
                if mazeWorld[y][x] is 0 and mazeWorld[y][x] is not -999:
                    blocks.append((y, x))

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

if __name__ == "__main__":
    main()
