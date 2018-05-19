'''
Created on May 18, 2018

@author: Antuhney
'''

class docInfo:

    def __init__(self, doc):
        self.docID = doc
        self.word_freq = 0
        self.indices = []
        self.tf_idf = 0