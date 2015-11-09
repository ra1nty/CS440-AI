class classifier:
  wordDict = list();
  # estimation model: 
  #   1 -- Multinomial Bayes
  #   2 -- Bernoulli Bayes
  model = 0;


  # Constructor for classfier
  # INPUTS -- filename: name of training file
  #           model: multinomial(1) or bernoulli(2)
  #           type: spam(0) or movie(1)
  # OUTPUTS  -- NONE

  def __init__(self, filename, model, type):
    if model == 1:
      self.wordDict = self.trainMultinomial(filename,1);
      print self.wordDict[0];
      print;
      print self.wordDict[1];
    else:
      self.wordDict = self.trainBernoulli(filename);

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
          info = word.split(':');
          dict1[info[0]] = int(info[1]);
      elif docType == TYPE2:
        print "TYPE2"
        for word in words:
          info = word.split(':');
          dict2[info[0]] = int(info[1]);

    retList.append(dict1);
    retList.append(dict2);
    return retList;

  def trainBernoulli(self, filename):

    return 0;

  # parses file into dictionary
  # INPUTS -- filename: the file to be parsed
  # OUTPUTS -- ret: dictionary of parsed words
  def __parseFile(self, filename):

    return dict();

  

  # classifies files
  # INPUTS -- testfile: the file to be classified
  # OUTPUTS -- array of solutions
  def classifyMultinomial(self, testFile):
    return 0;







def main():
  c = classifier("sentiment/rt-train.txt", 1,1);

main();

