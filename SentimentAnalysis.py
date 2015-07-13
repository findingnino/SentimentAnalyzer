from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier
from os import listdir
import time, winsound

def dir_list(dir):
    '''Returns the list of all files in self.directory'''
    try:
        return listdir(dir)
    except WindowsError as winErr:
        print("Directory error: " + str((winErr)))

def main():
    json = raw_input("Where is the json training set?")
    print "Program start", time.ctime() #debug
    with open(json, 'r') as file:
        classifier = NaiveBayesClassifier(file, format='json')
        print "Classifier done!", time.ctime() #debug
    test = raw_input("Where is the test eml_folder?")
    print "Testing...", time.ctime()
    for emails in dir_list(test):
        print classifier.classify(emails)
    print "Testing done", time.ctime()

    winsound.Beep(600, 1000)
    time.sleep(.5)
    winsound.Beep(450, 500)
    time.sleep(1)

if __name__ == '__main__':
    main()
