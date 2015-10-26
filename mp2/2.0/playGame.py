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
    while status[0] != 1:
      self.board.printBoard();
      move = input("Enter your move \n");
      parsedMove = parseUserInput(move);
      parsedMove.append(1);

      self.board.makeMove(parsedMove);
      #print "player 1 move"
      #print move1;

      temp = board(None);
      
      self.board.copycctor(temp);

      move2 = AI.generateMove(temp);
      
      self.board.makeMove(move2);
      #print "player 2 move"
      #print move2;

      status = self.board.getStatus();
      self.board.printBoard();
      print;
    self.board.printBoard();

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

def main():
  b = board("./game_boards/Keren.txt");
  p1 = MinimaxPlayer(2);
  g = Game(b);
  g.runGame(p1);

main();
