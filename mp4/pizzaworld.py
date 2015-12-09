import os
import sys
import random
import numpy as np
from math import sqrt

R = [[-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999],
     [-999, -1, -1, -1, -1, -1, -1, -1, -1, 10, -1, -1, -1, -1, -999],
     [-999, -1, 12, -1,-1,-1,-1,-1,-1,-1,-1,-1, 12, -1, -999],
     [-999, -1, -1, -1, -999, -1, -1, -1, -1, -1, -999, -1, -1, -1, -999],
     [-999, -999, -999, -999, -999, -1, -1, -1, -1, -1, -999, -999, -999, -999, -999,],
     [-999, -1,-1,-1,-1,-1,-1,-1,-1,-1,-999,-1,-1,-1,-999],
     [-999, -1, 11, -1,-1,-1,-1,-1,-1,-1,-1,-1, 11,-1,-999],
     [-999, -1,-1,-1,-1,-1,10,10,-1,-1,-1,-1,-1,-1,-999],
     [-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999]]

Q = dict()

action = dict()
action[0]="up"
action[1]="left"
action[2]="right"
action[3]="down"
action[4]="stay"

discount = 0.99

starting = (5,6)

def global_pizza(val):
    global pizza
    pizza = val

def global_ingredients(val):
    global ingredients
    ingredients = val

def state(x,y):
    return y* len(R) + x

def learningRate(t):
    return 60/(59.0 + t)

def exploration(q, n):
    if n < 100:
        return random.random()
    return q

def reward(x,y):
    if R[y][x] == -1:
        return -0.1
    elif R[y][x] == -999:
        return -0.1
    elif R[y][x] == 11:
        if ingredients == 0:
            global_ingredients(1)
            return -0.1
        else:
            return -0.1
    elif R[y][x] == 10:
        if (pizza == 0 and ingredients == 1):
            global_pizza(1)
            global_ingredients(0)
            return -0.1
        else:
            return -0.1
    elif R[y][x] == 12:
        if (pizza == 1):
            return 5
        else:
            return -0.1

def move(s,a):
    y = s[1]
    x = s[0]

    if a == 0:
        y -= 1
    elif a == 1:
        x -= 1
    elif a ==2:
        x += 1
    else:
        y += 1


    if (y < len(R) and y >= 0 and x < len(R[0]) and x >= 0):
        if R[y][x]== -999:
            y = s[1]
            x = s[0]
    else:
        y = s[1]
        x = s[0]

    if a == 4:
        y = s[1]
        x = s[0]

    return state(x,y)


def initializeQ():
    for i in range(len(R)):
        for j in range(len(R[i])):
            for k in range(5):
                if not R[i][j] == -999:
                    Q[(state(j, i), k)] = 0.0
                else:
                    Q[(state(j, i), k)] = -999

def initializeMoveSet(moves):
    for i in range(len(R)):
        for j in range(len(R[i])):
            for k in range(5):
                if not R[i][j] == -999:
                    moves[(state(j, i), k)] = 0.0
                else:
                    moves[(state(j, i), k)] = -999

def initializeMoveCount(moves):
    for i in range(len(R)):
        for j in range(len(R[i])):
            for k in range(5):
                if not R[i][j] == -999:
                    moves[(state(j, i), k)] = 0
                else:
                    moves[(state(j, i), k)] = -999



def tupleFromState(s):
    return (s/len(R), s % len(R))

def Qlearning():
    moveSet = dict()
    moveCount = dict()
    initializeMoveSet(moveSet)
    initializeMoveCount(moveCount)
    initializeQ()

    episode = 0
    max_epi = 800

    global_pizza(0)
    global_ingredients(0)

    currState = starting


    while episode < max_epi:
        maxCurrAction = 0
        maxVal = -1000

        for action in range(4):
            tempVal = exploration(Q[(state(currState[1], currState[0]), action)], moveCount[(state(currState[1], currState[0]), action)])
            if tempVal > maxVal:
                maxVal = tempVal
                maxCurrAction = action

        maxNextState = 0
        maxVal = -1000
        temp = random.randint(1,100)

        x = currState[1]
        y = currState[0]

        if (R[y][x] == -1 and pizza == 0):
            if temp <= 10 :
                if maxCurrAction == 0:
                    maxCurrAction = 1
                elif maxCurrAction == 1:
                    maxCurrAction = 0
                elif maxCurrAction == 2:
                    maxCurrAction = 3
            elif (temp >= 11 and temp <= 20) :
                if maxCurrAction == 0:
                    maxCurrAction = 2
                elif maxCurrAction == 1:
                    maxCurrAction = 3
                elif maxCurrAction == 2:
                    maxCurrAction = 0
        elif (R[y][x]== -1 and pizza == 1):
            if temp >= 96:
                maxCurrAction = 4
            elif temp <= 5 :
                if maxCurrAction == 0:
                    maxCurrAction = 1
                elif maxCurrAction == 1:
                    maxCurrAction = 0
                elif maxCurrAction == 2:
                    maxCurrAction = 3
            elif (temp >= 6 and temp <= 10) :
                if maxCurrAction == 0:
                    maxCurrAction = 2
                elif maxCurrAction == 1:
                    maxCurrAction = 3
                elif maxCurrAction == 2:
                    maxCurrAction = 0
        elif (R[y][x] == 10 and pizza == 1):
            if temp >= 71:
                maxCurrAction = 4
            elif temp <= 5 :
                if maxCurrAction == 0:
                    maxCurrAction = 1
                elif maxCurrAction == 1:
                    maxCurrAction = 0
                elif maxCurrAction == 2:
                    maxCurrAction = 3
            elif (temp >= 6 and temp <= 10) :
                if maxCurrAction == 0:
                    maxCurrAction = 2
                elif maxCurrAction == 1:
                    maxCurrAction = 3
                elif maxCurrAction == 2:
                    maxCurrAction = 0

        maxNextState = tupleFromState(move(currState, maxCurrAction))

       # if not maxNextState == currState:
       # if not maxNextState == currState:
        for action in range(5):
            tempVal = Q[(state(maxNextState[1], maxNextState[0]), action)]
            if tempVal > maxVal:
                maxVal = tempVal
                maxNextAction = action

        moveCount[(state(currState[1], currState[0]), action)] += 1
        Q[(state(currState[1], currState[0]), maxCurrAction)] = Q[(state(currState[1], currState[0]), maxCurrAction)] + learningRate(episode) * (reward(maxNextState[1], maxNextState[0]) + discount * (Q[(state(maxNextState[1], maxNextState[0]), maxNextAction)]) - Q[(state(currState[1], currState[0]), maxCurrAction)])

        currState = maxNextState
        moveCount[(state(currState[1], currState[0]), action)] += 1
        Q[(state(currState[1], currState[0]), maxCurrAction)] = Q[(state(currState[1], currState[0]), maxCurrAction)] + learningRate(episode) * (reward(maxNextState[1], maxNextState[0]) + discount * (Q[(state(maxNextState[1], maxNextState[0]), maxNextAction)]) - Q[(state(currState[1], currState[0]), maxCurrAction)])

#        print "Curr state (%d, %d)\nNext State (%d, %d)\nQLookup %f" % (currState[0], currState[1], maxNextState[0], maxNextState[1], QLookup[(state(currState[1], currState[0]), maxCurrAction)])
        currState = maxNextState
        episode +=1



    for i in range(len(R)):
        for j in range(len(R[i])):
            maxAction = 0
            maxVal = -1000

            for k in range(4):
                if R[i][j] == -999:
                    continue
                tempVal = Q[(state(j, i), k)]
                if tempVal > maxVal:
                    maxVal = tempVal
                    maxAction = k



            if R[i][j] == -999:
                print "W |",
            elif maxAction == 0:
                print "^ |",
            elif maxAction == 3:
                print "v |",
            elif maxAction == 1:
                print "<-|",
            elif maxAction == 2:
                print "->|",
            elif maxAction == 4:
                print ". |",
        print ""
    return


def main():
    Qlearning()

if __name__ == "__main__":
    main()