#Phase 3: Data Retrieval
from bsddb3 import db

def singularClauseQuery(query):
   op = operandIndex(query)
   

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
#We will break each query into field-operand-parameter groups.
#We can then perform queries on the appropriate fields using the specified operator and using the given parameter.
def queryHandler(query,mode,termsDB,yearsDB,recsDB):
   
   termsCursor = termsDB.cursor()
   yearsCursor = yearsDB.cursor()
   recsCursor = recsDB.cursor()
   
   #Need to determine what form the query is in.
   #singular clause:  i.e field:param, field<param, field>param, field:"param phrase"
   #Evalute singlular field-parameter queries
  
   
   
   return 0


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
         queryHandler(query,outputMode,termsDB,yearsDB,recsDB)
         print("\n========|^Results^|========")
   print("\n========|Program Closed|========")
   return 0


main()