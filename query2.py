'''
Created on May 27, 2018

@author: Antuhney
'''
import pickledb 


def search_query(terms):
    db = pickledb.load("C:\\Users\\Antuhney\\Desktop\\cs121\\New folder\\inverted_index2.db", False)
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
        
        sorted_urls = sorted(docs, key=lambda x: docs[x][1])
        #sort by tfIDF
        print(sorted_urls)
        
    for term in terms:
        print("The first url retrieved from the term \'"+term+"\' :")
        #docpost_list = index[term.lower()]
        
        ###########
        ####    INSERT THE FUNCTION FOR GRADING SUCH AS TF-IDF HERE
        ############
        
        # List the top 10 result
        """for doc in docpost_list[:10]:
            print(" --- " + doc.url )
           """ 
        

if __name__ == '__main__':
    query = raw_input("Input a query to search for: ")
    
    queries = query.split(" ")
    search_query(queries)
    
    
    