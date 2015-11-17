from math import log
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
      self.wordDict = self.trainBernoulli(filename, parseType);
    top20a = sorted(self.wordDict[0], key=self.wordDict[0].get);
    top20a = list(reversed(top20a));
    print top20a[0:20];
    top20b = sorted(self.wordDict[1], key=self.wordDict[1].get);
    top20b = list(reversed(top20b));
    print top20b[0:20];
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
    top20a = sorted(dict1, key=dict1.get);
    top20a = list(reversed(top20a));

    top20b = sorted(dict2, key=dict2.get);
    top20b =  list(reversed(top20b));

    if parsetype == 0:
      print "top 20 spam words";
    else:
      print "top 20 positive movie reviews words";
    print top20a[0:20];
    if parsetype == 0:
      print "top 20 not spam words";
    else:
      print "top 20 negative movie reviews words";
    print top20b[0:20];
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
    numDocs = 0;

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
      #print probT1;
      #print probT2;
      #print;
      if probT1 > probT2:
        classifyList.append(TYPE1);
      else:
        classifyList.append(TYPE2);
      del wordList[:];

    idx = 0;
    correct1 = 0;
    correct2 = 0;
    wrong1 = 0;
    wrong2 = 0;

    for guess in classifyList:
      if guess == solutionList[idx]:
        if guess == TYPE1:
          correct1 +=1;
        else:
          correct2 += 1;
      else:
        if guess == TYPE1:
          wrong1 +=1;
        else:
          wrong2 +=1;
      idx += 1; 

    print "confusion"
    print correct1;
    print correct2;
    print wrong1;
    print wrong2;
    return float(correct1 + correct2) / idx;

  def trainBernoulli(self, filename, parseType):
      if parseType == 0:
        TYPE1 = '1';
        TYPE2 = '0';
      else:
        TYPE1 = '1';
        TYPE2 = '-1';

      with open(filename, 'r') as file:
        temp = file.read()

      list_ret = list()
      dict1= dict()
      dict2= dict()
      doclist = temp.split('\n')
      for document in doclist:

        words = document.split(' ')
        document_type = words[0]
        words.pop(0)
        if document_type == TYPE1:
          for word in words:
            info = word.split(':')
            if dict1.get(info[0], -1) == -1:
              dict1[info[0]] = 1
            else:
              dict1[info[0]] += 1
          self.type1Size += 1
        elif document_type == TYPE2:
          for word in words:
            info = word.split(':')
            if dict2.get(info[0], -1) == -1:
              dict2[info[0]] = 1
            else:
              dict2[info[0]] += 1
          self.type2Size += 1

      print "dict1:", len(dict1)
      print "dict2:",len(dict2)
      list_ret.append(dict1)
      list_ret.append(dict2)
      print "list_ret:",len(list_ret)
      return list_ret

  def classifyBernoulli(self, testFile, parseType):
    if parseType == 0:
      TYPE1 = '1';
      TYPE2 = '0';
    else:
      TYPE1 = '1';
      TYPE2 = '-1';
    numDocs = 0;

    solution = list()
    classify = list()
    wordlist = list()
    with open(testFile, 'r') as file:
      temp = file.read()

    doclist = temp.split('\n')
    for doc in doclist:
      words = doc.split(' ')
      answer = words[0]
      words.pop(0)
      solution.append(answer)
      for word in words:
        info = word.split(':')
        wordlist.append(info[0])
      #print "wordlist:",len(wordlist)
      probtype1 = self.calculateBernoulli(wordlist,0)
      probtype2 = self.calculateBernoulli(wordlist,1)
      if probtype1 > probtype2 :
        classify.append(TYPE1)
      else:
        classify.append(TYPE2)
      del wordlist[:]
      #print "solution", len(solution)
    i = 0
    correct = 0
    for guess in classify:
      if guess == solution[i]:
        correct += 1
      i += 1
    return float (correct)/i

  def calculateMultiBayes(self, wordList, docType):
    ret = 1;
    for testWord in wordList:
      numerator = self.wordDict[docType].get(testWord, 0);
      numerator += 1;
      if docType == 0:
        denominator = self.vocab + self.type1Size;
      else:
        denominator = self.vocab + self.type2Size;
      ret += log(float(numerator)/denominator);
      print ret;


    return float(ret);
  def printWords(self):
    for k in self.wordDict[0]:
      i = 0;
      #print k;
      for i in range(1, self.wordDict[0].get(k)):
        print k;
    return 0;
  
  def calculateBernoulli(self,wordlist,doctype):
    ret = 1;
    for testword in wordlist:
      numerator = self.wordDict[doctype].get(testword,-3)
      if numerator == -3:
        if doctype == 0:
          denominator = self.type1Size
        else:
          denominator = self.type2Size
        ret += log(float(1.0)-(float(1.0)/(denominator+2)))
      else:
        if doctype == 0:
          denominator = self.type1Size
        else:
          denominator = self.type2Size
        ret += log(float(numerator+1)/(denominator+2))
    return float(ret)



def main():
  # print;
  # c = classifier("sentiment/rt-train.txt", 1,1);
  # accuracy = c.classifyMultinomial("sentiment/rt-test.txt",1);
  # print "accuracy"
  # print accuracy;
  # print;
  # c = classifier("spam_detection/train_email.txt", 1,0);
  # c.printWords();

  # accuracy = c.classifyMultinomial("spam_detection/test_email.txt",0);
  # print "accuracy"
  # print accuracy;



  #c = classifier("sentiment/rt-train.txt", 2,1);
 # accuracy = c.classifyBernoulli("sentiment/rt-test.txt",1);
 # print "sentiment:",accuracy;
  c = classifier("spam_detection/train_email.txt", 2,0);
  #accuracy = c.classifyBernoulli("spam_detection/test_email.txt",0);
  #print "detection:",accuracy;  



main();

