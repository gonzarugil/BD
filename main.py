# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 20:02:45 2015

@author: Gonzalo
"""
import EM
import TDM
import Graph    
#Loading lexicons
positiveLex = EM.loadLexicon("resources/wh-positive-words.txt")
negativeLex = EM.loadLexicon("resources/wh-negative-words.txt")
#Loading RSS
feed = TDM.getrss()
#Retrieve the days of the news in a list **** This has to be saved along with the titles 
dayslist = TDM.getRssDays(feed)
TDM.writeDaysList(dayslist)
#Getting a list of the titles (This will be saved in a file ****!!!)
titlelist = []
for entry in feed["entries"]:
    titlelist.append(entry["title"])
    
TDM.writeTitleList(titlelist)
#Retrieve all news from feed and save them to csv
TDM.saveallcsv(feed,dayslist)

#------------------RETRIEVING DATA --------------------------------------
#Getting the list of news from the csv to do the emotion analysis (and the titles and the days when implemented)
allnews = TDM.getDocsFromCsv(dayslist) #it gets the news by day
titlelist = TDM.getListCsv("csv/Titles.csv")
dayslist = TDM.getListCsv("csv/Days.csv")
CED = {"obama":0,"china":0,"clinton":0}
#for each new compute the emotional value and show it 
output = [] #output is a list of tuples with [day,CED of that day]
for i in range(0,len(dayslist)):
    EM.computeday(allnews[i],negativeLex,positiveLex,CED)
    output.append([dayslist[i],CED.copy()])
    
print ("The analysis has concluded, the results are:")
for x in output:
    print ("The emotional value of the words the day "+x[0]+" is:")
    for word in x[1].keys():
        print (word + ": "+str(x[1][word]))
        
Graph.plotall(output)

#The results can also be saved in a file :D