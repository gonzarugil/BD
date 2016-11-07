# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 20:02:45 2015
@author: Gonzalo
"""

import EM
import TDM
import Graph
import collections
import Utils
import Relations
import Config


def setcedwords(newced):
    global cedwords, CED, relevancelist, relationsmatrixes
    cedwords = newced
    CED = collections.OrderedDict()
    for word in cedwords:
        CED[word] = 0
    relevancelist = Relations.MakeRelevanceList(cedwords, news)
    relationsmatrixes = Relations.makeCumulativeRelationsMatrixes(CED, news)


def makedayinterval(daystart, dayend):
    global dayslist
    output = []
    if daystart < dayend:
        for day in dayslist:
            if daystart <= day <= dayend:
                output.append(day)
    return output


def makelast30days(dayslist):
    if len(dayslist) < 30:
        return dayslist
    else:
        output = []
        start = len(dayslist) - 30
        for i in range(start, len(dayslist)):
            output.append(dayslist[i])
        return output


def parseinput(input):
    return Utils.Text.parseinput(input)


def setdayinterval(input):
    global dayinterval,news,cedwords
    dayinterval = input
    news = TDM.getDocsFromCsv(dayinterval)
    setcedwords(cedwords)

# Loading lexicons
positiveLex = Utils.Data.loadLexicon(Config.POS_LEX)
negativeLex = Utils.Data.loadLexicon(Config.NEG_LEX)

# ------------------RETRIEVING DATA --------------------------------------
# Getting the list of news from the csv to do the emotion analysis
dayslist = Utils.Data.getListFromCsv("csv/Days.csv")
dayinterval = makelast30days(dayslist)
# last30days = makelast30days(dayslist)
# last30daysnews = TDM.getDocsFromCsv(last30days)  # it gets the news by day
news = TDM.getDocsFromCsv(dayinterval)
setcedwords(['default','test'])


def EmotionAnalysis(epsilon, figure):
    global news,CED
    EM.setEpsilon(epsilon)
    # for each new compute the emotional value and show it
    output = []  # output is a list of tuples with [day,CED of that day]
    for i in range(0, len(dayinterval)):
        EM.computeday(news[i], negativeLex, positiveLex, CED)
        output.append([news[i], CED.copy()])
    Graph.plotallfigure(figure, output,dayinterval)
    # after the execution we need to clean the values of the CED so they doesnt iterfere with next execution
    for word in cedwords:
        CED[word] = 0

#i = makedayinterval('2016 - 09 - 10','2016 - 09 - 13')
#setdayinterval(i)
#EmotionAnalysis(0.5,None)

def RelationsGraph():
    # print(relationsmatrix) #this is for debug purposes
    try:
        Graph.plotRelations(relationsmatrixes, relevancelist, cedwords)
    except ValueError:
        print("The words you have introduced have no relation")


# this is for printing only the graph corresponding to one day
def RelationDay(i, figure):
    if i in range(len(relationsmatrixes)):
        Graph.plotRelationsDayfigure(figure, relationsmatrixes[i], relevancelist[i], cedwords)
    else:
        print("The i value you have provided is incorrect")


def RelationDayCommand(i):
    if i in range(len(relationsmatrixes)):
        Graph.plotRelationsDay(relationsmatrixes[i], relevancelist[i], cedwords)
    else:
        print("The i value you have provided is incorrect")
