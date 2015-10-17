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
  vals = [[0 for x in range(BOARD_SIZE)] for x in range(BOARD_SIZE)];
  # who occupies each square on the board
  # 0: none
  # 1: blue
  # 2: green
  occupant = [[0 for x in range(BOARD_SIZE)] for x in range(BOARD_SIZE)]; 


  # initializes 6 by 6 board with random values
  # initializes occupied board all to zero
  def __init__(self):
    i = 0;
    for x in range(0, self.BOARD_SIZE):
      for y in range (0, self.BOARD_SIZE):
        self.vals[y][x] = randint(1,99);
        self.occupant[y][x] = 0;


  def printBoard(self):
    temp = ""
    for y in range(0, self.BOARD_SIZE):
      for x in range(0, self.BOARD_SIZE):
        if(self.vals[y][x] < 10):
          temp = temp + str(self.vals[y][x]) + "  ";
        else:
          temp = temp + str(self.vals[y][x]) + " ";
      print temp;
      temp = "";


  def nodeVal(self, x, y):
    return self.vals[y][x];

  def nodeOccupant(self, x,y):
    return self.occupant[y][x];



  # executes commando para drop on board
  # inputs -- x, y : location on where to drop
  #           player =  green (2) or blue (1) 
  # outputs -- node value if successful, -1 if failed
  def commandoParaDrop(self, player, x,y):
    if self.occupant[y][x] == 0:
      self.occupant[y][x] = player;
      return self.vals[y][x];
    else:
      return -1;

  # same as commandoParaDrop but does not actually populate board
  # inputs -- x, y : location on where to drop
  #           player =  green (2) or blue (1) 
  # outputs -- node value if successful, -1 if failed  
  def commandoParDropPeek(self, x,y):
    if self.occupant[y][x] == 0:
      return self.vals[y][x];
    else:
      return -1;



  # executes M1 Death Blitz on board
  # inputs -- x, y : location on where to drop
  #           player =  green (2) or blue (1) 
  # outputs -- total values earned if successful, -1 if failed
  def m1DeathBlitz(self, player, x, y):
    ret = 0;
    opposingPlayer = 0;
    if player == self.GREEN:
      opposingPlayer = self.BLUE;
    else:
      opposingPlayer = self.GREEN;
    # take initial spot
    self.occupant[y][x] = player;

    # check neighbors for opposing pieces and change them
    # right
    if x + 1 >= self.BOARD_SIZE:
      if self.occupant[y][x + 1] == opposingPlayer:
        self.occupant[y][x + 1] = player;
    # left 
    if x - 1 < 0:
      if self.occupant[y][x - 1] == opposingPlayer:
        self.occupant[y][x - 1] = player;
    # up 
    if y + 1 >= self.BOARD_SIZE:
      if self.occupant[y + 1][x] == opposingPlayer:
        self.occupant[y + 1][x] = player;
    # down
    if y - 1 < 0:
      if self.occupant[y - 1][x] == opposingPlayer:
        self.occupant[y - 1][x] = player;








  # gets current status of the board
  # inputs -- NONE
  # outputs -- list
  #   index 0: whether or not game is over
  #   index 1: blue score
  #   index 2: green score
  def getStatus(self):
    game_over = 1;
    blue_score = 0;
    green_score = 0;
    ret = [];
    for x in range(0, self.BOARD_SIZE):
      for y in range (0, self.BOARD_SIZE):
        if self.occupant[y][x] == self.BLUE:
          blue_score += self.vals[y][x];
        elif self.occupant[y][x] ==  self.GREEN:
          green_score += self.vals[y][x];
        else:
          game_over = 0;
    ret.append(game_over);
    ret.append(blue_score);
    ret.append(green_score);

    return ret






def main():
  b = board()
  b.printBoard()
  status  = b.getStatus()
  print status

main()