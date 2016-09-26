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
    relevancelist = Relations.MakeRelevanceList(cedwords, last30daysnews)
    relationsmatrixes = Relations.makeCumulativeRelationsMatrixes(CED, last30daysnews)


def makelast30days(dayslist):
    if len(dayslist) < 30:
        return dayslist
    else:
        output = []
        start = len(dayslist) - 30
        for i in range(start, len(dayslist)):
            output = output.append(dayslist[i])
        return output

def parseinput(input):
    return Utils.Text.parseinput(input)

# Loading lexicons
positiveLex = Utils.Data.loadLexicon(Config.POS_LEX)
negativeLex = Utils.Data.loadLexicon(Config.NEG_LEX)

# ------------------RETRIEVING DATA --------------------------------------
# Getting the list of news from the csv to do the emotion analysis
dayslist = Utils.Data.getListFromCsv("csv/Days.csv")
last30days = makelast30days(dayslist)
last30daysnews = TDM.getDocsFromCsv(last30days)  # it gets the news by day
titlelist = Utils.Data.getListFromCsv("csv/Titles.csv")  # titlelist is unused
setcedwords(['pope','photo'])


def EmotionAnalysis(epsilon, figure):
    EM.setEpsilon(epsilon)
    # for each new compute the emotional value and show it
    output = []  # output is a list of tuples with [day,CED of that day]
    for i in range(0, len(last30days)):
        EM.computeday(last30daysnews[i], negativeLex, positiveLex, CED)
        output.append([last30days[i], CED.copy()])
    Graph.plotallfigure(figure, output)
    # after the execution we need to clean the values of the CED so they doesnt iterfere with next execution
    for word in cedwords:
        CED[word] = 0


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
