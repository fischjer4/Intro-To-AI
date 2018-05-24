import sys
import string
import re


class BayesData(object):
    """docstring for BayesData."""
    def __init__(self, vocabulary=None, features=None):
        super(BayesData, self).__init__()
        self.vocabulary = vocabulary if vocabulary is not None else list()
        self.features = features if features is not None else list()


    #############################################################
    # Prints the data comma seperated to a files
    # Data is a list []
    #############################################################
    def printToFile(self, fileName):
        try:
            fp = open(str(fileName), "w")
            commaSeperated = ','.join(self.vocabulary)
            fp.write(commaSeperated + ",classlabel\n")

            for vector in self.features:
                # turn all numbers in the vector to strings via map()
                commaSeperated = ','.join(map(str,vector))
                fp.write(commaSeperated+ "\n")
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
        classLabel = sentence.rsplit(None, 1)[-1]
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
    # Given a file pointer, for each line in the file createFeatures()
    #  adds converts it to a feature vector then adds it to the list of
    #  feature vectores
    #############################################################
    def createFeatures(self, fp):
        # make sure at beginning of file
        fp.seek(0, 0)
        self.vocabulary.sort()
        for line in fp:
            self.features.append(self.createFeatureVector(line))


class NaiveBayes(BayesData):
    """docstring for NaiveBayes."""
    def __init__(self, vocabulary, features):
        super(NaiveBayes, self).__init__(vocabulary, features)














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
    trainingData.createFeatures(trainingFO)
    trainingData.printToFile("preprocessed_train.txt")

    testData = BayesData(trainingData.vocabulary)
    trainingData.createFeatures(testFO)
    trainingData.printToFile("preprocessed_test.txt")

    # Start Classifying


    trainingFO.close()
    testFO.close()

if __name__ == "__main__":
    main()
