from __future__ import division, unicode_literals
from textblob import TextBlob as tb
import math
from os import listdir

def tf(word, blob):
    '''computes "term-frequency" within a single document'''
    return blob.words.count(word) / len(blob.words)

def n_containing(word, bloblist):
    '''returns number of documents containing "word" '''
    return sum(1 for blob in bloblist if word in blob)

def idf(word, bloblist):
    '''computes "inverse document frequency" - how common "word" is throughout "bloblist" '''
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))

def tfidf(word, blob, bloblist):
    '''computes "tf-idf" '''
    return tf(word, blob) * idf(word, bloblist)

def main():
    '''Give it any folder containing only .txt files and it will compute and display
    the top 5 tf-idf words for each .txt file'''
    folder = raw_input("Which folder am I calculating the tf-idf for?")
    bloblist = []
    for emails in listdir(folder):
        path = folder + '/' + emails
        with open(path, 'r') as email:
            next = tb(email.read())
            bloblist.append(next)
    for i, blob in enumerate(bloblist):
        print("Top words in document {}".format(i + 1))
        scores = {word: tfidf(word, blob, bloblist) for word in blob.words}
        sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        for word, score in sorted_words[:5]:
            print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))

if __name__ == '__main__':
    main()
