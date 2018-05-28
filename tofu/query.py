'''
Created on May 26, 2018

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
total_doc_num=0
index = defaultdict(dict) 
#f= open("inverted_index1.json","w+")
#f.write("{}")
#db = pickledb.load("C:\\Users\\Antuhney\\Desktop\\cs121\\New folder\\inverted_index.db", False)
#db.set("test", ["val1"])
#db.ladd("test", "val2")
sys.setrecursionlimit(5000)

#nltk.download('stopwords')
#nltk.download('punkt')

def process_line(file_line, docID, web_url):
    #index = defaultdict(dict)
    # -------- Tokenization --------
    doc_text = []
    stop_words = stopwords.words('english') + list(string.punctuation)
    
    #for i in nltk.word_tokenize( str(file_line).lower() ):
    temp = defaultdict(lambda: [0,0,0])
    index_num = 0
    
    tokenizer = RegexpTokenizer(r'\w+')
    tok = tokenizer.tokenize( file_line )
    #chunk = len(tok)/5
    #print("my nem jeff:",len(tok),tok)
    
    #should read the into directly into database
    for i in tok:
        if i not in stop_words:
            #doc_text.append(i)
            temp[i.lower()][0] += 1
            #temp[i][1].append(index_num)
            index_num += 1 #Keeps track of the index in which the word appears
    
    """Dictionary of list. 
        [0] is word frequency
        [1] is a set containing indices
        [2] may be used for tf_idf calculation
    """
    """temp = defaultdict(lambda: [0,set(),0])
    index_num = 0
    
    #Each token has a docInfo object for each doc it's found in
    for word in doc_text:
        temp[word.lower()][0] += 1
        temp[word.lower()][1].add(index_num)
        index_num += 1 #Keeps track of the index in which the word appears
    """
    #keys = db.getall()
    #Store posting information in docInfo object
    for token in temp:
        """doc_post = posting.docInfo(docID)
        doc_post.word_freq = temp[token][0] #Word frequency
        doc_post.indices = temp[token][1] #List of indices
        doc_post.total_terms = index_num
        doc_post.url = web_url"""
        
        #Posting is a dictionary of lists
        post = defaultdict(list)
        post[docID].append(temp[token][0]) #0 word freq
        post[docID].append(temp[token][1]) #1 tf_idf score
        post[docID].append(index_num) #2 total_terms
        post[docID].append(web_url) #3 url
        
        #Creating database here makes it hard to write tf_idf scores later
        """if token in keys:
            
            db.dadd(token, (docID, post[docID]) )
        else:
            db.dcreate(token) 
            db.dadd(token, (docID, post[docID]) ) """

        index[token][docID] = post[docID] #docID is key 
        
    #1) Create a sub-index 2) Calculate tfidf 3) Write into database 
    #calculate_tlidf(index, total_doc_num)

    

#calculate_tlidf will be called once
def calculate_tlidf(index, total_doc_num):
    #Moved pickedb load here for faster processing
    db = pickledb.load("C:\\Users\\Antuhney\\Desktop\\cs121\\New folder\\inverted_index2.db", False)
    for token, docs in index.items():
        #print(docs, type(index))
        db.dcreate(token) #Create an empty dict for 'token'
        
        for doc in docs.keys(): #inner dict
            word_freq = index[token][doc][0]
            total_terms = index[token][doc][2]
            #docID = docs[doc]
            
            tf = float(word_freq)/float(total_terms)
            #doc.tf = tf
            idf = np.log(total_doc_num / len(docs))
            tf_idf = float(tf) * float(idf)
            index[token][doc][1] = tf_idf #[1] is tfidf
            #print(token , " tfidf score in ",docs[doc] ," : " , tf_idf)
            
        db.set(token, docs)
    db.dump()
            
def init_index():
    counter = 0
    #index = defaultdict(lambda: [0,set(),0,0]) # [ word_freq, docIDs, indices, tf_idf ]
    
    #Key: token  Value: list of docInfo objects    
    #path="C:\\Users\\Antuhney\\Desktop\\cs121\\WEBPAGES\\WEBPAGES_RAW\\"
    path="/Users/DavidLin/Documents/WEBPAGES_RAW/"
    
    
    #bookkeeping2.json is a smaller file for testing purposes
    with open(path+"bookkeeping2.json") as f: 
        data = json.load(f)
    
    filepaths_and_urls = data.items()
    
    total_doc_num = len(filepaths_and_urls)
    print(total_doc_num)
    for file_index, web_url in filepaths_and_urls:
        counter+=1
        if counter >=100:
            #print("status check:")
            #print("Running the raw file of the url:"+ str(web_url) )
            counter = 0
        
        
        dir_file = file_index.split("/")
        dir = dir_file[0] #directory that stores the file
        f = dir_file[1] #file name
        
        #PROBLEMATIC FILES - CAUSES CRASH
        if (dir == u"39" and f == u"373"): #5/200
            continue
        if (dir == u"5" and f == u"200"): #5/200
            continue
        
        
        #html_data is a full path to a file
        html_data = path + dir + "/" + f
        try:
            temp = open(html_data)
            print("FILE: ",html_data)
            soup = BeautifulSoup(temp, "html.parser")
            #print(soup.get_text)
                
            #Read all words into a string
            text = soup.get_text()
            
            process_line(text, file_index, web_url)
        except RuntimeError:
            pass
        
        #For each FILE, parse it and add it to INDEX
   

    calculate_tlidf(index, total_doc_num)
    #db.dump()
    #print("All keys: \n"+str(db.getall()))
        # Store the information into the database
    #calculate_tlidf(index, total_doc_num)
        #db.set()
        
        #Dump the information from memory into database for every 128 files
       # if temp_batch >=128:
            
        #    temp_batch = 0
         #  db.dump()
         
    #collecting stats
    """print("======Result======")
    print("Number of the documents: " + str(total_doc_num))
    print("Number of unique tokens found in index" + str(len(index.items())))
    print("Total size of index in disk: " + str(sys.getsizeof(index)/1000) +"KB" )
    """
    

# <Anthony> I moved search_query and user input to another file "query2.py"
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
    #search_query(["Informatics", "Mondego", "Irvine"])
    
    # -------- Ask user for Query --------
    #query = input("Input a query to search for: ")
    
    # -------- Search database/file and output Query information --------
    
    
    pass




