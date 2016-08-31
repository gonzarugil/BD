# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 20:02:45 2015

@author: Gonzalo
"""

import EM
import TDM
import Graph
import collections

   
def setcedwords(newced):
    global cedwords,CED,relevancelist,relationsmatrixes
    cedwords = newced
    CED = collections.OrderedDict()
    for word in cedwords:
        CED[word] = 0
    relevancelist = TDM.MakeRelevanceList(cedwords,last30daysnews)
    relationsmatrixes = TDM.makeCumulativeRelationsMatrixes(CED,last30daysnews)
    
def makelast30days(dayslist):
    if len(dayslist) < 30:
        return dayslist
    else:
        output=[]
        start = len(dayslist)-30
        for i in range(start , len(dayslist)):
            output.append(dayslist[i])
        return output
            

def parseinput(input):
    input = input.lower()
    output = [x.strip() for x in input.split(',')]
    return output    
#Loading lexicons
positiveLex = EM.loadLexicon("resources/wh-positive-words.txt")
negativeLex = EM.loadLexicon("resources/wh-negative-words.txt")
#loading CED
cedwords = ["isis","trump","syria","obama","uk"]
CED = collections.OrderedDict()
for word in cedwords:
    CED[word] = 0
#Loading RSS
feed = TDM.getrss()
#Retrieve the days of the news in a list **** This has to be saved along with the titles 
dayslist = TDM.getRssDays(feed)
TDM.writeDaysList(dayslist)
#Getting a list of the titles (this is unused)
titlelist = []
for entry in feed["entries"]:
    titlelist.append(entry["title"])
    
TDM.writeTitleList(titlelist)
#Retrieve all news from feed and save them to csv
TDM.saveallcsv(feed,dayslist)

#------------------RETRIEVING DATA --------------------------------------
#Getting the list of news from the csv to do the emotion analysis
dayslist = TDM.getListCsv("csv/Days.csv")
last30days= makelast30days(dayslist)
last30daysnews = TDM.getDocsFromCsv(last30days) #it gets the news by day
titlelist = TDM.getListCsv("csv/Titles.csv") #titlelist is unused
relevancelist = TDM.MakeRelevanceList(cedwords,last30daysnews)
relationsmatrixes = TDM.makeCumulativeRelationsMatrixes(CED,last30daysnews)

def EmotionAnalysis(delta,epsilon,figure):
    EM.setDelta(delta)
    EM.setEpsilon(epsilon)
    #for each new compute the emotional value and show it 
    output = [] #output is a list of tuples with [day,CED of that day]
    for i in range(0,len(last30days)):
        EM.computeday(last30daysnews[i],negativeLex,positiveLex,CED)
        output.append([last30days[i],CED.copy()])
    Graph.plotallfigure(figure,output)
    #after the execution we need to clean the values of the CED so they doesnt iterfere with next execution
    for word in cedwords:
        CED[word] = 0
    
def Relations():        
    #print(relationsmatrix) #this is for debug purposes
    try:
        Graph.plotRelations(relationsmatrixes,relevancelist,cedwords)
    except ValueError:
        print("The words you have introduced have no relation")

# this is for printing only the graph corresponding to one day
def RelationDay(i,figure):
    if i in range(len(relationsmatrixes)):
        Graph.plotRelationsDayfigure(figure,relationsmatrixes[i],relevancelist[i],cedwords)
    else:
        print("The i value you have provided is incorrect")
    
def RelationDayCommand(i):
    if i in range(len(relationsmatrixes)):
        Graph.plotRelationsDay(relationsmatrixes[i],relevancelist[i],cedwords)
    else:
        print("The i value you have provided is incorrect")
