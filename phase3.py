#Phase 3: Data Retrieval
from bsddb3 import db

#return a list of matches
def termQry(term,mode,tCursor,yCursor,rCursor):
   return 0

#queries of the form field:param. Should return a list of matches
def equivalenceQuery(field,param,mode,tCursor,yCursor,rCursor):
   
   return 0
#return a list of matches
def singleRangeQry(field,param,mode,tCursor,yCursor,rCursor):
   return 0

#Handles singular clause queries.
def singleClauseQryHdlr(query,mode,tCursor,yCursor,rCursor):
   
   #gets the index of the operator
   op = operandIndex(query)
   
   if(op != None):
      #identify query operator
      if(query[op] == ":"):
         
         field = query[:op]
         field = field.lower
         param = query[op:]
         
         matches = equivalenceQuery(field,param,mode,tCursor,yCursor,rCursor)
      else:
         matches = singleRangeQry(field,param,mode,tCursor,yCursor,rCursor):
            
   else:
      matches = termQry(query,mode,tCursor,yCursor,rCursor)
      
   return matches

#Handles multi claused queries.
#We can treat each clause individually and take the intersection of them all.
#Need to find a way to split the query into clauses without splitting the conditions in the form "term term term"
#Thinking of replacing any space in the phrase with $(or any unallowed title char), do split() on the while query and then turn the $ back into spaces.
def multiClauseQryHdlr(query,mode,tCursor,yCursor,rCursor):
   
   #Find the range queries and assert that there is at most 2 and they must be different directions <,>
   if(query.count('<')>1) or (query.count('>')>1):
      raise ValueError("\nInvalid range query combination.")
   
   #if there is 1 or more phrase clauses we will alter the phrase to not interfere with the query splitting.
   if(query.count('"') >= 2):
   
      #we get all the indexes of the quotations
      quotations = []
      i = 0
      for i in range(0, len(query)-1):
         if(query[i] == '"'):
            quotations.append(i)
      
      #Altering phrase clause(s)
      while(len(quotations) != 0):
         #for each phrase (in between each set of quotations)
         for i in range(quotations[0], quotations[1]):
            if(query[i] == " "):
               query[i] = '$'
         quotations.pop(0)
         quotations.pop(0)
   
   queries = query.split()
   
      
   matches = []
   for qry in queries:
      #reformat phrase query
      if(qry.count('$')>0):
         qry.replace('$',' ')
         
      match = singleClauseQryHdlr(qry,mode,tCursor,yCursor,rCursor)
      matches.append(match)
      
   #now matches is a list of list which contains matching records in each
   #We now want to get the intersection of all these sets in order to find the real results.
   result = matches[0]
   matches.pop(0)
   for match in matches:
      result = set(result).intersection(match)
   return result


#This method will identify the operator in the query clause being used and return the index.
def operandIndex(clause):
   for c in clause:
      if(c == ":"):
         return clause.index(c)
      elif(c == ">"):
         return clause.index(c)
      elif(c == "<"):
         return clause.index(c)
   return None
      
#Method to handle the input that are not output changes or program exits but queries.
#We can then perform queries on the appropriate fields using the specified operator and using the given parameter.
def queryHandler(query,mode,termsCurs,yearsCurs,recsCurs):
   
   #Need to determine what form the query is in.
   #singular clause:  i.e field:param, field<param, field>param, field:"param phrase"
   #multi clause: i.e. field:param field:param, etc.
   if(query.count(" ") == 0):
      results = singleClauseQryHdlr(query,mode,termsCurs,yearsCurs,recsCurs)
   else:
      results = multiClauseQryHdlr(query,mode,termsCurs,yearsCurs,recsCurs)
   return results


#termsDBConstructor creates the database object from the te.idx file.
def termsDBConstructor():
   try:
      database = db.DB()
      DB_File = "te.idx"
      database.open(DB_File,None,db.DB_BTREE,db.DB_CREATE)
   except:
      print("Error: Creating the terms database.")
   return database


#yearsDBConstructor creates the database object from the ye.idx file.
def yearsDBConsuctor():
   try:
      database = db.DB()
      DB_File = "ye.idx"
      database.open(DB_File,None,db.DB_BTREE,db.DB_CREATE)
   except:
      print("Error: Creating years database.")   
   return database


#recsDBConstructor creates the database object from the re.idx file.
def recsDBConstructor():
   try:
      database = db.DB()
      DB_File = "re.idx"
      database.open(DB_File,None,db.DB_HASH,db.DB_CREATE)
   except:
      print("Error: Creating recs db.")   
   return database


#Our MAIN Function
def main():
   print("========|Data Retrieval|========")    
   #creates the BerkelyDB databases from the provided index files from phase 2
   try:
      termsDB = termsDBConstructor()
      yearsDB = yearsDBConsuctor()
      recsDB = recsDBConstructor()
      #initialize cursors
      termsCurs = termsDB.cursor()
      yearsCurs = yearsDB.cursor()
      recsCurs = recsDB.cursor()      
   except:
      return False
   
   print("\nInput options:\ni) Q to quit\nii) output=full for full output format\niii) output=key for key output format")
   quit = False
   #This var indicates the output mode.
   # 1 => full; 0 => key
   outputMode = 0
   while(quit == False):
      #Indicating the current output format.
      if(outputMode == 1):
         print("\nOutput Format: Full")
      else:
         print("\nOutput Format: Key")
            
      query = input("\nEnter query: ")
      query = str(query).strip()
      #may need a for loop to go through and any alpha char call .lower()
      #Decision making with input.
      if(query == 'Q') or (query == 'q'):
         quit = True
         break
      elif(query.replace(" ",'') == "output=full"):
         outputMode = 1
         print("\n========|Output Format Changed|========")
            
      elif(query.replace(" ",'') == "output=key"):
         outputMode = 0
         print("\n========|Output Format Changed|========")
      #Handle Query
      else:
         results = queryHandler(query,outputMode,termsCurs,yearsCurs,recsCurs)
         #Need to format print based on mode
         if(len(results) == 0):
            print("\nNo matches found.")
         #Print in key mode
         elif(outputMode == 0):
            for r in results:
               print("Key: "+r+'\n')
         #Print in full mode
         else:
            for r in results:
               #Will format this later
               print('\n'+r)
               
         print("\n========|^Results^|========")
   print("\n========|Program Closed|========")
   return 0


main()