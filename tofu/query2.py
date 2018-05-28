'''
Created on May 27, 2018

@author: Antuhney
'''

from collections import OrderedDict
import pickledb
import cgi
import codecs
#form = cgi.FieldStorage()
#searchterm =  form.getvalue('searchbox')


def search_query(terms):
    db = pickledb.load("inverted_index2.db", False)
    print("reading database...")
    result = []
    #return a list of unranked url for each terms
    #implement the rank here in the future
    if(len(terms) == 2):
        docs = db.get(terms[0])
        docs2 = db.get(terms[1])
        
        new = set(docs).intersection(set(docs2))

        #result = sorted(new, key=lambda x: )
            
            
        print(new)
        if (len(new) == 0):
            print("docs for terms[0]: ",docs)
    
    if (len(terms) == 1):
        docs = db.get(terms[0])
        docs_list = docs.values()
        #print(docs_list)

        
        sorted_index = sorted(docs_list, key=lambda x: x[1], reverse= True)
        
        
        #sort by tfIDF
        #print(sorted_index)
        
        
        
    for term in terms:
        print("The first url retrieved from the term \'"+term+"\' :")
        #docpost_list = index[term.lower()]
        
        ###########
        ####    INSERT THE FUNCTION FOR GRADING SUCH AS TF-IDF HERE
        ############
        
        # List the top 10 result
        for result in sorted_index[:10]:
            print("tfidf score: " + str(result[1])+"---" + result[3])
        

if __name__ == '__main__':
    query = raw_input("Input a query to search for: ")
    
    queries = query.split(" ")
    search_query(queries)
    
    
    