import math
import os
import sys
import pdb

class Classifier:

    edge = '+'
    body = '#'
    __imageN = 28

    def __init__(self):

        self.likelyhoods = dict()
        self.classNum = dict()

        for i in range(0, 10):
            temp = [0] * self.__imageN * self.__imageN
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

    def train(self, trainingImages, trainingLabels):
        labels = open(trainingLabels, 'r').read()
        images = open(trainingImages, 'r')

        labels = labels.split('\n')

        counter = 0
        representation = [0] * self.__imageN * self.__imageN
        self.totalImages = 0

        for line in images:
            for i in range(0, self.__imageN):
                if not line[i] == ' ':
                    representation[counter * self.__imageN + i] += 1

            counter += 1

            if counter == self.__imageN:
                counter = 0
                nextNum = int(labels.pop(0))
                self.classNum[nextNum] += 1

                # Add it up
                for i in range(0, self.__imageN * self.__imageN):
                    self.likelyhoods[nextNum][i] += representation[i]

                # Reset the representation array
                representation = [0] * self.__imageN * self.__imageN
                self.totalImages += 1

        images.close()
        self.smoothing()
        self.totalPixels = self.countPixels()

    def retrain(self, trainingImages, trainingLabels):
        self.likelyhoods = dict()
        self.classNum = dict()

        for i in range(0, 10):
            temp = [0] * self.__imageN * self.__imageN
            self.likelyhoods[i] = temp
            self.classNum[i] = 0

        self.train(trainingImages, trainingLabels)

    def generateIndex(self, x, y):
        return y * self.__imageN + x

    def chainRule(self, jointProbabilities):
        pass

    def testRelaxed(self, trainingImages, trainingLabels, n, m):
        images = open(trainingImages, 'r')
        labels = open(trainingLabels, 'r').read().split('\n')

        counter = 0
        representation = [0] * self.__imageN * self.__imageN
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

                for idx, posterior in self.likelyhoods.iteritems():
                    temp = list()
                    lidx = 0

                    for y in range(0, self.__imageN, m):
                        for x in range(0, self.__imageN, n):

                            jointProbabilities = list()
                            for yi in range(0, m):
                                for xi in range(0, n):
                                    jointProbabilities.append(self.generateIndex(xi + x, yi + y))

                            PFeature = ()
                            for probability in jointProbabilities:
                                PFeature = PFeature + (posterior[probability]/(0.0 + self.classNum[idx]),)

                            temp.append(PFeature)

                    featureSets[idx] = temp

                temp = list()
                for y in range(0, self.__imageN, m):
                    for x in range(0, self.__imageN, n):

                        jointProbabilities = list()
                        for yi in range(0, m):
                            for xi in range(0, n):
                                jointProbabilities.append(self.generateIndex(xi + x, yi + y))

                        PFeature = ()
                        for probability in jointProbabilities:
                            PFeature = PFeature + (representation[probability],)

                        temp.append(PFeature)

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
            for i in range(0, self.__imageN * self.__imageN):
                count += representation[i]
            totalPixels[idx] = count
            count = 0

        return totalPixels

    constant = 1

    def smoothArr(self, arr, classNum):
        constant = self.constant

        for i in range(0, self.__imageN * self.__imageN):
            arr[i] += constant

        self.classNum[classNum] += constant
        self.totalImages += constant

        return arr

    def smoothing(self):
        constant = self.constant
        self.totalImages = 0

        for idx in self.likelyhoods.keys():
            for i in range(0, self.__imageN * self.__imageN):
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
        images = open(testImages, 'r')
        labels = open(testLabels, 'r').read().split('\n')
        self.confusionMatrix = list()

        """
        Create the confusion matrix as an NxN array
        """

        for i in range(0, len(self.likelyhoods.keys())):
            temp = [0] * len(self.likelyhoods.keys())
            self.confusionMatrix.append(temp)

        counter = 0
        representation = [0] * self.__imageN * self.__imageN
        accuracy = 0
        total = 0
        classClassified = [0] * self.__imageN

        """
        Go through the image file line by line
        """
        for line in images:

            # if the line is not the end of an image
            for i in range(0, self.__imageN):
                if not line[i] == ' ':
                    representation[counter * self.__imageN + i] += 1

            # When counter is equal to the size of an image we can try to classify it
            counter += 1

            if counter == self.__imageN:
                counter = 0

                testing = [0] * len(self.likelyhoods.keys())

                # Go through the learned likelyhoods and create the naive bayes probability
                for idx, posterior in self.likelyhoods.iteritems():
                    Pclass = self.classNum[idx] / (self.totalImages + 0.0)
                    PixelP = [0] * self.__imageN * self.__imageN

                    # For each pixel calculate the probability
                    for i in range(0, self.__imageN * self.__imageN):
                        if representation[i] == 1:
                            PixelP[i] = posterior[i]/(self.classNum[idx] + 0.0)
                        else:
                            PixelP[i] = (self.classNum[idx] - posterior[i])/(self.classNum[idx] + 0.0)

                    # P(x | e) maxSetOf P(e | x) * P(x)
                    testing[idx] = math.log(Pclass, 2)

                    for i in range(0, self.__imageN * self.__imageN):
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
                else:
                    self.confusionMatrix[actual][idx] += 1


                """
                Use the new data and learn from it to improve the future results
                (Not sure if we should do this but this brought the accuracy up to around 70%)
                """

                for i in range(0, self.__imageN * self.__imageN):
                    self.likelyhoods[actual][i] += representation[i]

                self.classNum[actual] += 1
                self.totalImages += 1

                representation = [0] * self.__imageN * self.__imageN
                total += 1

        # The accuracy of the predictions
        print "Accuracy " + str(accuracy/(total + 0.0))

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
                    for pixel in range(0, self.__imageN * self.__imageN):
                        if j == 2:
                            f.write(str(math.log(toPrint[j][pixel], 2)) + ' ')
                        else:
                            f.write(str(math.log(toPrint[j][pixel]/(0.0 + self.classNum[maxConfusion[i][j]]), 2)) + ' ')
                    f.write('\n')

    def __oddRatio(self, believed, actual, pixel):
        first = 0.0
        second = 0.0

        first = self.likelyhoods[believed][pixel]/(self.classNum[believed] + 0.0)
        second = self.likelyhoods[actual][pixel]/(self.classNum[actual] + 0.0)

        return first/second

if __name__ == "__main__":
    c = Classifier()
    c.train('./digitdata/trainingimages', './digitdata/traininglabels')
    cMatrix = c.test('./digitdata/testimages', './digitdata/testlabels')

    # Print the confusion matrix
    i = 0
    for row in cMatrix:
        print i,
        print row
        i += 1

    # oddRatios = c.oddRatios(cMatrix)

    n = 2
    m = 2
    c.retrain('./digitdata/trainingimages', './digitdata/traininglabels')
    c.testRelaxed('./digitdata/testimages', './digitdata/testlabels', n, m)

