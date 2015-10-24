import pdb
from board import board
from playerminimax import MinimaxPlayer
import copy

class Simulation:
  BLUE = 0;
  GREEN = 0;
  def __init__(self, board):
    self.BLUE = 1;
    self.GREEN = 2;
    self.board = board;




  def run(self, maxPlayer, minPlayer, isTest):
    status = self.board.getStatus();
    if not isTest:
      while status[0] != 1:
        temp = board(None);
        
        self.board.copycctor(temp);
        #temp.printOccupants();
        move1 = maxPlayer.generateMove(temp);
        #self.board.printOccupants();
        
        self.board.makeMove(move1);
        #print move1;
        #self.board.printOccupants();

        temp = board(None);
        
        self.board.copycctor(temp);
        #temp.printOccupants();
        move2 = minPlayer.generateMove(temp);
        #self.board.printOccupants();
        
        self.board.makeMove(move2);
        #print move2;
        #self.board.printOccupants();
        status = self.board.getStatus();
      self.board.printBoard();
      print self.board.getStatus();
    else:
      temp = board(None);
      
      self.board.copycctor(temp);
      #temp.printOccupants();
      move1 = maxPlayer.generateMove(temp);
      print;
      #self.board.printOccupants();
      
      self.board.makeMove(move1);
      print move1;
      self.board.printOccupants();






def main():
  b = board("./game_boards/Sevastopol.txt");
  p1 = MinimaxPlayer(1);
  p2 = MinimaxPlayer(2);
  s = Simulation(b);
  s.run(p1,p2, False);




main()






