import sys
import pdb
import os
from random import randint

class board:
  NONE = 0;
  BLUE = 1;
  GREEN = 2;
  BOARD_SIZE = 6;
  # board values for each square
  vals = [[0 for x in range(BOARD_SIZE)] for x in range(BOARD_SIZE)]
  # who occupies each square on the board
  # 0: none
  # 1: blue
  # 2: green
  occupant = [[0 for x in range(BOARD_SIZE)] for x in range(BOARD_SIZE)] 


  # initializes 6 by 6 board with random values

  def __init__(self):
    i = 0;
    for x in range(0, self.BOARD_SIZE):
      for y in range (0, self.BOARD_SIZE):
        self.vals[y][x] = randint(1,99)
        self.occupant[y][x] = 0;


  def printBoard(self):
    temp = ""
    for y in range(0, self.BOARD_SIZE):
      for x in range(0, self.BOARD_SIZE):
        if(self.vals[y][x] < 10):
          temp = temp + str(self.vals[y][x]) + "  "
        else:
          temp = temp + str(self.vals[y][x]) + " "
      print temp
      temp = ""


  def nodeVal(self, x, y):
    return self.vals[y][x];

  def nodeOccupant(self, x,y):
    return self.occupant[y][x]


  # executes commando para drop on board
  # inputs -- x, y : location on where to drop
  #           player =  green (2) or blue (1) 
  # outputs -- node value if successful, -1 if failed
  def commandoParaDrop(self, player, x,y):
    if self.occupant[y][x] == 0
      self.occupant[y][x] = player 
      return self.vals[y][x]
    else
      return -1

  def m1DeathBlitz(self, player, x, y):





def main():
  b = board()
  b.printBoard()
    

main()