import numpy
import math
import pdb

class digitClassifier:
  BLACK  = '#';
  GRAY = '+';
  WHITE = ' ';

  NUM_EPOCHS = 3;
  BIAS = None;
  MAX_VECTOR = 10;
  MIN_VECTOR = 0;
  IMG_HEIGHT = 28;
  IMG_WIDTH = 28;
  IMG_AREA = IMG_WIDTH * IMG_HEIGHT;

  WEIGHT_INIT = 0;
  vectors = list();
  numEachClass = [0] * 10;
  correctClassifications = [0] * 10;
  confusionMatrix = list();
  iteration = 0;

  def __init__(self, trainingData, trainingLabel, testingData, testingLabel, epochs, bias= None):
    self.BIAS = bias;
    # initialize weights of vector all to zero
    for x in range(self.MIN_VECTOR, self.MAX_VECTOR):
      temp = list();
      for y in range(0, self.IMG_AREA):
        temp.append(float(self.WEIGHT_INIT));
      self.vectors.append(temp);
      temp = [];
    self.NUM_EPOCHS = epochs

    print "Training Results \n";
    accuracyTrain = self.trainPerceptron(trainingData, trainingLabel, self.vectors);
    print;

    print "Testing \n";
    accuracyTest = self.testPerceptron(testingData,testingLabel, self.vectors);
    for line in self.confusionMatrix:
      del line [:];
    del self.confusionMatrix [:];
    #self.confusionMatrix = list();
    del self.vectors[:];
    self.vectors = list();
    del self.numEachClass[:];
    self.numEachClass = [0] * 10;

  # trains perceptron algorithms
  def trainPerceptron(self, data, labels, vectors):
    trainData= open(data, 'r').read();
    trainLabels = open(labels, 'r').read();
    solutions = trainLabels.split('\n');
    for x in range(0, self.NUM_EPOCHS):
      print x + 1; 
      acc = self.epoch(trainData, solutions, vectors, False);
      print acc;
      self.iteration += 1; 
    self.iteration =  0;
    return acc;

  def testPerceptron(self, data, labels, vectors):
    # initialize confusion matrix
    temp = list();
    for i in range(0, 10):
      for j in range(0,10):
        temp.append(0);
      self.confusionMatrix.append(temp);
      temp = [];


    testData= open(data, 'r').read();
    testLabels = open(labels, 'r').read();
    solutions = testLabels.split('\n');
    acc = self.epoch(testData, solutions, vectors, True);

    print "accuracy";
    print acc;
    print "confusion matrix";
    for line in self.confusionMatrix:
      print line;

    #print "digit accuracies";
    #print self.correctClassifications;
    #print self.numEachClass;
    return 0;

  # unit for 1 round of testing all characters
  def epoch(self, data, solutions, vectors, test):
    representation = list();
    counter = 0;
    correct = 0;
    lines = data.split('\n');
    for i in range(0, len(lines)):
      representation.append(lines[i]);
      if len(representation) == self.IMG_HEIGHT:
        F = self.parseInput(representation);
        representation = [];
        if self.classifyInput(F, int(solutions[counter]), vectors, test):
          correct += 1;
        counter += 1;
    retList = list();
    retList.append(correct);
    retList.append(counter);
    return retList;

  # parses characters into an array of 1s and 0s
  def parseInput(self,representation):
    ret = list();
    for i in range(0, self.IMG_HEIGHT):
      for j in range(0, self.IMG_WIDTH):
        if representation[j][i] == self.WHITE:
          ret.append(float(0));
        else:
          ret.append(float(1));
    return ret;

  def classifyInput(self, F, solution, vectors, test):
    bias = self.BIAS;
    #if test:
      #self.numEachClass[solution] += 1;
    args = list();
    for i in range(self.MIN_VECTOR, self.MAX_VECTOR):
      if bias is not None:
        if i == bias:
          #print numpy.dot(vectors[i],F);
          args.append(numpy.dot(vectors[i],F) + 28);
        else:
          args.append(numpy.dot(vectors[i],F));
      else:
        args.append(numpy.dot(vectors[i],F));
    decision = args.index(max(args));
    # update confusion matrix
    if test:
      self.confusionMatrix[decision][solution] += 1;
    # update weights
    if not decision == solution:
      if not test:
        self.updateWeights(decision, solution, F, vectors);
      return False;
    else:
      if test:
        self.correctClassifications[solution] += 1;
      return True;



    return 0;
  # updates weights based on outcome of each test example
  def updateWeights(self, guess, solution, F, vectors):
    # learning decay rate
    a = float(1)/(1+ self.iteration);
    b = float(1000)/(1000 + self.iteration);
    temp = [x * a for x in F];
    
    for i in range (0, len(F)):   
      vectors[guess][i] = vectors[guess][i] - temp[i];
      vectors[solution][i] = vectors[solution][i] + temp[i];

    return 0;






def main():
  DATATEST = "./digitdata/testimages";
  LABELTEST = "./digitdata/testlabels";
  DATATRAIN = "./digitdata/trainingimages";
  LABELTRAIN = "./digitdata/traininglabels";
  #Control Testing
  # print "Epochs"
  # print "3 epochs";
  # print "No bias";
  # print "1/(t+1) Learning rate";
  # print "All weights initialized to 0";
  # print "++++++++++++++++++++++++++++++++++++++";
  # print;
  # d = digitClassifier(DATATRAIN, LABELTRAIN, DATATEST, LABELTEST);

  # Epoch testing 
  # print "Epoch";
  # print "No bias";
  # print "1/(t+1) Learning rate";
  # print "All weights initialized to 0";
  # print "++++++++++++++++++++++++++++++++++++++";
  # i = 4;
  # while i in range(4, 10):
  #   print str(i) + " Epochs";
  #   print "++++++++++++++++++++++++++++++++++++++";
  #   d = digitClassifier(DATATRAIN, LABELTRAIN, DATATEST, LABELTEST, i, None);
  #   print;
  #   i +=3;

  #Bias Testing
  print "Bias"
  print "3 Epochs"
  print "1/(t+1) Learning rate"
  print "all weights initialized to 0" 
  print "++++++++++++++++++++++++++++++++++++++";

  #for i in range(0, 9):
  print "Bias on 9 " ;
  print "++++++++++++++++++++++++++++++++++++++";
  d = digitClassifier(DATATRAIN, LABELTRAIN, DATATEST, LABELTEST, 3, 9);







main();