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
import pymongo
import numpy as np
import sys
# https://pythonhosted.org/pickleDB/commands.html
import pickledb 
#db = pickledb.load('inverted_index.db', False)



# Use nltk to tokenize and remove stopwords
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import string
import posting

temp_batch = 0

index = defaultdict(list) 

sys.setrecursionlimit(5000)   # Delete this line if your laptop can tank the recursion, my laptop cannot

#nltk.download('stopwords')
#nltk.download('punkt')

def process_line(index, file_line, docID, web_url):

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
        doc_post.total_terms = index_num # Number of words in each doc ( to calculate TF)
        doc_post.url = web_url # The original url of the document
        #Add specific document info to token list
        index[token].append(doc_post)
        
        
def calculate_tlidf(index, total_doc_num):
    for token, docs in index.items():
        for doc in docs:
            tf = float(doc.word_freq)/float(doc.total_terms)
            doc.tf = tf
            idf = np.log(total_doc_num / len(docs))
            tf_idf = float(tf) * float(idf)
            doc.tf_idf = tf_idf
            #print(str(token) + " tfidf score in "+str(doc.docID) +" : " + str(doc.tf_idf))
    
            
def init_index():
    counter = 0
    #index = defaultdict(lambda: [0,set(),0,0]) # [ word_freq, docIDs, indices, tf_idf ]
    
    #Key: token  Value: list of docInfo objects    
    #path="C:\\Users\\Antuhney\\Desktop\\cs121\\WEBPAGES\\WEBPAGES_RAW\\"
    path="/Users/DavidLin/Documents/WEBPAGES_RAW/"
    
    
    #bookkeeping2.json is a smaller file for testing purposes
    with open(path+"bookkeeping.json") as f: 
        data = json.load(f)
    #pprint(data)
    
    """file_index is a string "x/y"
        x is directory and y is file that stores the HTML data
    """
    
    filepaths_and_urls = data.items()
    
    total_doc_num = len(filepaths_and_urls)
    for file_index, web_url in filepaths_and_urls:
        counter+=1
        if counter >=100:
            print("status check:")
            print("Running the raw file of the url:"+ str(web_url) )
            counter = 0
        

        dir_file = file_index.split("/")
        dir = dir_file[0] #directory that stores the file
        f = dir_file[1] #file name
        
        #html_data is a full path to a file
        html_data = path + dir + "/" + f
        try:
            temp = open(html_data)
            soup = BeautifulSoup(temp, "html.parser")
            #print(soup.get_text)
                
            #Read all words into a string
            text = soup.get_text
            process_line(index, text, file_index, web_url)
        except RuntimeError:
            pass
        
        #For each FILE, parse it and add it to INDEX
   

        
        
        # Store the information into the database
    calculate_tlidf(index, total_doc_num)
        #db.set()
        
        #Dump the information from memory into database for every 128 files
       # if temp_batch >=128:
            
        #    temp_batch = 0
         #  db.dump()
         
    #collecting stats
    print("======Result======")
    print("Number of the documents: " + str(total_doc_num))
    print("Number of unique tokens found in index" + str(len(index.items())))
    print("Total size of index in disk: " + str(sys.getsizeof(index)/1000) +"KB" )
    
    
    
def search_query(terms):
    #return a list of unranked url for each terms
    #implement the rank here in the future
    for term in terms:
        print("The first url retrieved from the term \'"+term+"\' :")
        docpost_list = index[term.lower()]
        
        ###########
        ####    INSERT THE FUNCTION FOR GRADING SUCH AS TF-IDF HERE
        ############
        
        # List the top 10 result
        for doc in docpost_list[:10]:
            print(" --- " + doc.url )
            
        
        
        
         
if __name__ == '__main__':
    init_index()
    # Instead of asking for query, Just directly import the query for testing
    
    
    ###########
    ####    INSERT THE FUNCTION that prompt user for quary here, including dicing
    ############
    
    search_query(["Informatics", "Mondego", "Irvine"])
    
    

    
    
    # -------- Search database/file and output Query information --------
    
    
    pass





