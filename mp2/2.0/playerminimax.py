from board import board
from node import stateNode

class MiniMax:
  BLUE = 1;
  GREEN = 2;
  color = 0;
  COMMANDO = 3;
  M1 = 4;
  board;

  def __init__(self, color, board):
    self.color = color;
    self.board = board;

  def minimax(board, depth, color):
    status = board.getStatus();
    if status[0] == 1
      if status[1] > status[2]:
        return 1;
      elif status[1] < status[2]:
        return -1;
      else:
        return 0;
    elif depth == 0:
        return evalfn(board)
    else:
      bestScore = -1;


  def evalFn(board):
    return 0;




def main():
  b = board("./game_boards/Keren.txt")
  b.printBoard();
  b.m1DeathBlitz(1,3,5)
  points = b.getM1Points(1)



main();






