import sys
import string
import math
import re

#############################################################
# Class to create bayes data. That is, the vocabulary and
#  the feature vectors. This is done by sending a file object
#  to createVocab(), and then to createFeatureVecs()
#############################################################
class BayesData(object):
    """docstring for BayesData."""
    def __init__(self, vocabulary=None, features=None):
        super(BayesData, self).__init__()
        self.vocabulary = vocabulary if vocabulary is not None else list()
        self.featureVecs = features if features is not None else list()


    #############################################################
    # Prints the data comma seperated to a files
    # Data is a list []
    #############################################################
    def printFeatsToFile(self, fileName):
        try:
            fp = open(str(fileName), "w")
            commaSeperated = ','.join(self.vocabulary)
            fp.write(commaSeperated + ",classlabel\n")

            for vector in self.featureVecs:
                # turn all numbers in the vector to strings via map()
                commaSeperated = ','.join(map(str,vector))
                fp.write(commaSeperated+ "\n")
            fp.close()
        except:
            print("Error opening file named " + str(fileName) + " for writing")
            return

    #############################################################
    # Strips all punctuation, special characters, and numbers
    #  and converts all letters to lowercase
    #############################################################
    def cleanSentence(self, line):
        regEscapes = re.compile('[.!?@#$%^&*():;/,\\\<>\{\}\[\]+=\-_~`\'1234567890]')
        return regEscapes.sub(r'', line.lower())

    #############################################################
    # Given a string, the string is stripped and converted to
    #  lower case. Then each word is added to the vocabulary if
    #  it is not already in it.
    #############################################################
    def __addToVocab(self, sentence):
        # clean string then turn it into a list
        cleanStr = self.cleanSentence(sentence).split()
        for word in cleanStr:
            if word not in self.vocabulary:
                self.vocabulary.append(word)

    #############################################################
    # Given a file pointer, createVocab() adds each line to
    #  the vocabulary
    #############################################################
    def createVocab(self, fp):
        # make sure at beginning of file
        fp.seek(0, 0)
        for line in fp:
            self.__addToVocab(line)

    #############################################################
    # Creates a features vector given a sentence
    #  Goes through all words in the vocabulary, and if a vocabWord
    #  is in the cleanStr then a 1 is placed in the index representing
    #  that word in the feature vector
    #############################################################
    def createFeatureVector(self, sentence):
        # get the classlabel before cleaning it. The classlabel is
        #  the last character in the line, ignoring whitespace
        classLabel = int(sentence.rsplit(None, 1)[-1])
        # clean string then turn it into a list
        cleanStr = self.cleanSentence(sentence).split()
        newVector = [0] * len(self.vocabulary)
        idx = 0
        for vocabWord in self.vocabulary:
            if vocabWord in cleanStr:
                newVector[idx] = 1
            idx += 1

        # class label is the last element in feature vector
        newVector.append(classLabel)
        return newVector

    #############################################################
    # Given a file pointer, for each line in the file createFeatureVecs()
    #  adds converts it to a feature vector then adds it to the list of
    #  feature vectores
    #############################################################
    def createFeatureVecs(self, fp):
        # make sure at beginning of file
        fp.seek(0, 0)
        self.vocabulary.sort()
        for line in fp:
            self.featureVecs.append(self.createFeatureVector(line))






#############################################################
# Class is inherited from BayesData. It must be given a
#  vocabulary which is a list of strings, and the
#  trainedFeatureVecs, which is a list of 1's and 0's where a 1
#  means the vocabWord at vocab[i] is in the training document.
# NaiveBayes creates a naive bayes net and the conditional
#  probability tables based off of the trained features
#############################################################
class NaiveBayes(object):
    """docstring for NaiveBayes."""
    def __init__(self, vocabulary, trainedFeatureVecs):
        super(NaiveBayes, self).__init__()
        self.vocabulary = vocabulary if vocabulary is not None else list()
        self.featureVecs = trainedFeatureVecs if trainedFeatureVecs is not None else list()

        # used to hold the number of features with classLabel X
        self.classLabelSet = {0: 0, 1: 0}

        # Objects where key is vocabWord and value is P(vocabWord | classLabel=1)
        self.labelIsPositive = {}
        self.labelIsNegative = {}

        for vocabWord in self.vocabulary:
            self.labelIsPositive[vocabWord] = {"isPresent": 0, "notPresent": 0}
            self.labelIsNegative[vocabWord] = {"isPresent": 0, "notPresent": 0}

        self.createPropabilities()

    #############################################################
    # Goes through all vocab words and finds the P(vocabWord | classLabel).
    #  It does this via Uniform Dirichlet Priors. For classLabel=1
    #  this is,
    #
    #  (#featureVectors with vocabword=1 AND classLabel=1) + 1
    #  --------------------------------------------------------
    #           (#featureVectors where classLabel=1) + 2
    #############################################################
    def createPropabilities(self):
        for fVector in self.featureVecs:
            # add one to the count for this class label
            if fVector[-1] == 1 or fVector[-1] == 0:
                self.classLabelSet[fVector[-1]] += 1

            for idx in range(0, len(self.vocabulary)):
                vocabWord = self.vocabulary[idx]
                # If classLabel is 1
                if fVector[-1] == 1:
                    if fVector[idx] == 1:
                        self.labelIsPositive[vocabWord]["isPresent"] += 1
                    elif fVector[idx] == 0:
                        self.labelIsPositive[vocabWord]["notPresent"] += 1
                # If classLabel is 0
                elif fVector[-1] == 0:
                    if fVector[idx] == 1:
                        self.labelIsNegative[vocabWord]["isPresent"] += 1
                    elif fVector[idx] == 0:
                        self.labelIsNegative[vocabWord]["notPresent"] += 1
        # Now that we have the (#featureVectors with vocabword=1 AND classLabel=1)
        #  and classLabelSet{} has (#featureVectors where classLabel=1),
        #  add dichlet priors and compute P(vocabWord | classLabel)
        # Values must be casted to float, cuz python2 doesn't do float
        #  division by default, meaning domain error in math.log() if it
        #  were to be 0
        for word, values in self.labelIsPositive.items():
            denom = float(self.classLabelSet[1] + 2)
            presNumerator = float(values["isPresent"] + 1)
            notPresNumerator = float(values["notPresent"] + 1)

            values["isPresent"] = math.log( presNumerator / denom, 2 )
            values["notPresent"] = math.log( notPresNumerator / denom, 2 )

        for word, values in self.labelIsNegative.items():
            denom = float(self.classLabelSet[0] + 2)
            presNumerator = float(values["isPresent"] + 1)
            notPresNumerator = float(values["notPresent"] + 1)

            values["isPresent"] = math.log( presNumerator / denom, 2 )
            values["notPresent"] = math.log( notPresNumerator / denom, 2 )



    #############################################################
    # Given a feature vector, the function returns a tuple where
    #  the first element is the probability the classLabel = 0,
    #  and the second is the probability the classLabel = 1
    #############################################################
    def predictClassLabel(self, featureVector):
        sumLabelPositive = 0
        sumLabelNegative = 0
        for idx in range(0, len(self.vocabulary)):
            vocabWord = self.vocabulary[idx]
            if featureVector[idx] == 1:
                sumLabelPositive += self.labelIsPositive[vocabWord]["isPresent"]
                sumLabelNegative += self.labelIsNegative[vocabWord]["isPresent"]
            elif featureVector[idx] == 0:
                sumLabelPositive += self.labelIsPositive[vocabWord]["notPresent"]
                sumLabelNegative += self.labelIsNegative[vocabWord]["notPresent"]

        totalVectors = self.classLabelSet[0] + self.classLabelSet[1]
        probabilityPos = math.log(float(self.classLabelSet[1]) / float(totalVectors), 2) + sumLabelPositive
        probabilityNeg = math.log(float(self.classLabelSet[0]) / float(totalVectors), 2) + sumLabelNegative
        return [ probabilityNeg, probabilityPos ]

    #############################################################
    # Runs through each feature vecor in testFeatures and predicts
    #  whether the sentiment is positive or negative and reports
    #  the accuracy
    #############################################################
    def predictAllTestFeatures(self, testFeatures):
        numCorrectlyPredicted = 0
        totalNumPredictions = len(testFeatures)

        for featureVector in testFeatures:
            result = self.predictClassLabel(featureVector)
            prediction = 1 if result[1] > result[0] else 0
            if prediction == featureVector[-1]:
                numCorrectlyPredicted += 1
        accuracy = str((float(numCorrectlyPredicted) / float(totalNumPredictions)) * 100)
        print("Accuracy: " + str(accuracy))
        return accuracy

    #############################################################
    # Prints results to a file
    #############################################################
    def printResultsToFile(self, result, trainingName, testingName, fileName, append=False):
        try:
            if append:
                fp = open(str(fileName), "a+")
            else:
                fp = open(str(fileName), "w")
            fp.write("Training File: " + str(trainingName) + "\n")
            fp.write("Testing File: " + str(testingName) + "\n")
            fp.write("Accuracy: " + str(result) + "\n\n")
            fp.close()
        except:
            print("Error opening file named " + str(fileName) + " for writing")
            return




#############################################################
# The trainingSet.txt is in the following order:
#       "some text    ", classlabel
#   where classlabel is 1 is positive sentiment and 0 is
#   negative sentiment.
#
# If cmmd line args are supplied, then use them. If not,
#   then use the default ones
#############################################################
def main():
    # If cmmd args are present adn there are the correct
    #  correct number of them, get cmmd line args as files
    args = sys.argv
    if len(args) > 1:
        if len(args) is not 3:
            print("Lacking two cmmd line args: < trainingSet.txt > < testSet.txt >. \
                    Either supply them or run with no arguments and program will use defualt sets")
            return
        # Open files
        try:
            trainingFO = open(args[1], "r")
            testFO = open(args[2], "r")
        except:
            print("Error on opening a file. Make sure that the file names are correct")
            return
    else:
        trainingFO = open("training_text.txt", "r")
        testFO = open("test_text.txt", "r")


    # Start Pre-Processing
    trainingData = BayesData()
    trainingData.createVocab(trainingFO)
    trainingData.createFeatureVecs(trainingFO)
    trainingData.printFeatsToFile("preprocessed_train.txt")

    testData = BayesData(trainingData.vocabulary)
    testData.createFeatureVecs(testFO)
    testData.printFeatsToFile("preprocessed_test.txt")

    # Start Classifying
    bayes = NaiveBayes(trainingData.vocabulary, trainingData.featureVecs)
    result = bayes.predictAllTestFeatures(trainingData.featureVecs)
    bayes.printResultsToFile(result, trainingFO.name, trainingFO.name, "results.txt")

    result = bayes.predictAllTestFeatures(testData.featureVecs)
    bayes.printResultsToFile(result, trainingFO.name, testFO.name, "results.txt", True)



    trainingFO.close()
    testFO.close()

if __name__ == "__main__":
    main()
