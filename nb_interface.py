# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 20:02:45 2015
@author: Gonzalo
"""

import emotion_polarity_analysis
import term_document_matrix
import graph_figures
import collections
import Utils
import relation_analysis
import config_vars


def setcedwords(newced):
    global cedwords, CED, relevancelist, relationsmatrixes, mds_coords
    cedwords = newced
    CED = collections.OrderedDict()
    for word in cedwords:
        CED[word] = 0
    relevancelist = relation_analysis.MakeRelevanceList(cedwords, news)
    relationsmatrixes = relation_analysis.makeCumulativeRelationsMatrixes(CED, news)
    mds_coords = relation_analysis.compute_mds_coords(relationsmatrixes)


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
    global dayinterval, news, cedwords
    dayinterval = input
    news = term_document_matrix.getDocsFromCsv(dayinterval)
    setcedwords(cedwords)


# Loading lexicons
positiveLex = Utils.Data.loadLexicon(config_vars.POS_LEX)
negativeLex = Utils.Data.loadLexicon(config_vars.NEG_LEX)

# ------------------RETRIEVING DATA --------------------------------------
# Getting the list of news from the csv to do the emotion analysis
dayslist = Utils.Data.getListFromCsv("csv/Days.csv")
dayinterval = makelast30days(dayslist)
# last30days = makelast30days(dayslist)
# last30daysnews = TDM.getDocsFromCsv(last30days)  # it gets the news by day
news = term_document_matrix.getDocsFromCsv(dayinterval)
setcedwords(['default', 'test'])


def EmotionAnalysis(epsilon, figure):
    global news, CED
    emotion_polarity_analysis.setepsilon(epsilon)
    # for each new compute the emotional value and show it
    output = []  # output is a list of tuples with [day,CED of that day]
    for i in range(0, len(dayinterval)):
        emotion_polarity_analysis.computeday(news[i], negativeLex, positiveLex, CED,len(dayinterval))
        output.append([news[i], CED.copy()])
    graph_figures.plotEMfigure(figure, output, dayinterval)
    # after the execution we need to clean the values of the CED so they doesnt iterfere with next execution
    for word in cedwords:
        CED[word] = 0


#DEBUG


# ----

def RelationsGraph():
    # print(relationsmatrix) #this is for debug purposes
    try:
        graph_figures.plotRelations(relationsmatrixes, relevancelist, cedwords)
    except ValueError:
        print("The words you have introduced have no relation")


# this is for printing only the graph corresponding to one day
def RelationDay(i, figure):
    if i in range(len(mds_coords)):
        graph_figures.plotRelationsDayfigure(figure, mds_coords[i], relevancelist[i], cedwords)
    else:
        print("The i value you have provided is incorrect")


def RelationDayCommand(i):
    if i in range(len(mds_coords)):
        graph_figures.plotRelationsDay(mds_coords[i], relevancelist[i], cedwords)
    else:
        print("The i value you have provided is incorrect")

def RelationSummary(figure):
    graph_figures.plotRelationsEvolutionFigure(figure, mds_coords, cedwords)
