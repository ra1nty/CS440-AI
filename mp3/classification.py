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


    def train(self, trainingImages, trainingLabels):
        labels = open(trainingLabels, 'r').read()
        images = open(trainingImages, 'r')

        labels = labels.split('\n')

        counter = 0
        representation = [0] * self.__imageN * self.__imageN

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

        images.close()
        self.smoothing()
        self.totalPixels = self.countPixels()

    def countPixels(self):
        count = 0
        totalPixels = dict()

        for idx, representation in self.likelyhoods.iteritems():
            for i in range(0, self.__imageN * self.__imageN):
                count += representation[i]
            totalPixels[idx] = count
            count = 0

        return totalPixels

    def smoothArr(self, arr):
        constant = 1

        for i in range(0, self.__imageN * self.__imageN):
            arr[i] += constant

        return arr

    def smoothing(self):
        constant = 1
        self.totalImages = 0

        for idx in self.likelyhoods.keys():
            for i in range(0, self.__imageN * self.__imageN):
                self.likelyhoods[idx][i] += constant
            self.classNum[idx] += constant * self.classNum[idx]
            self.totalImages += self.classNum[idx]

    def test(self, testImages, testLabels):
        images = open(testImages, 'r')
        labels = open(testLabels, 'r').read().split('\n')

        self.confusionMatrix = [[0] * len(self.likelyhoods.keys())] * len(self.likelyhoods.keys())

        counter = 0
        representation = [0] * self.__imageN * self.__imageN
        accuracy = 0
        total = 0

        for line in images:

            for i in range(0, self.__imageN):
                if not line[i] == ' ':
                    representation[counter * self.__imageN + i] += 1
            counter += 1

            if counter == self.__imageN:
                counter = 0

                testing = [0] * len(self.likelyhoods.keys())

                for idx, posterior in self.likelyhoods.iteritems():
                    Pclass = self.classNum[idx] / (self.totalImages + 0.0)
                    PixelP = [0] * self.__imageN * self.__imageN

                    for i in range(0, self.__imageN * self.__imageN):
                        if representation[i] == 1:
                            PixelP[i] = posterior[i]/(self.classNum[idx] + 0.0)
                        else:
                            PixelP[i] = (self.classNum[idx] - posterior[i])/(self.classNum[idx] + 0.0)

                    # P(x | e) maxSetOf P(e | x) * P(x)
                    testing[idx] = math.log(Pclass, 2)

                    for i in range(0, self.__imageN * self.__imageN):
                        testing[idx] += math.log(PixelP[i])

                representation = self.smoothArr(representation)

                maximum = -999999999999999
                idx = 0

                for i in range(0, len(testing)):
                    if testing[i] > maximum:
                        maximum = testing[i]
                        idx = i

                actual = int(labels.pop(0))
                if idx == actual:
                    accuracy += 1
                else:
                    self.confusionMatrix[idx][actual] += 1

                for i in range(0, self.__imageN * self.__imageN):
                    self.likelyhoods[actual][i] += representation[i]

                self.classNum[actual] += 1
                self.totalImages += 1
                total += 1

                representation = [0] * self.__imageN * self.__imageN

        print "Accuracy " + str(accuracy/(total + 0.0))
        return self.confusionMatrix

if __name__ == "__main__":
    c = Classifier()
    c.train('./digitdata/trainingimages', './digitdata/traininglabels')
    cMatrix = c.test('./digitdata/testimages', './digitdata/testlabels')

    for row in cMatrix:
        print row


