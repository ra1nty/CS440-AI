class classifier:
  wordDict = list();
  # estimation model: 
  #   1 -- Multinomial Bayes
  #   2 -- Bernoulli Bayes
  model = 0;
  # total number of words in each doctype
  type1Size = 0;
  type2Size = 0;
  # vocab of words for Laplacian Smoothing 
  vocab = 0;
  #P(class) will always be 0.5 in this case since 
  PCLASS = 0.5;


  # Constructor for classfier
  # INPUTS -- filename: name of training file
  #           model: multinomial(1) or bernoulli(2)
  #           type: spam(0) or movie(1)
  # OUTPUTS  -- NONE

  def __init__(self, filename, model, parseType):
    if model == 1:
      self.wordDict = self.trainMultinomial(filename, parseType);
    else:
      self.wordDict = self.trainBernoulli(filename);

    print self.wordDict;


    self.model = model;



  # parses and trains values for Multinomial Bayes Model
  # INPUTS -- filename: name of training file
  #           parsetype: Spam(0) or Movie(1)
  # OUTPUTS -- list of dictionaries 
  #             index 0 :dictionary for type 1(positive review or spam)
  #             index 1 : dictionary for type 2(negative review or not spam)
  #             dictionary has following format:
  #               {word: string , count: integer}
  def trainMultinomial(self, filename, parsetype):
    if parsetype == 0:
      TYPE1 = '1';
      TYPE2 = '0';
    else:
      TYPE1 = '1';
      TYPE2 = '-1';

    # parse file first
    with open(filename, 'r') as f:
      temp = f.read();

    retList = list();
    dict1 = dict();
    dict2 = dict();
    docList = temp.split('\n');
    for doc in docList:
      words = doc.split(' ');
      docType = words[0];
      words.pop(0);
      if docType == TYPE1:
        for word in words:
          self.vocab += 1;
          info = word.split(':');
          if dict1.get(info[0], -1) == -1:
            dict1[info[0]] = int(info[1]);
          else:
            dict1[info[0]] += int(info[1]);
          self.type1Size += int(info[1]);
      elif docType == TYPE2:
        for word in words:
          self.vocab += 1;
          info = word.split(':');
          if dict2.get(info[0], -1) == -1:
            dict2[info[0]] = int(info[1]);
          else:
            dict2[info[0]] += int(info[1]);
          self.type2Size += int(info[1]);

    retList.append(dict1);
    retList.append(dict2);
    return retList;

  def trainBernoulli(self, filename):

    return 0;


  

  # classifies files
  # INPUTS -- testfile: the file to be classified
  # OUTPUTS -- accuracy
  def classifyMultinomial(self, testFile, parseType):
    if parseType == 0:
      TYPE1 = '1';
      TYPE2 = '0';
    else:
      TYPE1 = '1';
      TYPE2 = '-1';

    solutionList = list();
    classifyList = list();
    wordList = list();
    with open(testFile, 'r') as f:
      temp = f.read();
    
    # parse doc into a dictionary of word counts, and accumulate the solution
    docList = temp.split('\n');
    for doc in docList:
      words =  doc.split(' ');
      solution = words[0];
      words.pop(0);
      solutionList.append(solution);
      for word in words:
        info =  word.split(':');
        wordList.append(info[0]);
      probT1 = self.calculateMultiBayes(wordList,0);
      probT2 = self.calculateMultiBayes(wordList,1);
      if probT1 > probT2:
        classifyList.append(TYPE1);
      else:
        classifyList.append(TYPE2);
      del wordList[:];




    return 0;

  def calculateMultiBayes(self, wordList, type):
    for testWord in wordList:
      self.wordDict[0].get(testWord,1);





    return 0;







def main():
  c = classifier("sentiment/rt-train.txt", 1,1);
  accuracy = c.classifyMultinomial("sentiment/rt-test.txt",1);


main();

