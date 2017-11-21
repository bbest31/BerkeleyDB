#Phase 1: Preparing Data Files
import re
#iterates through the lines in the data file
def iterateFile(path):
    with open(path) as f:
        #iterates each line
        for line in f:
            lineType = re.findall(r'(?<=\<).+?(?=\ key)',line)
            handleLine(lineType[0],line)
            
    
            
#handles each line from the data file based on its starting tag.
def handleLine(lineType,line):
    #Do nothing
    if(lineType == "article"):
        handleArticle(line)
    elif(lineType == "inproceedings"):
        handleInproceeding

def handleArticle(line):
    #grab key
    k = re.findall(r'key="(.*?)"',line)
    key = k[0]
    
    #grab terms and write to terms.txt
    #open file
    try:
        termFile = open("terms.txt")
    except IOError:
        termFile = open("terms.txt",'w+')
        
    #write terms from title
    t = re.findall(r'<title>(.*?)</title>',line)
    terms = t[0].split(' ')
    for term in terms:
        if(len(term)>2) and (re.match("^[0-9a-zA-Z_]*$")):
            termFile.write('t-'+term.lower()+':'+key+'\n')
            
    #write terms from author
    auth = re.findall(r'<author>(.*?)</author>',line)
    authors = auth[0].split(' ')
    for term in authors:
        if(len(term)>2) and (re.match("^[0-9a-zA-Z_]*$")):
            termFile.write('a-'+term.lower()+':'+key)
    
    #write terms from journal
    j = re.findall(r'<journal>(.*?)</journal>',line)
    journal = j[0].split(' ')
    for term in journal:
        if(len(term)>2) and (re.match("^[0-9a-zA-Z_]*$")):
            termFile.write('o-'+term.lower()+':'+key)
            
    #write terms from publisher
    try:
        p = re.findall(r'<publisher>(.*?)</publisher>',line)
        publisher = p[0].split(' ')
        for term in publisher:
            if(len(term)>2) and (re.match("^[0-9a-zA-Z_]*$")):
                termFile.write('o-'+term.lower()+':'+key)            
    except:
        continue
    #grab year and write to years.txt
    try:
        yearFile = open("years.txt")
    except IOError:
        yearFile = open("years.txt",'w+')
        
    a = re.findall(r'<year>(.*?)</year>',line)
    year = a[0] 

    yearFile.write(year+':'+key+'\n')
        
    #write to recs.text    
    try:
        recFile = open("recs.txt")
    except IOError:
        recFile = open("recs.txt",'w+')
        
    recFile.write(key+':'+line+'\n')
    
    return 0

def handleInproceeding(line):
    #grab key
    k = re.findall(r'key="(.*?)"',line)
    key = k[0]
    
    #grab terms and write to terms.txt
    #open term file
    try:
        termFile = open("terms.txt")
    except IOError:
        termFile = open("terms.txt",'w+')
    
    #write the terms in title
    t = re.findall(r'<title>(.*?)</title>',line)
    terms = t[0].split(' ')
    for term in terms:
        if(len(term)>2) and (re.match("^[0-9a-zA-Z_]*$")):
            termFile.write('t-'+term.lower()+':'+key+'\n')
    
    #write the terms in author
    auth = re.findall(r'<author>(.*?)</author>',line)
    authors = auth[0].split(' ')
    for term in authors:
        if(len(term)>2) and (re.match("^[0-9a-zA-Z_]*$")):
            termFile.write('a-'+term.lower()+':'+key)
            
    #write the terms in booktitle
    j = re.findall(r'<booktitle>(.*?)</booktitle>',line)
    booktitle = j[0].split(' ')
    for term in booktitle:
        if(len(term)>2) and (re.match("^[0-9a-zA-Z_]*$")):
            termFile.write('o-'+term.lower()+':'+key)
    #write the terms in publisher
    try:
        p = re.findall(r'<publisher>(.*?)</publisher>',line)
        publisher = p[0].split(' ')
        for term in publisher:
            if(len(term)>2) and (re.match("^[0-9a-zA-Z_]*$")):
                termFile.write('o-'+term.lower()+':'+key)            
    except:
        continue
    
    #grab year and write to years.txt
    try:
        yearFile = open("years.txt")
    except IOError:
        yearFile = open("years.txt",'w+')
        
    a = re.findall(r'<year>(.*?)</year>',line)
    year = a[0] 

    yearFile.write(year+':'+key+'\n')
        
    #write to recs.text    
    try:
        recFile = open("recs.txt")
    except IOError:
        recFile = open("recs.txt",'w+')
        
    recFile.write(key+':'+line+'\n')
    
    return 0

def main():
    path = input("Please enter the path of the data file to read:")
    
    if(path == ''):
            print('\nNo data file path given!')
            return False
    try:
        iterateFile(path)
    except:
        print("Error opening data file.")
        return False
    
    return True    
    
    
    
    
main()