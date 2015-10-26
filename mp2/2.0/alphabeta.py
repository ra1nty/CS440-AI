import copy
from board import board
from node import stateNode
from decimal import Decimal


class AlphaBeta:
  BLUE = 1
  GREEN = 2
  color = 0
  Nodes = 0
  moves = 0

  def __init__(self, color):
    self.color = color;

  def generateMove(self, curGame):
    self.moves += 1
    move = self.alphabeta(curGame, 5, self.color,0,Decimal('-Infinity'),Decimal('Infinity'));
    ret =  list();
    ret.append(move[2]);
    ret.append(move[0]);
    ret.append(move[1]);
    ret.append(self.color);

    return ret;


  def evalFn(self, board):
    status = board.getStatus();
    maxScore = status[1] + status[2];

    ret = float((status[1] - status[2])/maxScore);
    #print ret;
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
  def alphabeta(self, board, depth, color, index, alpha, beta):
    self.Nodes = self.Nodes + 1;
    #print self.num;
    # initialize variables
    bestScore = 0;
    currentScore = 0;
    opColor = 0;
    alpha = alpha
    beta = beta
    if color == self.BLUE:
      bestScore = -1
      opColor = self.GREEN

    else:
      bestScore = 1
      opColor = self.BLUE

    bestX = -1
    bestY = -1
    bestMove = -1
    invaded = list()

    #check status
    Commando = board.getCommandoPoints()
    M1 = board.getM1Points(color)
    status = board.getStatus()
    if status[0] == 1:
      # Blue Wins
      if status[1] > status[2]:
        bestScore = 1
      # Blue Loses
      elif status[1] < status[2]:
        bestScore = -1
      # Draw
      else:
        bestScore = 0

    # get all possible moves


    # Game has reached terminal state
    # Base case 1

    # Stopped expansion on a non terminal state
    # Use evaluation function
    # Base case 2
    elif depth == 0:
      bestScore = self.evalFn(board)
    # Not at base case, recursive call to minimax
    else:
      # looping through commando
      for commandoMove in Commando:
        board.commandoParaDrop(color, commandoMove[0], commandoMove[1])
        result = self.alphabeta(board, depth - 1, opColor, index, alpha, beta)
        currScore = result[3]
        # MAX PLAYER
        if color == self.BLUE:
          if currScore > alpha:
            alpha = currScore
            bestScore = currScore
            bestX = commandoMove[0]
            bestY = commandoMove[1]
            bestMove = 0
        # player is minimizer
        else:
          if currScore < beta:
            beta = currScore
            bestScore = currScore
            bestX = commandoMove[0]
            bestY = commandoMove[1]
            bestMove = 0
        board.occupant[commandoMove[1]][commandoMove[0]] = 0
        if alpha >= beta:
            break

      # find best possible M1blitz move
      for m1Move in M1:
        invades = board.m1DeathBlitz(color, m1Move[0], m1Move[1], invaded)
        # only consider M1 if its effect is different from commando
        if invades is True:
          result = self.alphabeta(board, depth - 1, opColor, index, alpha, beta)
          currScore = result[3]
          # player is maximizer
          if color == self.BLUE:
            if currScore > alpha:
              alpha = currScore
              bestScore = currScore
              bestX = m1Move[0]
              bestY = m1Move[1]
              bestMove = 1
          # player is minimizer
          else:
            if currScore < beta:
              beta = currScore
              bestScore = currScore
              bestX = m1Move[0]
              bestY = m1Move[1]
              bestMove = 1
          board.occupant[m1Move[1]][m1Move[0]] = 0
          for invadeCoord in invaded:
            board.occupant[invadeCoord[1]][invadeCoord[0]] = opColor;
        if alpha >= beta:
          break


    # populate return array
    ret = list()
    ret.append(bestX) # index 0
    ret.append(bestY) # index 1
    ret.append(bestMove) # index 2
    ret.append(bestScore) # index 3
    #print depth;
    #print ret;

    return ret;

