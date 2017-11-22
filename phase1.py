#Phase 1: Preparing Data Files
import re
#iterates through the lines in the data file
def iterateFile(path):
    #open file
    try:
        termFile = open("terms.txt","w+")
    except IOError:
        termFile = open("terms.txt","w+")
    #grab year and write to years.txt
    try:
        yearFile = open("years.txt","w+")
    except IOError:
        yearFile = open("years.txt","w+")    
    #write to recs.text    
    try:
        recFile = open("recs.txt","w+")
    except IOError:
        recFile = open("recs.txt","w+")
        
    with open(path) as f:
        #iterates each line
        for line in f:
            lineType = re.findall(r'(?<=\<).+?(?=\ )',line)
            if(lineType != []):
                handleLine(lineType[0],line,termFile,yearFile,recFile)
            
    
            
#handles each line from the data file based on its starting tag.
def handleLine(lineType,line,termFile,yearFile,recFile):
    #Do nothing
    if(lineType == "article"):
        handleArticle(line,termFile,yearFile,recFile)
    elif(lineType == "inproceedings"):
        handleInproceeding(line,termFile,yearFile,recFile)

def handleArticle(line,termFile,yearFile,recFile):
    #grab key
    k = re.findall(r'key="(.*?)"',line)
    key = k[0]
    
    #grab terms and write to terms.txt
    
        
    #write terms from title
    temp = re.findall(r'<title>(.*?)</title>',line)
    title = []
    t = temp[0]
    t = re.sub('[^0-9a-zA-Z]+', ' ',t)
    title.append(t)
    terms = title[0].split(' ')
    for term in terms:
        if(len(term)>2) and (re.match("^[0-9a-zA-Z_]*$",term)):
            termFile.write('t-'+term.lower()+':'+key+'\n')
       
    #write terms from author
    authTemp = re.findall(r'<author>(.*?)</author>',line)
    auth = []
    for a in authTemp:
        a = re.sub('[^0-9a-zA-Z]+', ' ',a)
        auth.append(a)
        auth[auth.index(a)] = a.split(' ')
    for authors in auth:
        for term in authors:
            if(len(term)>2) and (re.match("^[0-9a-zA-Z_]*$",term)):
                termFile.write('a-'+term.lower()+':'+key+'\n')
    
    #write terms from journal
    j = re.findall(r'<journal>(.*?)</journal>',line)
    journal = j[0].split(' ')
    for term in journal:
        if(len(term)>2) and (re.match("^[0-9a-zA-Z_]*$",term)):
            termFile.write('o-'+term.lower()+':'+key+'\n')
            
    #write terms from publisher
    try:
        p = re.findall(r'<publisher>(.*?)</publisher>',line)
        publisher = p[0].split(' ')
        for term in publisher:
            if(len(term)>2) and (re.match("^[0-9a-zA-Z_]*$",term)):
                termFile.write('o-'+term.lower()+':'+key+'\n')            
    except:
        pass
    
        
    a = re.findall(r'<year>(.*?)</year>',line)
    year = a[0] 

    yearFile.write(year+':'+key+'\n')
        
    
    recFile.write(key+':'+line)
    
    return 0

def handleInproceeding(line,termFile,yearFile,recFile):
    #grab key
    k = re.findall(r'key="(.*?)"',line)
    key = k[0]
    
    #grab terms and write to terms.txt
    
    #write the terms in title
    temp = re.findall(r'<title>(.*?)</title>',line)
    title = []
    t = temp[0]
    t = re.sub('[^0-9a-zA-Z]+', ' ',t)
    title.append(t)
    terms = title[0].split(' ')
    for term in terms:
        if(len(term)>2) and (re.match("^[0-9a-zA-Z_]*$",term)):
            termFile.write('t-'+term.lower()+':'+key+'\n')
    
    #write the terms in author
    authTemp = re.findall(r'<author>(.*?)</author>',line)
    auth = []
    for a in authTemp:
        a = re.sub('[^0-9a-zA-Z]+', ' ',a)
        auth.append(a)        
        auth[auth.index(a)] = a.split(' ')
    for authors in auth:
        for term in authors:
            if(len(term)>2) and (re.match("^[0-9a-zA-Z_]*$",term)):
                termFile.write('a-'+term.lower()+':'+key+'\n')
            
    #write the terms in booktitle
    j = re.findall(r'<booktitle>(.*?)</booktitle>',line)
    booktitle = j[0].split(' ')
    for term in booktitle:
        if(len(term)>2) and (re.match("^[0-9a-zA-Z_]*$",term)):
            termFile.write('o-'+term.lower()+':'+key+'\n')
    #write the terms in publisher
    try:
        p = re.findall(r'<publisher>(.*?)</publisher>',line)
        publisher = p[0].split(' ')
        for term in publisher:
            if(len(term)>2) and (re.match("^[0-9a-zA-Z_]*$",term)):
                termFile.write('o-'+term.lower()+':'+key+'\n')            
    except:
        pass
    
    #grab year and write to years.txt
        
    a = re.findall(r'<year>(.*?)</year>',line)
    year = a[0] 

    yearFile.write(year+':'+key+'\n')
        
    #write to recs.text    
        
    recFile.write(key+':'+line)
    
    return 0

def main():
    path = input("Please enter the path of the data file to read:")
    
    if(path == ''):
            print('\nNo data file path given!')
            return False
    
    iterateFile(path)
    
    print("\nData extraction complete!\n")
    return True    
    
    
    
    
main()