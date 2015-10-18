from board import board
from node import stateNode

class playerMiniMax:
  BLUE = 1;
  GREEN = 2;
  color = 0;
  COMMANDO = 3;
  M1 = 4;
  board;
  def __init__(self, color, board):
    self.color = color;
    self.board = board;

  def generateTree(depth):
    root = stateNode(board);
    generateChildren(root);




  def generateTreeRecursive(curNode, curDepth, finalDepth, method, color):
    status = curNode.data.getStatus();

    # base case: terminal node or hit final depth
    # calculate depth and return
    if curNode.isTerminal() or curDepth == finalDepth:
      if curNode.isTerminal():
        curNode.utility = 1;
      elif curDepth == finalDepth:
        curNode.utility = calculateEval(node);
      return curNode;
    else:




  



  def calculateEval(node):







def main():




main();






