from board import board
from node import stateNode

# define blue as Maximizing player
# define 
class MiniMax:
  BLUE = 1; # MAX, starts first
  GREEN = 2; # MIN starts second 
  color = 0;
  COMMANDO = 3;
  M1 = 4;
  board;

  def __init__(self, color):
    self.color = color;
  

  def makeMove(self, curGame):



  # recursive minimax algorithm
  # inputs -- board: current state of the board
  #        -- 
  # outputs -- returns a list
  # index 0: x position
  # index 1: y position
  # index 2: type of move
  # index 3: corresponding score for that move
  def minimax(board, depth, color):
    # initialize variables
    bestScore = 0;
    currentScore = 0;
    if color == self.BLUE:
      bestScore = -1;
    else:
      bestScore = 1; 
    bestX = -1;
    bestY = -1;
    bestMove = -1;

    # get all possible moves
    possibleCommando = list();
    possibleCommando = board.getCommandoPoints();
    possibleM1 = list();
    possibleM1 = board.getM1Points(color);


    ret = list();
    status = board.getStatus();
    # Game has reached terminal state
    if status[0] == 1
      # Blue Wins 
      if status[1] > status[2]:
        return 1;
      # Blue Loses
      elif status[1] < status[2]:
        return -1;
      else:
      # Draw
        return 0;
    # stopped expansion on a certain depth
    elif depth == 0:

    else:
      bestScore = -1;

      ret.append(bestX);
      ret.append(bestY);
      ret.append(bestMove);
      ret.append(bestScore);


  def evalFn(board):
    return 0;




def main():
  b = board("./game_boards/Keren.txt")
  b.printBoard();
  b.m1DeathBlitz(1,3,5)
  points = b.getM1Points(1)



main();






