'''
Created on May 17, 2018

@author: Antuhney 
'''

#from bs4 import BeautifulSoup
import json
from pprint import pprint
from collections import defaultdict
from bs4 import BeautifulSoup
import re
import urllib2
import os

# Use nltk to tokenize and remove stopwords
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import string
import posting


#nltk.download('stopwords')
#nltk.download('punkt')

def process_line(index, file_line, docID):
    # -------- Tokenization --------
    #doc_text = list(re.split('[\W_]+', str(file_line))) 
    doc_text = []
    stop_words = stopwords.words('english') + list(string.punctuation)
    
    #for i in nltk.word_tokenize( str(file_line).lower() ):
    tokenizer = RegexpTokenizer(r'\w+')
    for i in tokenizer.tokenize( str(file_line).lower() ):
        if i not in stop_words:
            doc_text.append(i)
    
    """Dictionary of list. 
        [0] is word frequency
        [1] is a set containing indices
        [2] may be used for tf_idf calculation
    """
    temp = defaultdict(lambda: [0,set(),0])
    index_num = 0
    
    #Each token has a docInfo object for each doc it's found in
    for word in doc_text:
        temp[word.lower()][0] += 1
        temp[word.lower()][1].add(index_num)
        index_num += 1 #Keeps track of the index in which the word appears
        
    #Store posting information in docInfo object
    for token in temp:
        doc_post = posting.docInfo(docID)
        doc_post.word_freq = temp[token][0] #Word frequency
        doc_post.indices = temp[token][1] #List of indices
        # -------- Handle tf-idf here? --------
        
        #Add specific document info to token list
        index[token].append(doc_post)
    
            
def init_index():
    #index = defaultdict(lambda: [0,set(),0,0]) # [ word_freq, docIDs, indices, tf_idf ]
    
    #Key: token  Value: list of docInfo objects
    index = defaultdict(list) 
    
    path="C:\\Users\\Antuhney\\Desktop\\cs121\\WEBPAGES\\WEBPAGES_RAW\\"
    
    #bookkeeping2.json is a smaller file for testing purposes
    with open(path+"bookkeeping2.json") as f: 
        data = json.load(f)
    #pprint(data)
    
    """file_index is a string "x/y"
        x is directory and y is file that stores the HTML data
    """
    for file_index, web_url in data.items():
        #print(file_index, web_url)

        dir_file = file_index.split("/")
        dir = dir_file[0] #directory that stores the file
        f = dir_file[1] #file name
        
        #html_data is a full path to a file
        html_data = path + dir + "\\" + f
        temp = open(html_data)
        soup = BeautifulSoup(temp, "html.parser")
        #print(soup.get_text)
            
        #Read all words into a string
        text = soup.get_text
        
        #For each FILE, parse it and add it to INDEX
        process_line(index, text, file_index)
        
        # ------ Store the data in a file or Database ------
        fil = open("Analytics.txt", 'w')
        
        #Output words and how many documents the word appears in
        for token in index:
            fil.write(str(token) + "-" + str( len(index[token]) ) +"\n" )



if __name__ == '__main__':
    init_index()
    
    
    # -------- Ask user for Query --------
    
    
    # -------- Search database/file and output Query information --------
    
    
    pass





