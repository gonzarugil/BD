# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 19:14:35 2015

@author: Gonzalo
"""


import feedparser
import textmining
import time
from bs4 import BeautifulSoup
import re
from nltk.corpus import stopwords # Import the stop word list
import operator
import csv
import os.path

def unformatTime(string):
    return time.strp(string,"%Y - %m - %d")

def formatTime(datein):
    return time.strftime("%Y - %m - %d",datein)

def textCleaner( input ):
     # 1. Remove HTML
    html_free_text = BeautifulSoup(input).get_text()
    # 2. Remove non-letters        
    letters_only = re.sub("[^a-zA-Z]", " ", html_free_text) 
    #
    # 3. Convert to lower case, split into individual words
    words = letters_only.lower().split()                             
    #
    # 4. In Python, searching a set is much faster than searching
    #   a list, so convert the stop words to a set
    stops = set(stopwords.words("english"))                  
    # 
    # 5. Remove stop words
    meaningful_words = [w for w in words if not w in stops]   
    #
    # 6. Join the words back into one string separated by space, 
    # and return the result.
    return( meaningful_words)


# Obtenemos las noticias a través del RSS

def getrss():
    feed = feedparser.parse('http://www.theguardian.com/world/rss')
    feed["entries"].sort(key=operator.itemgetter('date'))
    return feed

#Para saber que dia es hoy usaremos la fecha de la ultima noticia
def todayformatted():
    today = time.time()
    todaystr = formatTime(today)
    print("Today its "+todaystr)
    return todaystr

def getRssDays(feed):
    days = []
    for i in range(0,len(feed['entries'])):
        currentpost = feed['entries'][i]
        postdate = formatTime(currentpost['date_parsed'])
        if postdate not in days:
            days.append(postdate)
        days.sort()
    return days

def getDayPosts(feed,dayformatted):
    posts = []
    numposts = 0
    for i in range(0,len(feed['entries'])):
        currentpost = feed['entries'][i]
        postdate = formatTime(currentpost['date_parsed'])
        if dayformatted == postdate:
            posts.append({
                'title': currentpost.title,
                'description': currentpost.summary,
                'url': currentpost.link,
                })
            numposts += 1
    print(str(numposts)+' posts have been processed')
    return posts
 
def makeTxD(posts):   
    # Se inicializa la matriz de Terminos x Documentos
    tdm = textmining.TermDocumentMatrix()
    # Añadimos las noticias
    for post in posts:
        tdm.add_doc(" ".join(post))
    return tdm
    
def writeCsv(tdm,dayformatted):
    #Esto escribe la matriz en un archivo csv (El cutoff define el numero mínimo de apariciones de cada término)
    tdm.write_csv("csv/"+dayformatted+'.csv', cutoff=1)
#Escribimos por pantalla la matriz
def showTxD(tdm):
    for row in tdm.rows(cutoff=2):
        print(row)
#guarda todas las noticias en archivos separados por dias        
def saveallcsv(feed,feeddays):
    for day in feeddays:
        postsclean = []
        posts = getDayPosts(feed,day)
        #we have to clean the posts here because we need to compare them
        for post in posts:
            newpost = textCleaner(post['description'])
            newpost.sort()  #the post have to be sorted
            postsclean.append(newpost)
        
        #we check if the day exists
        if os.path.exists("csv/"+day+'.csv'):
            olderposts = getOneDocsCsv("csv/"+day+'.csv')
            for old in olderposts:
                old.sort() #sorting again the older posts
            for p in postsclean:
                if p not in olderposts:
                    olderposts.append(p)
            tdm = makeTxD(olderposts)
        else:
            tdm = makeTxD(postsclean)
            
        writeCsv(tdm,day)
        print ("SAVED DAY", day)
        
def loadcsv(name):
    reader=csv.reader(open(name),delimiter=',')
    x=list(reader)
    return x
    
def getOneDocsCsv(path):
    currentdocument = []
    matrix = loadcsv(path)
    words = matrix[0]
    docwords = []
    lenght = len(words)
    for i in range(2,len(matrix)): #for each row
        row = matrix[i]
        if not row == []:
            for j in range (0,lenght):#for each element
                element = int(matrix[i][j])
                for e in range(0,element): #for the value of each element
                    docwords.append(words[j]) # append the corresponding word n times
        #docwords contains a list of all the words in the document
            currentdocument.append(docwords)
            docwords = [] # we have to clean docwords between documents
    return currentdocument
        
def getDocsFromCsv(dayslist):
    doclist = []
    for day in dayslist:
        daylist = []
        path = "csv/"+day +".csv"
        matrix = loadcsv(path)
        words = matrix[0]
        docwords = []
        lenght = len(words)
        for i in range(2,len(matrix)): #for each row
            row = matrix[i]
            if not row == []:
                for j in range (0,lenght):#for each element
                    element = int(matrix[i][j])
                    for e in range(0,element): #for the value of each element
                        docwords.append(words[j]) # append the corresponding word n times
        #docwords contains a list of all the words in the document
                daylist.append(docwords)
                docwords = [] # we have to clean docwords between documents
        doclist.append(daylist) #we append the current day's news to doclist
    return doclist
    
def writeListCsv(name,l):
    resultFile = open(name,'w',encoding='utf-8')
    wr = csv.writer(resultFile, dialect='excel')
    wr.writerow(l)
    return 1
def getListCsv(path):
    l = []
    resultFile = open(path,"r",encoding='utf-8')
    reader = csv.reader(resultFile)
    for row in reader:
        l.append(row)
    return l[0]
def writeTitleList(l):
    path = "csv/Titles.csv"
    if not os.path.exists(path):
        resultFile = open(path,"w",encoding='utf-8')
    resultFile = open(path,"r",encoding='utf-8')
    reader = csv.reader(resultFile)
    old = []
    new = []
    for row in reader:
        old.append(row)
    for title in l:
        if title not in old:
            new.append(title)
    writeListCsv(path, new)
    return 1
    
def writeDaysList(l):
    path = "csv/Days.csv"
    if not os.path.exists(path):
        resultFile = open(path,"w",encoding='utf-8')
    resultFile = open(path,"r",encoding='utf-8')
    reader = csv.reader(resultFile)
    old = []
    new = []
    for row in reader:
        old.append(row)
    for title in l:
        if title not in old:
            new.append(title)
    new.sort()
    writeListCsv(path, new)
    return 1
    