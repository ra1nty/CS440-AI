import copy
from board import board
from node import stateNode

# define BLUE as Maximizing player
# define 
class MinimaxPlayer:
  BLUE = 1; # MAX, starts first
  GREEN = 2; # MIN starts second 
  color = 0;
  num = 0;

  def __init__(self, color):
    self.color = color;
  

  def generateMove(self, curGame):
    move = self.minimax(curGame,3, self.color);
    ret =  list();
    ret.append(move[2]);
    ret.append(move[0]);
    ret.append(move[1]);
    ret.append(self.color);

    return ret;


  def evalFn(self, board):
    status = board.getStatus();
    maxScore = status[1] + status[2];
    ret = float(status[1])/maxScore - float(status[2])/maxScore;
    return ret;


  # recursive minimax algorithm
  # inputs -- board: current state of the board
  #        -- depth: max depth
  #        -- color: color of the color
  # outputs -- returns a list
  # index 0: x position
  # index 1: y position
  # index 2: type of move
  # index 3: corresponding score for that move
  #   0: commando Para Drop
  #   1: M1 Death Blitz 
  def minimax(self, board, depth, color):
    #self.num = self.num + 1;
    #print self.num;
    # initialize variables
    bestScore = 0;
    currentScore = 0;
    opColor = 0;
    if color == self.BLUE:
      bestScore = -1;
      opColor = self.GREEN;
    else:
      bestScore = 1; 
      opColor = self.BLUE;

    bestX = -1;
    bestY = -1;
    bestMove = -1;
    invaded = list();

    # get all possible moves
    possibleCommando = board.getCommandoPoints();
    possibleM1 = board.getM1Points(color);
    status = board.getStatus();
    # Game has reached terminal state
    # Base case 1
    if status[0] == 1:
      # Blue Wins 
      if status[1] > status[2]:
        bestScore = 1;
      # Blue Loses
      elif status[1] < status[2]:
        bestScore = -1;
      # Draw
      else:
        bestScore = 0;
    # Stopped expansion on a non terminal state
    # Use evaluation function
    # Base case 2
    elif depth == 0:
      bestScore = self.evalFn(board);
    # Not at base case, recursive call to minimax
    else:
      # Find best commandoPara move
      for commandoMove in possibleCommando:
        board.commandoParaDrop(color, commandoMove[0], commandoMove[1]);
        result = self.minimax(board, depth - 1, opColor);
        currentScore = result[3];
        # player is maximizer
        if color == self.BLUE:
          if currentScore >= bestScore:
            bestScore = currentScore;
            bestX = commandoMove[0];
            bestY = commandoMove[1];
            bestMove = 0;
        # player is minimizer
        else:
          if currentScore <= bestScore:
            bestScore = currentScore;
            bestX = commandoMove[0];
            bestY = commandoMove[1];
            bestMove = 0;
        board.occupant[commandoMove[1]][commandoMove[0]] = 0
      # find best possible M1blitz move
      for m1Move in possibleM1:
        invades = board.m1DeathBlitz(color, m1Move[0], m1Move[1], invaded);
        # only consider M1 if its effect is different from commando
        if invades is True:
          self.num = self.num + 1;
          result = self.minimax(board, depth - 1, opColor);
          currentScore = result[3];
          # player is maximizer
          if color == self.BLUE:
            if currentScore >= bestScore:
              bestScore = currentScore;
              bestX = m1Move[0];
              bestY = m1Move[1];
              bestMove = 1;
          # player is minimizer
          else:
            if currentScore <= bestScore:
              bestScore = currentScore;
              bestX = m1Move[0];
              bestY = m1Move[1];
              bestMove = 1;

          board.occupant[m1Move[1]][m1Move[0]] = 0
          for invadeCoord in invaded:
            board.occupant[invadeCoord[1]][invadeCoord[0]] = opColor;



    # populate return array
    ret = list();
    ret.append(bestX); # index 0
    ret.append(bestY); # index 1
    ret.append(bestMove); # index 2
    ret.append(bestScore); # index 3

    return ret;






#def main():
  #p = MinimaxPlayer(1)
  #b = board("./game_boards/Keren.txt")
  #b.printBoard();
  #b.m1DeathBlitz(1,3,5)
  #points = b.getM1Points(1)
  #p.minimax(b,4,1);



#main();






