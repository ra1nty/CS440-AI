import os
import sys
from Queue import Queue
from sets import Set
import pdb
import copy
import valueIteration
from reinforcementLearning import *
from policyIteration import *

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

def main():
    print "~~~~~~~~~~ Value iteration rewards mean stop ~~~~~~~~~~\n\n"
    valueIteration.valueIteration()
    valueIteration.STOP = 0
    print "\n\n~~~~~~~~~~ Value iteration rewards mean nothing ~~~~~~~~~~\n\n"
    valueIteration.valueIteration()

    print "\n\n~~~~~~~~~~ Reinforcement Learning ~~~~~~~~~~\n\n"
    reinforcementLearning()

if __name__ == "__main__":
    main()
