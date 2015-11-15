import math
import os
import sys
import pdb

class Classifier:

    LEARN = 0
    edge = '+'
    body = '#'
    __imageN = 28
    __imageM = 28

    def __init__(self):

        self.likelyhoods = dict()
        self.classNum = dict()

        for i in range(0, 10):
            temp = [0] * self.__imageN * self.__imageN
            self.likelyhoods[i] = temp
            self.classNum[i] = 0

    def changeToFaces(self):
        self.likelyhoods = dict()
        self.classNum = dict()
        self.__imageN = 70
        self.__imageM = 60

        for i in range(0, 2):
            temp = [0] * self.__imageN * self.__imageM
            self.likelyhoods[i] = temp
            self.classNum[i] = 0


    """
    def train(self, trainingImages, trainingLabels)

    inputs: trainingImages - {String} pathname to the training image set
            trainingLabels - {String} pathname to the training image labels

    outputs: None
    returns: None
    side effects: creates a new dictionary of the likelyhoods of each class (the number) and the
                  number of times the pixel appears (likelyhood)
    """

    def train(self, trainingImages, trainingLabels, relaxed=0, n=0, m=0):
        labels = open(trainingLabels, 'r').read()
        images = open(trainingImages, 'r')

        labels = labels.split('\n')

        counter = 0
        representation = [0] * self.__imageN * self.__imageM
        self.totalImages = 0

        """
        Go through every line in the image
        """
        for line in images:
            for i in range(0, self.__imageM):
                if not line[i] == ' ':
                    representation[counter * self.__imageM + i] += 1

            counter += 1

            """
            End of an image, store the current representation in the frequency table and reset everything
            """
            if counter == self.__imageN:
                counter = 0
                nextNum = int(labels.pop(0))
                if (relaxed):
                    iterator = 0
                    for yO in range(0, self.__imageN, n):
                        for xO in range(0, self.__imageM, m):
                            binary = list()
                            for y in range(0, n):
                                for x in range(0, m):
                                    binary.append(representation[(yO + y) * self.__imageN + (x + xO)])

                            currPow = 0
                            num = 0
                            for b in binary:
                                num += b * pow(2, currPow)
                                currPow += 1
                            if not num == 0:
                                pdb.set_trace()
                            self.likelyhoods[nextNum][num][iterator] += 1
                            iterator += 1
                else:
                    for i in range(0, self.__imageN * self.__imageM):
                        self.likelyhoods[nextNum][i] += representation[i]

                self.classNum[nextNum] += 1

                # Add it up

                # Reset the representation array
                representation = [0] * self.__imageN * self.__imageM
                self.totalImages += 1

        images.close()
        self.smoothing()
        self.totalPixels = self.countPixels()

    """
    Deletes the current trained information and runs through the new training set
    """
    def retrain(self, trainingImages, trainingLabels, relaxed=0, n=0, m=0):
        self.likelyhoods = dict()
        self.classNum = dict()

        for i in range(0, 10):
            if relaxed:
                temp = dict()
                for j in range(0, pow(2, n * m)):
                    temp[j] = [0] * (self.__imageN/n) * (self.__imageM/m)
                self.likelyhoods[i] = temp
            else:
                temp = [0] * self.__imageN * self.__imageM
                self.likelyhoods[i] = temp

            self.classNum[i] = 0

        self.train(trainingImages, trainingLabels, relaxed, n, m)

    def generateIndex(self, x, y):
        return y * self.__imageN + x

    def testRelaxed(self, trainingImages, trainingLabels, n, m):
        images = open(trainingImages, 'r')
        labels = open(trainingLabels, 'r').read().split('\n')

        counter = 0
        representation = [0] * self.__imageN * self.__imageM
        accuracy = 0
        total = 0

        for line in images:

            for i in range(0, self.__imageN):
                if not line[i] == ' ':
                    representation[self.generateIndex(i, counter)] += 1

            counter += 1

            # End of the image, process this
            if counter == self.__imageN:
                featureSets = dict()
                temp = dict()

                for yO in range(0, self.__imageN, n):
                    for xO in range(0, self.__imageM, m):
                        binary = list()
                        for y in range(0, n):
                            for x in range(0, m):
                                binary.append(representation[(yO + y) * self.__imageN + (x + xO)])

                        currPow = 0
                        num = 0
                        for b in binary:
                            num += b * pow(2, currPow)
                            currPow += 1
                        self.likelyhoods[nextNum][binary] += 1

                MAP = dict()
                for idx, features in featureSets.iteritems():
                    probability = self.classNum[idx]/(self.totalImages + 0.0)

                    for j in range(0, len(temp)):
                        masterFeature = features[j]
                        testFeature = temp[j]

                        for i in range(0, len(masterFeature)):
                            if testFeature[i] == 1:
                                probability += math.log(masterFeature[i], 2)
                            else:
                                probability += math.log(1 - masterFeature[i], 2)

                    MAP[idx] = probability

                maximum = -9999999999999.9
                finalIdx = idx

                for idx, p in MAP.iteritems():
                    if p > maximum:
                        maximum = p
                        finalIdx = idx

                actual = int(labels.pop(0))

                if actual == finalIdx:
                    accuracy += 1

                total += 1
                counter = 0

                if self.LEARN:
                    for i in range(0, self.__imageN * self.__imageN):
                        self.likelyhoods[actual][i] += representation[i]

                    self.classNum[actual] += 1
                    self.totalImages += 1

                representation = [0] * self.__imageN * self.__imageN

        print "%f accuracy" % ((accuracy/(total + 0.0)))

    def countPixels(self):
        count = 0
        totalPixels = dict()

        for idx, representation in self.likelyhoods.iteritems():
            for i in range(0, self.__imageN * self.__imageM):
                count += representation[i]
            totalPixels[idx] = count
            count = 0

        return totalPixels

    constant = 1

    """
    Smooth a single array
    """
    def smoothArr(self, arr, classNum):
        constant = self.constant

        for i in range(0, self.__imageN * self.__imageN):
            arr[i] += constant

        self.classNum[classNum] += constant
        self.totalImages += constant

        return arr

    """
    Smooth the likelyhoods, called after the main training function
    """
    def smoothing(self):
        constant = self.constant
        self.totalImages = 0

        for idx in self.likelyhoods.keys():
            for i in range(0, self.__imageN * self.__imageM):
                self.likelyhoods[idx][i] += constant
            self.classNum[idx] += constant * self.classNum[idx]
            self.totalImages += self.classNum[idx]

    """
    def test(self, testImages, testLabels)

    input: testImages - {String} path to the testimages
           testLabels - {String} path to the testlabels

    outputs: Accuracy of the learned data
    returns: Confusion matrix - {List[List * 10]} When they don't match up the percentage of the actual vs predicted
    side effects: Increases the likelyhoods as it learns from the different test images
    """

    def test(self, testImages, testLabels):

        """
        Setup variables
        """
        images = open(testImages, 'r')
        labels = open(testLabels, 'r').read().split('\n')
        self.confusionMatrix = list()
        PHighest = dict()
        PLowest = dict()
        highest = dict()
        lowest = dict()
        classificationRate = dict()
        totalPerDigit = dict()
        currCount = 0

        """
        Initial Setup Code
        """

        for i in range(0, len(self.likelyhoods.keys())):
            PHighest[i] = -9999999999
            PLowest[i] = 9999999999
            classificationRate[i] = 0
            totalPerDigit[i] = 0

        """
        Create the confusion matrix as an NxN array
        """

        for i in range(0, len(self.likelyhoods.keys())):
            temp = [0] * len(self.likelyhoods.keys())
            self.confusionMatrix.append(temp)

        counter = 0
        representation = [0] * self.__imageN * self.__imageM
        accuracy = 0
        total = 0
        classClassified = [0] * self.__imageN

        """
        Go through the image file line by line
        """
        for line in images:

            # if the line is not the end of an image
            for i in range(0, self.__imageM):
                if not line[i] == ' ':
                    representation[counter * self.__imageM + i] += 1

            # When counter is equal to the size of an image we can try to classify it
            counter += 1

            if counter == self.__imageN:
                counter = 0

                testing = [0] * len(self.likelyhoods.keys())

                # Go through the learned likelyhoods and create the naive bayes probability
                for idx, posterior in self.likelyhoods.iteritems():
                    Pclass = self.classNum[idx] / (self.totalImages + 0.0)
                    PixelP = [0] * self.__imageN * self.__imageM

                    # For each pixel calculate the probability
                    for i in range(0, self.__imageN * self.__imageM):
                        """
                        If representation is 1 then do pixels/total
                        otherwise do 1-pixels/total for the likelyhood that it didn't appear there
                        """
                        if representation[i] == 1:
                            PixelP[i] = posterior[i]/(self.classNum[idx] + 0.0)
                        else:
                            PixelP[i] = (self.classNum[idx] - posterior[i])/(self.classNum[idx] + 0.0)

                    # P(x | e) maxSetOf P(e | x) * P(x)
                    testing[idx] = math.log(Pclass, 2)

                    for i in range(0, self.__imageN * self.__imageM):
                        testing[idx] += math.log(PixelP[i], 2)

                """
                Find the maximum value from all the trials and that is the index that we are gonna classify
                This number as
                """
                maximum = -999999999999999
                idx = 0


                for i in range(0, len(testing)):
                    if testing[i] > maximum:
                        maximum = testing[i]
                        idx = i

                actual = int(labels.pop(0))
                classClassified[actual] += 1

                if idx == actual:
                    accuracy += 1
                    classificationRate[actual] += 1
                else:
                    self.confusionMatrix[actual][idx] += 1

                """
                Check if lower or higher than curr lowest/highest and then store
                """
                if testing[actual] < PLowest[actual]:
                    PLowest[actual] = testing[actual]
                    lowest[actual] = list(representation)
                if testing[actual] > PHighest[actual]:
                    PHighest[actual] = testing[actual]
                    highest[actual] = list(representation)

                """
                Use the new data and learn from it to improve the future results
                Increased the accuracy up 1.5%
                """
                if self.LEARN:
                    for i in range(0, self.__imageN * self.__imageM):
                        self.likelyhoods[actual][i] += representation[i]

                    self.classNum[actual] += 1
                    self.totalImages += 1

                representation = [0] * self.__imageN * self.__imageM
                total += 1
                totalPerDigit[actual] += 1

        """
        Output of the function, displays the accuracies of everything
        """
        # The accuracy of the predictions
        print "Accuracy " + str(accuracy/(total + 0.0)) + "\n"

        print "Accuracy per digit"
        for i in range(0, len(self.likelyhoods.keys())):
            print str(i) + " | " + str(float(classificationRate[i]/(totalPerDigit[i] + 0.0)))

        self.exportHighestLowest(PHighest, PLowest, highest, lowest)
        print "  ",
        for i in range(0, len(self.confusionMatrix)):
            print i,
            print "  ",
        print ""

        for i in range(0, len(self.confusionMatrix)):
            for j in range(0, len(self.confusionMatrix[i])):
                self.confusionMatrix[i][j] /= float(classClassified[i])
                self.confusionMatrix[i][j] = round(self.confusionMatrix[i][j], 2)

        return self.confusionMatrix

    def exportHighestLowest(self, PHighest, PLowest, highest, lowest):
        high = open('highest.p', 'w')
        low = open('lowest.p', 'w')

        for i in range(0, len(self.likelyhoods.keys())):
            high.write(str(PHighest[i]) + "\n")
            low.write(str(PLowest[i]) + "\n")
            counter = 0
            for idx in range(0, self.__imageN * self.__imageM):
                high.write(str(highest[i][idx]))
                low.write(str(lowest[i][idx]))
                counter += 1
                if counter % self.__imageN == 0:
                    high.write("\n")
                    low.write("\n")

    def oddRatios(self, confusionMatrix):
        maxConfusion = list()

        for actual in range(0, len(confusionMatrix)):
            for confusion in range(0, len(confusionMatrix[actual])):
                maxConfusion.append((confusion, actual, confusionMatrix[actual][confusion]))

        maxConfusion.sort(key=lambda x : x[2], reverse=True)

        ratios = [0.0] * self.__imageN * self.__imageN
        for i in range(0, 4):
            for pixel in range(0, self.__imageN * self.__imageN):
                ratios[pixel] = self.__oddRatio(maxConfusion[i][0], maxConfusion[i][1], pixel)

            with open("%d_%d.confusion" % (maxConfusion[i][0], maxConfusion[i][1]), 'w') as f:
                toPrint = list()
                toPrint.append(self.likelyhoods[maxConfusion[i][0]])
                toPrint.append(self.likelyhoods[maxConfusion[i][1]])
                toPrint.append(ratios)
                for j in range(0, 3):
                    counter = 0
                    for pixel in range(0, self.__imageN * self.__imageN):
                        toWrite = 0
                        counter += 1
                        if j == 2:
                            toWrite = math.log(toPrint[j][pixel], 2)
                        else:
                            toWrite = toPrint[j][pixel]/(0.0 + self.classNum[maxConfusion[i][j]]) #* self.classNum[maxConfusion[i][j]]/(self.totalImages + 0.0)


                        if j == 2:
                            if toWrite < 0:
                                f.write('-')
                            elif abs(1 - toWrite) < 0.2:
                                f.write('#')
                            else:
                                f.write('+')
                        else:
                            if abs(toWrite) < 0.2:
                                f.write('-')
                            elif abs(toWrite) > 0.35:
                                f.write('+')
                            else:
                                f.write('#')

                        if counter % self.__imageN == 0:
                            f.write("\n")
                    f.write('\n')

    def __oddRatio(self, believed, actual, pixel):
        first = 0.0
        second = 0.0

        first = self.likelyhoods[believed][pixel]/(self.classNum[believed] + 0.0)
        second = self.likelyhoods[actual][pixel]/(self.classNum[actual] + 0.0)

        return first/second

if __name__ == "__main__":
    c = Classifier()
    """
    c.train('./digitdata/trainingimages', './digitdata/traininglabels')
    cMatrix = c.test('./digitdata/testimages', './digitdata/testlabels')

    # Print the confusion matrix
    i = 0
    for row in cMatrix:
        print i,
        print row
        i += 1

    oddRatios = c.oddRatios(cMatrix)

    print "\n\n\n"

    c.changeToFaces()
    c.train('./facedata/facedatatrain', './facedata/facedatatrainlabels')
    cMatrix = c.test('./facedata/facedatatest', './facedata/facedatatestlabels')

    i = 0
    for row in cMatrix:
        print i,
        print row
        i += 1

    """
    c.retrain('./digitdata/trainingimages', './digitdata/traininglabels', 1, 2, 2)
    c.testRelaxed('./digitdata/testimages', './digitdata/testlabels', 2, 2)

