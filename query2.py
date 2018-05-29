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
        docs = {}
        for i in range(len(terms)):
            
            temp = db.get(terms[i]) #Get urls for terms[i]
            if( docs == None ):
                print("No documents containing '"+str(terms[i])+"' found.")
                continue
            #Find all common documents with term i, using intersection
            docs = set(docs).intersection(set(temp))
            
        #If no URLs containing the whole query: Return any of them
        if (len(docs) == 0):
            query_num = 0 #Index of query that has valid results
            new_docs = {}
            for i in range(len(terms)):
                new_docs = db.get(terms[i])
                if (len(new_docs) == 0):
                    continue
                else:#Found URLs containing the query terms[i]
                    query_num = i
                    break
            if (len(new_docs) == 0):#If none of the queries have results
                print("No results found ...")
                return 0
            print("No URLs containing queries: ",terms,"\n")
            print("Displaying URLs for '",terms[query_num],"': \n")
            sorted_urls = sorted(new_docs, key=lambda x: docs[x][1])
        else:
            sorted_urls = sorted(docs, key=lambda x: docs[x][1])
            
    #Query with 1 word
    if (len(terms) == 1):
        docs = db.get(terms[0])
        if( docs==None ):
            print("No documents containing '"+str(terms[0])+"' found.")
            return 0
            
        #Store the top 10 results (sorted by biggest tf_idf size
        sorted_urls = sorted(docs, key=lambda x: docs[x][1])[:10]
        #sorted_urls contains docID's (e.g. "0/1", "10/55")
        
    for term in terms:
        print("Top 10 URLs for the query '",term,"':\n")
        # List the top 10 result
        for docID in sorted_urls:
            print(docs[docID][3]," --- tf_idf score: ", docs[docID][1],"\n")

if __name__ == '__main__':
    query = raw_input("Input a query to search for: ")
    
    queries = query.split(" ")
    if (len(queries) == 0):
        print("ERROR: User must input 1 or more queries.")
    else:
        search_query(queries)
    
    
    