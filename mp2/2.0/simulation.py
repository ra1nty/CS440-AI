import pdb
from board import board
from playerminimax import MinimaxPlayer
import copy
import time

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
        move1 = maxPlayer.generateMove(temp);
        
        self.board.makeMove(move1);
        #print "player 1 move"
        #print move1;

        temp = board(None);
        
        self.board.copycctor(temp);

        move2 = minPlayer.generateMove(temp);
        
        self.board.makeMove(move2);
        #print "player 2 move"
        #print move2;

        status = self.board.getStatus();
      #  self.board.printBoard();
        #sprint;
        #time.sleep(1)
      self.board.printBoard();

      # Print Scores
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

  print "Keren Minimax vs Minimax"
  b = board("./game_boards/Keren.txt");
  p1 = MinimaxPlayer(1);
  p2 = MinimaxPlayer(2);
  s = Simulation(b);
  s.run(p1,p2, False);

  print "Narvik Minimax vs Minimax"
  b = board("./game_boards/Narvik.txt");
  p1 = MinimaxPlayer(1);
  p2 = MinimaxPlayer(2);
  s = Simulation(b);
  s.run(p1,p2, False);


  print "Sevastopol Minimax vs Minimax"
  b = board("./game_boards/Sevastopol.txt");
  p1 = MinimaxPlayer(1);
  p2 = MinimaxPlayer(2);
  s = Simulation(b);
  s.run(p1,p2, False);

  print "Smolensk Minimax vs Minimax"
  b = board("./game_boards/Smolensk.txt");
  p1 = MinimaxPlayer(1);
  p2 = MinimaxPlayer(2);
  s = Simulation(b);
  s.run(p1,p2, False);

  print "Westerplatte Minimax vs Minimax"
  b = board("./game_boards/Westerplatte.txt");
  p1 = MinimaxPlayer(1);
  p2 = MinimaxPlayer(2);
  s = Simulation(b);
  s.run(p1,p2, False);


main()






