#Phase 3: Data Retrieval
from bsddb3 import db
import re

#return a list of matches
def termQry(term,mode,tCursor,rCursor):
   
   matches = []
   record = tCursor.get(b't-'+ term.encode(),db.DB_SET)
   if(record != None):
      #Add the match found
      if(mode == 0):
         matches.append(record[1].decode())
      else:
         matches.append(rCursor.get(record[1],db.DB_SET))
      #Add all other instances in title
      dup = tCursor.next_dup()
      while(dup!=None):
         if(mode == 0):
            matches.append(dup[1].decode())
         else:
            matches.append(rCursor.get(dup[1],db.DB_SET))
         dup = tCursor.next_dup()
   
   record = tCursor.get(b'a-'+ term.encode(),db.DB_SET)
   if(record != None):
      #Add the match found
      if(mode == 0):
         matches.append(record[1].decode())
      else:
         matches.append(rCursor.get(record[1],db.DB_SET))
         
      #Add all other instances in author
      dup = tCursor.next_dup()
      while(dup!=None):
         if(mode == 0):
            matches.append(dup[1].decode())
         else:
            matches.append(rCursor.get(dup[1],db.DB_SET))
         dup = tCursor.next_dup()
   
   record = tCursor.get(b'o-'+ term.encode(),db.DB_SET) 
   if(record !=None):
      #Add the match found
      if(mode == 0):
         matches.append(record[1].decode())
      else:
         matches.append(rCursor.get(record[1],db.DB_SET))
         
      #Add all other instances in other
      dup = tCursor.next_dup()
      while(dup!=None):
         if(mode == 0):
            matches.append(dup[1].decode())
         else:
            matches.append(rCursor.get(dup[1],db.DB_SET))
         dup = tCursor.next_dup()
         
   
   return matches

#queries of the form field:param. Should return a list of matches
def equivalenceQuery(field,param,mode,tCursor,yCursor,rCursor):
   matches = []
   
   if(field != 'title' and field != 'author' and field!='year' and field != 'other'):
      print('\nInvalid prefix format!')
      return matches
   #Identifies this as a phrase query
   if(param[0] == '"' and param[-1] == '"' and field != 'year' and param.count('"') == 2):
      
      param = param.replace('"','')
      terms = param.split()
      
      phrase = ''
      query = ''
      #Here we build a multi-clause query using the prefix given in field and the terms we split up from the phrase
      #as well we rebuild the phrase for later use
      for t in terms:
         phrase += t+' '
         t = field+':'+ t+' '
         query = query + t
      query = query.strip()
      #The multiClauseQryHdlr() will give us the keys of the records which have all the terms from the phrase in it.
      matches = multiClauseQryHdlr(query,0,tCursor,yCursor,rCursor)
      
      phrase = phrase.strip()
      phraseMatches = []
      #Now we check to see if the match we found in the multi clause handler has that exact subtring in any of the fields
      for m in matches:
         record = rCursor.get(m.encode(),db.DB_SET)
         full = record[1].decode()
         
         #Now search for substring in the appropriate field.
         #Search in the title field
         if(field == 'title'):
            title = re.findall(r'<title>(.*?)</title>',full)            
            if(phrase in title[0].lower()):
               if(mode == 0):
                  phraseMatches.append(m)
               else:
                  phraseMatches.append(full)
                  
         #Search in the author field
         elif(field == 'author'):
            author = re.findall(r'<author>(.*?)</author>',full)
            if(phrase in author[0].lower()):
               if(mode == 0):
                  phraseMatches.append(m)
               else:
                  phraseMatches.append(full)
                  
                  
         #identify if the record is an article or inproceeding      
         elif(field == 'other'):
            lineType = re.findall(r'(?<=\<).+?(?=\ )',full)
            ltype = lineType[0]
            
            #Search in journal and publisher fields if article
            if(ltype == 'article'):
               journal = re.findall(r'<journal>(.*?)</journal>',full)
               if(phrase in journal[0].lower()):
                  if(mode == 0):
                     phraseMatches.append(m)
                  else:
                     phraseMatches.append(full)
               else:
                  publisher = re.findall(r'<publisher>(.*?)</publisher>',full)
                  if(phrase in publisher[0].lower()):
                     if(mode == 0):
                        phraseMatches.append(m)
                     else:
                        phraseMatches.append(full)
                        
            #Search in booktitle and publisher fields if inproceedings         
            elif(ltype == 'inproceedings'):
               bookTitle = re.findall(r'<booktitle>(.*?)</booktitle>',full)
               if(phrase in bookTitle[0].lower()):
                  if(mode == 0):
                     phraseMatches.append(m)
                  else:
                     phraseMatches.append(full)
               else:
                  publisher = re.findall(r'<publisher>(.*?)</publisher>',full)
                  if(phrase in publisher[0].lower()):
                     if(mode == 0):
                        phraseMatches.append(m)
                     else:
                        phraseMatches.append(full)               
      return phraseMatches
   
   elif(param.count('"')==0):
      
      #Query had form title:x
      if(field == 'title'):
         record = tCursor.get(b't-'+ param.encode(),db.DB_SET)
         if(record != None):
            #Add the match found
            if(mode == 0):
               matches.append(record[1].decode())
            else:
               matches.append(rCursor.get(record[1],db.DB_SET))
            #Add all other instances in title
            dup = tCursor.next_dup()
            while(dup!=None):
               if(mode == 0):
                  matches.append(dup[1].decode())
               else:
                  matches.append(rCursor.get(dup[1],db.DB_SET))
               dup = tCursor.next_dup()      
      #Query had form author:x 
      elif(field == 'author'):
         record = tCursor.get(b'a-'+ param.encode(),db.DB_SET)
         if(record != None):
            #Add the match found
            if(mode == 0):
               matches.append(record[1].decode())
            else:
               matches.append(rCursor.get(record[1],db.DB_SET))
            #Add all other instances in author
            dup = tCursor.next_dup()
            while(dup!=None):
               if(mode == 0):
                  matches.append(dup[1].decode())
               else:
                  matches.append(rCursor.get(dup[1],db.DB_SET))
               dup = tCursor.next_dup()
      #Query had form other:x        
      elif(field == 'other'):
         record = tCursor.get(b't-'+ term.encode(),db.DB_SET)
         if(record != None):
            #Add the match found
            if(mode == 0):
               matches.append(record[1].decode())
            else:
               matches.append(rCursor.get(record[1],db.DB_SET))
            #Add all other instances in title
            dup = tCursor.next_dup()
            while(dup!=None):
               if(mode == 0):
                  matches.append(dup[1].decode())
               else:
                  matches.append(rCursor.get(dup[1],db.DB_SET))
               dup = tCursor.next_dup()      
      #Query had form year:x   
      elif(field == 'year'):
         record = yCursor.get(param.encode(),db.DB_SET)
         if(record != None):
            #Add the match found
            if(mode == 0):
               matches.append(record[1].decode())
            else:
               matches.append(rCursor.get(record[1],db.DB_SET))
            #Add all other instances where year = param
            dup = yCursor.next_dup()
            while(dup!=None):
               if(mode == 0):
                  matches.append(dup[1].decode())
               else:
                  matches.append(rCursor.get(dup[1],db.DB_SET))
               dup = yCursor.next_dup()      
      else:
         print('\nInvalid prefix search!')
   else:
      print('\nInvalid condition format!')
      
   return matches

#return a list of matches
#Look at Range_Search.py from BerkeleyDB lab 
def singleRangeQry(field,param,mode,tCursor,yCursor,rCursor):
   return 0

#
def doubleRangeQry(field,param,mode,yCursor):
   return 0

#Handles singular clause queries.
def singleClauseQryHdlr(query,mode,tCursor,yCursor,rCursor):
   matches = []
   #gets the index of the operator
   op = operandIndex(query)
   
   if(op != None):
      #identify query operator
      field = query[:op]
      field = field.lower()
      param = query[op+1:] 
      
      if(query[op] == ":"):
         param = param.lower()
         matches = equivalenceQuery(field,param,mode,tCursor,yCursor,rCursor)
      elif(query[op] == "<") or (query[op] == ">"):
         matches = singleRangeQry(field,param,mode,yCursor)
         
      else:
         matches = singleRangeQry(field,param,mode,tCursor,yCursor,rCursor)
            
   else:
      query = query.lower()
      matches = termQry(query,mode,tCursor,rCursor)
      
   return matches

#Handles multi claused queries.
#We can treat each clause individually and take the intersection of them all.
#Need to find a way to split the query into clauses without splitting the conditions in the form "term term term"
#Thinking of replacing any space in the phrase with $(or any unallowed title char), do split() on the while query and then turn the $ back into spaces.
def multiClauseQryHdlr(query,mode,tCursor,yCursor,rCursor):
   matches = []
   #Find the range queries and assert that there is at most 2 and they must be different directions <,>
   if(query.count('<')>1) or (query.count('>')>1):
      raise ValueError("\nInvalid range query combination.")
   
   #if there is 1 or more phrase clauses we will alter the phrase to not interfere with the query splitting.
   if(query.count('"') >= 2):
   
      #we get all the indexes of the quotations
      quotations = []
      i = 0
      for i in range(0, len(query)):
         if(query[i] == '"'):
            quotations.append(i)
      
      #Altering phrase clause(s)
      while(len(quotations) != 0):
         #We get everything to the left of the leftmost quotation-mark, everything in between and everything to the right of the rightmost quotation-mark.
         tempLeft = query[:quotations[0]+1]
         tempMid = query[quotations[0]+1:quotations[1]]
         tempRight = query[quotations[1]:]
         #We replace all spaces inside quotation marks with $
         tempMid = tempMid.replace(' ','$')
         query = tempLeft+tempMid+tempRight         
         quotations.pop(0)
         quotations.pop(0)
      
      queries = query.split()
   
      for qry in queries:
         #Reformat phrase query
         if('$' in qry):
            qry = qry.replace('$',' ')
  
         match = singleClauseQryHdlr(qry,mode,tCursor,yCursor,rCursor)
         matches.append(match)
   else:
      queries = query.split()
      
      for qry in queries:
         #Reformat phrase query
         if('$' in qry):
            qry = qry.replace('$',' ')
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
   #This changes all spaces inside quotations to $ for phrase queries in order to accurately discern single or multi clause query format
   temp = query
   if(query.count('"') >= 2):
   
      #we get all the indexes of the quotations
      quotations = []
      i = 0
      for i in range(0, len(temp)):
         if(temp[i] == '"'):
            quotations.append(i)
      
      #Altering phrase clause(s)
      while(len(quotations) != 0):
         #We get everything to the left of the leftmost quotation-mark, everything in between and everything to the right of the rightmost quotation-mark.
         tempLeft = temp[:quotations[0]+1]
         tempMid = temp[quotations[0]+1:quotations[1]]
         tempRight = temp[quotations[1]:]
         #We replace all spaces inside quotation marks with $
         tempMid = tempMid.replace(' ','$')
         temp = tempLeft+tempMid+tempRight         
         quotations.pop(0)
         quotations.pop(0)
         
   if(temp.count(" ") == 0):
      results = singleClauseQryHdlr(query,mode,termsCurs,yearsCurs,recsCurs)
   else:
      results = multiClauseQryHdlr(query,mode,termsCurs,yearsCurs,recsCurs)
   return results


#termsDBConstructor creates the database object from the te.idx file.
def termsDBConstructor():
   try:
      database = db.DB()
      database.set_flags(db.DB_DUP)
      DB_File = "te.idx"
      database.open(DB_File,None,db.DB_BTREE,db.DB_CREATE)
   except:
      print("Error: Creating the terms database.")
   return database


#yearsDBConstructor creates the database object from the ye.idx file.
def yearsDBConsuctor():
   try:
      database = db.DB()
      database.set_flags(db.DB_DUP)
      DB_File = "ye.idx"
      database.open(DB_File,None,db.DB_BTREE,db.DB_CREATE)
   except:
      print("Error: Creating years database.")   
   return database


#recsDBConstructor creates the database object from the re.idx file.
def recsDBConstructor():
   try:
      database = db.DB()
      database.set_flags(db.DB_DUP)
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
         termsDB.close
         yearsDB.close
         recsDB.close
         termsCurs.close
         yearsCurs.close
         recsCurs.close
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
               r = str(r)
               print("\nKey: "+r)
         #Print in full mode
         else:
            for r in results:
               r =str(r)
               #Will format this later
               print(r)
               
         print("\n========|^Results^|========")
   print("\n========|Program Closed|========")
   return 0


main()