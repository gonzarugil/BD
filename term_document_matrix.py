# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 19:14:35 2015

@author: Gonzalo
"""

import os.path
import Utils.Data
import Utils.Time
from Utils import textmining
import Utils.Rss
import Utils.Text


def makeTxD(posts):
    # Se inicializa la matriz de Terminos x Documentos
    tdm = textmining.TermDocumentMatrix()
    # Clean the news and add them to the tdm
    # Añadimos las noticias
    for post in posts:
        post.sort()
        tdm.add_doc(" ".join(post))
    return tdm


# Escribimos por pantalla la matriz
def showTxD(tdm):
    for row in tdm.rows(cutoff=2):
        print(row)


# guarda todas las noticias en archivos separados por dias
def saveallcsv(feed, feeddays):
    for day in feeddays:
        postsclean = []
        posts = Utils.Rss.getdayposts(feed, day)
        # we have to clean the posts here because we need to compare them
        for post in posts:
            posttext = post['title'] + " " + post['description']
            newpost = Utils.Text.textCleaner(posttext)
            postsclean.append(newpost)
        # we check if the day exists
        if os.path.exists("csv/" + day + '.csv'):
            olderposts = getOneDocsCsv("csv/" + day + '.csv')
            for old in olderposts:
                old.sort()  # sorting again the older posts
            for p in postsclean:
                if p not in olderposts:
                    olderposts.append(p)
            tdm = makeTxD(olderposts)
        else:
            tdm = makeTxD(postsclean)

        Utils.Data.writeCsv(tdm, day)
        # print ("SAVED DAY", day)


def getOneDocsCsv(path):
    currentdocument = []
    matrix = Utils.Data.loadcsv(path)
    words = matrix[0]
    docwords = []
    lenght = len(words)
    for i in range(2, len(matrix)):  # for each row
        row = matrix[i]
        if not row == []:
            for j in range(0, lenght):  # for each element
                element = int(matrix[i][j])
                for e in range(0, element):  # for the value of each element
                    docwords.append(words[j])  # append the corresponding word n times
                    # docwords contains a list of all the words in the document
            currentdocument.append(docwords)
            docwords = []  # we have to clean docwords between documents
    return currentdocument


def getDocsFromCsv(dayslist):
    doclist = []
    for day in dayslist:
        daylist = []
        path = "csv/" + day + ".csv"
        matrix = Utils.Data.loadcsv(path)
        words = matrix[0]
        docwords = []
        lenght = len(words)
        for i in range(1, len(matrix)):  # for each row, we start in the row 2 (values)
            for j in range(0, lenght):  # for each word (column)
                element = int(matrix[i][j])
                for e in range(0, element):  # for the value of each element
                    docwords.append(words[j])  # append the corresponding word n times
                    # docwords contains a list of all the words in the document
            daylist.append(docwords)
            docwords = []  # we have to clean docwords between documents
        doclist.append(daylist)  # we append the current day's news to doclist
    return doclist


def writeTitleList(l):
    path = "csv/Titles.csv"
    if not os.path.exists(path):
        Utils.Data.writeListToCsv(path, l)
    old = Utils.Data.getListFromCsv(path)
    new = []
    for title in l:
        if title not in old:
            new.append(title)
    Utils.Data.writeListToCsv(path, new)
    return 1


def writeDaysList(l):
    path = "csv/Days.csv"
    if not os.path.exists(path):
        l.sort()  # Thia is not really necessary but for assuring the days are sorted
        Utils.Data.writeListToCsv(path, l)
    else:
        days = Utils.Data.getListFromCsv(path)
        for day in l:
            if day not in days:
                days.append(day)
        days.sort()
        Utils.Data.writeListToCsv(path, days)
    return 1
