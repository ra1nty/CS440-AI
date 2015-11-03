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

if __name__ == "__main__":
    c = Classifier()
    c.train('./digitdata/trainingimages', './digitdata/traininglabels')
    cMatrix = c.test('./digitdata/testimages', './digitdata/testlabels')

    i = 0
    for row in cMatrix:
        print i,
        print row
        i += 1


