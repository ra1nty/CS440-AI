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


  # initializes occupied board all to zero
  # parses file into board values 
  def __init__(self, filename):
    i = 0;

    with open(filename, 'r') as f:
      temp = f.read()

    arrayBoard = list()
    boardRow = list()

    for c in temp:
      if c != '\n':
        if c != '\t' and c != '\r':
          boardRow.append(c)

      else:
        arrayBoard.append(boardRow)
        boardRow = list()

    print arrayBoard

    for x in range(0, self.BOARD_SIZE):
      for y in range (0, self.BOARD_SIZE):
        self.occupant[y][x] = 0;
        self.vals[y][x] = int(arrayBoard[y][x]);




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

  # gets points for commando move
  # inputs -- NONE
  # outputs -- list containing lists of x,y values of open commando points
  # For each element in commandolist
  #   index 0 : x
  #   index 1 : y
  def getCommandoPoints(self):
    commandoList = list();
    coord = list();

    for x in range(0, self.BOARD_SIZE):
      for y in range (0, self.BOARD_SIZE):
        # check to see if point is occupied
        if self.occupant[y][x] == 0:
          coord.append(x);
          coord.append(y);
          commandoList.append(coord);
          coord = list();

    return commandoList;

  # gets points for m1 blitz move
  # inputs -- color
  # outputs -- list containing lists of x,y values of potential M1 blitz points
  # For each element in m1Points
  #   index 0 : x
  #   index 1 : y
  def getM1Points(self, color):
    m1Points = list();
    coord = list();
    for x in range(0, self.BOARD_SIZE):
      for y in range (0, self.BOARD_SIZE):
        if self.occupant[y][x] == color:
          # right
          if x + 1 < self.BOARD_SIZE:
            coord.append(x + 1);
            coord.append(y);
            m1Points.append(coord);
            coord = list();
          # left 
          if x - 1 >= 0:
            coord.append(x - 1);
            coord.append(y);
            m1Points.append(coord);
            coord = list();
          # up 
          if y + 1 < self.BOARD_SIZE:
            coord.append(x);
            coord.append(y + 1);
            m1Points.append(coord);
            coord = list();            
          # down
          if y - 1 >= 0:
            coord.append(x);
            coord.append(y - 1);
            m1Points.append(coord);
            coord = list();  

    return m1Points;




def main():
  b = board("./game_boards/Keren.txt")
  b.printBoard();
  b.m1DeathBlitz(1,1,1)
  points = list();
  points = b.getM1Points(1)
  print points;

main()