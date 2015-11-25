# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 20:02:45 2015

@author: Gonzalo
"""
import EM
import TDM
import Graph
import collections


    
#Loading lexicons
positiveLex = EM.loadLexicon("resources/wh-positive-words.txt")
negativeLex = EM.loadLexicon("resources/wh-negative-words.txt")
#loading CED
cedwords = ["isis","france","clinton","syria","obama","otan"]
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
allnews = TDM.getDocsFromCsv(dayslist) #it gets the news by day
titlelist = TDM.getListCsv("csv/Titles.csv") #titlelist is unused

def EmotionAnalysis(delta,epsilon):
    EM.setDelta(delta)
    EM.setEpsilon(epsilon)
    #for each new compute the emotional value and show it 
    output = [] #output is a list of tuples with [day,CED of that day]
    for i in range(0,len(dayslist)):
        EM.computeday(allnews[i],negativeLex,positiveLex,CED)
        output.append([dayslist[i],CED.copy()])
    Graph.plotall(output)
    #after the execution we need to clean the values of the CED so they doesnt iterfere with next execution
    for word in cedwords:
        CED[word] = 0
    
def Relations():        
    relationsmatrix = TDM.makeRelationsMatrix(CED,allnews)
    #print(relationsmatrix) #this is for debug purposes
    Graph.plotRelations(relationsmatrix,cedwords)



