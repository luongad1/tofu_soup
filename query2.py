'''
Created on May 27, 2018

@author: Antuhney
'''
import pickledb 


def search_query(terms):
    db = pickledb.load("C:\\Users\\James\\Desktop\\temp\\inverted_index.db", False)
    sorted_urls = []
    
    #Query with two words
    if(len(terms) > 1):
        docs = dict()#db.get(terms[0])
        set_docs = None
        for i in range(len(terms)):
            temp = db.get(terms[i]) #Get urls for terms[i]
            if( temp == None ):
                print("No documents containing '"+str(terms[i])+"' found.")
                continue
            #Find all common documents with term i, using intersection
            set_docs = set(docs).intersection(set(temp))
            docs.update(temp) #Combine the docs of all queries
            
        #If no URLs containing the whole query: Return any of them
        if (set_docs == None):
            query_num = 0 #Index of query that has valid results
            new_docs = {}
            #Find a query that returns valid documents
            for i in range(len(terms)):
                new_docs = db.get(terms[i])
                if (new_docs == None):
                    continue
                else:#Found URLs containing the query terms[i]
                    query_num = i
                    break
            if (new_docs == None):#If none of the queries have results
                print("No results found ...")
                return 0
            print("No URLs containing all queries: "+str(terms)+"\n")
            print("Displaying URLs for '"+str(terms[query_num])+"'.\n")
            docs = db.get(terms[query_num])
            sorted_urls = sorted(new_docs, key=lambda x: docs[x][1])
        else:
            print("Top 10 URLs for the query '"+str(terms)+"':\n")
            sorted_urls = sorted(docs, key=lambda x: docs[x][1])
            
    #Query with 1 word
    if (len(terms) == 1):
        docs = db.get(terms[0])
        if( docs==None ):
            print("No documents containing '"+str(terms[0])+"' found.")
            return 0
        print("Top 10 URLs for the query '"+str(terms[0])+"':\n")
        #Store the top 10 results (sorted by biggest tf_idf size
        sorted_urls = sorted(docs, key=lambda x: docs[x][1])[:10]
        #sorted_urls contains docID's (e.g. "0/1", "10/55")
        
    #for term in terms:
        # List the top 10 result
    for docID in sorted_urls:
        print(str(docs[docID][3])+" --- tf_idf score: "+ str(docs[docID][1])+"\n")

if __name__ == '__main__':
    query = raw_input("Input a query to search for: ")
    
    queries = query.split(" ")
    if (len(queries) == 0):
        print("ERROR: User must input 1 or more queries.")
    else:
        search_query(queries)
    
    
    