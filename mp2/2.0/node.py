from board import board

class stateNode():
  children = [];
  utility = 0;

  def __init__(self, board, color):
    self.data = board;
    self.children = [];
    self.color = color;
    self.utility = 0;


  def addChild(self, obj):
    self.children.append(obj);

  def isTerminal(self):
    status = self.data.getStatus();
    if status[0] == 1:
      return True;
    else:
      return False;
  def setUtility(self, val):
    self.utility = val;

  def getNodeStatus(self):
    return self.data.getStatus();
  
  def generateChildre(self):
    print; 