#Phase 1: Preparing Data Files
import re
import os
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
    
    #write terms from journal
    j = re.findall(r'<journal>(.*?)</journal>',line)
    journal = []
    for ji in j:
        ji = re.sub('[^0-9a-zA-Z]+', ' ',ji)
        journal.append(ji)
        journal[journal.index(ji)] = ji.split(' ')
    for jo in journal:
        for term in jo:
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
    
    #grab year and write to years.txt
        
    a = re.findall(r'<year>(.*?)</year>',line)
    year = a[0] 

    yearFile.write(year+':'+key+'\n')
        
    #write to recs.text    
        
    recFile.write(key+':'+line)
    
    return 0

def reset():
    cmnd = "rm -f r_sorted.txt t_sorted.txt y_sorted.txt \
    r.txt t.txt y.txt re.idx te.idx ye.idx"
    os.system(cmnd)

def phase_two():
    # get rid of old files
    reset()

    # commands will be stored here
    commands = []

    # series of commands for phase 2
    sort_r = "sort -u recs.txt >  r_sorted.txt"
    sort_t = "sort -u terms.txt >  t_sorted.txt"
    sort_y = "sort -u years.txt >  y_sorted.txt"
    format_r = "perl break.pl <r_sorted.txt> r.txt"
    format_t = "perl break.pl <t_sorted.txt> t.txt"
    format_y = "perl break.pl <y_sorted.txt> y.txt"
    hash_r = "< r.txt db_load -T -c duplicates=1 -t hash re.idx"
    btree_t = "< t.txt db_load -T -c duplicates=1 -t btree te.idx"
    btree_y = "< y.txt db_load -T -c duplicates=1 -t btree ye.idx"

    # add commands to the list
    commands.extend((sort_r,sort_t,sort_y,format_r, format_t, format_y,\
        hash_r, btree_t, btree_y))

    # run commands in terminal
    for cmnd in commands:
        os.system(cmnd)

    # to see the results, run:
    # db_dump -p indexname.idx

    return True

def main():
    path = input("Please enter the path of the data file to read: ")
    
    if(path == ''):
            print('\nNo data file path given!')
            return False
    
    iterateFile(path)
    
    print("\nPhase 1 complete!\n")

    phase_two()

    print("\nPhase 2 complete!\n")
    return True 

main()