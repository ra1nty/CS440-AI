import pdb
from board import board
from playerminimax import MinimaxPlayer
import copy
import time

class Game:

  def __init__(self, board):
    self.BLUE = 1;
    self.GREEN = 2;
    self.board = board;

  def runGame(self, AI):
    status = self.board.getStatus();
    self.board.printBoardforGame();
    while status[0] != 1:
      
      move = input("Enter your move \n");
      parsedMove = parseUserInput(move);
      parsedMove.append(1);

      if not isValidMove(parsedMove, self.board):
        print "Please enter a valid move";
        continue;
      self.board.makeMove(parsedMove);
      self.board.printBoardforGame();
      print;
      #print "player 1 move"
      #print move1;

      temp = board(None);
      
      self.board.copycctor(temp);

      move2 = AI.generateMove(temp);
      
      self.board.makeMove(move2);
      #print "player 2 move"
      #print move2;
      print move2;
      status = self.board.getStatus();
      self.board.printBoardforGame();
      print;
    self.board.printBoardforGame();

    # Print Scores
    print self.board.getStatus();

def parseUserInput(move):
  parsedMove = str(move);
  parsedMove = parsedMove.replace("(", "");
  parsedMove = parsedMove.replace(")", "");
  temp = parsedMove.split(",");
  ret = list();
  for num in temp:
    ret.append(int(num));
  return ret;

def isValidMove(move, board):
  if len(move) != 4:
    print "invalid number of arguements";
    return False;
  elif move[0] != 0 and move [0] != 1:
    print "invalid move type (index 0)";
    return False;
  elif move[1] >= 6 or move[2] >= 6:
    print "coordinates out of bounds";
    return False;
  elif move[1] < 0 or move[2] < 0:
    print "coordinates out of bounds";
    return False;
  elif board.occupant[move[2]][move[1]] != 0:
    print "space is occupied";
    return False;
  else:
    return True;


def main():
  b = board("./game_boards/Keren.txt");
  p1 = MinimaxPlayer(2);
  g = Game(b);
  g.runGame(p1);

main();
