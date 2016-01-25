# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 14:08:51 2015

@author: Gonzalo
"""

import matplotlib.pyplot as plt
import collections
from sklearn import manifold

flag = 0

def plotall(input):
    days = [];
    for day in input:
        days.append(day[0]) #append the string day, this will be the x axis
    words = [];
    for word in input[0][1].keys():
        words.append(word) #append the words, we will draw one graph for each word
    
    showabledays = []
    for day in days:
        showabledays.append(day[12:])
    emgraph = plt.figure("Grafica de Emociones")
    emgraph.clear()
    plt.xticks(range(len(days)),showabledays,color="blue");
    for word in words:
        values = []
        for day in input:
            values.append(day[1][word]) #append the value of the word in each day
        plt.plot(range(len(days)),values, label=word)
        plt.legend( loc="lower left")
    plt.draw()
    
def plotRelations(relationsmatrixes,relevancelist,cedwords):
    #version to compute the global relevance (this will change in the future)
    """allrelevances=collections.OrderedDict()
    for word in cedwords:
        allrelevances[word]=0
    for newsday in relevancelist:
        for word in cedwords:
            #we have to check if the word appears in newsday
            if word in list(newsday.keys()):
                allrelevances[word]+=newsday[word]"""
    #-------------------------------------------------------------------------
    for i in range(len(relevancelist)):
        
        #Getting the relevance and relations of the day to plot
        relevance = relevancelist[i]
        relations = relationsmatrixes[i]
        if (relations==[[1, 0, 0, 0, 0.0], [0, 1, 0, 0, 0.0], [0, 0, 1, 0, 0.0], [0, 0, 0, 1, 0.0], [0.0, 0.0, 0.0, 0.0, 1]]):
            print("THERE IS NO RELATION AT AL HUEHUEHUEHUEHEU")
        else:
            mds = manifold.MDS(n_components=2,metric = False, dissimilarity="precomputed", random_state=6)
            results = mds.fit(relations)
            coords = results.embedding_
            plt.figure(i)
            plt.subplots_adjust(bottom = 0.1)
            #for having better visibility, this can be changed for another function(exponential?)
            for word in cedwords:
                relevance[word]=relevance[word]*10
                
            sizes = list(relevance.values())    
            plt.scatter(coords[:, 0], coords[:, 1], marker = 'o', s=sizes)
            for label, x, y in zip(cedwords, coords[:, 0], coords[:, 1]):
                plt.annotate(label,xy = (x, y), xytext = (-20, 20),textcoords = 'offset points', ha = 'right', va = 'bottom',
                             bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
                             arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))
    
        
    
def plotRelationsDay(relations,relevance,cedwords):
        global flag        
        if flag == 1:
            plt.close(plt.figure("Relations"))
        else:
            flag = 1
        relevanceaux = relevance.copy()
        mds = manifold.MDS(n_components=2,metric = False, dissimilarity="precomputed", random_state=6)
        results = mds.fit(relations)
        coords = results.embedding_
        relfig = plt.figure("Relations")
        relfig.clear()
        plt.subplots_adjust(bottom = 0.1)
        #for having better visibility, this can be changed for another function(exponential?)
        for word in cedwords:
            relevanceaux[word]=relevanceaux[word]*10
                
        sizes = list(relevanceaux.values())    
        plt.scatter(coords[:, 0], coords[:, 1], marker = 'o', s=sizes)
        for label, x, y in zip(cedwords, coords[:, 0], coords[:, 1]):
            plt.annotate(label,xy = (x, y), xytext = (-20, 20),textcoords = 'offset points', ha = 'right', va = 'bottom',
                        bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
                        arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))
        plt.draw()
        
def plotRelationsDayfigure(figure,relations,relevance,cedwords):
        plt.figure(figure.number)
        global flag        
        if flag == 1:
            plt.clf()
        else:
            flag = 1
        relevanceaux = relevance.copy()
        mds = manifold.MDS(n_components=2,metric = False, dissimilarity="precomputed", random_state=6)
        results = mds.fit(relations)
        coords = results.embedding_
        plt.subplots_adjust(bottom = 0.1)
        #for having better visibility, this can be changed for another function(exponential?)
        for word in cedwords:
            relevanceaux[word]=relevanceaux[word]*10
                
        sizes = list(relevanceaux.values())    
        plt.scatter(coords[:, 0], coords[:, 1], marker = 'o', s=sizes)
        for label, x, y in zip(cedwords, coords[:, 0], coords[:, 1]):
            plt.annotate(label,xy = (x, y), xytext = (-20, 20),textcoords = 'offset points', ha = 'right', va = 'bottom',
                        bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
                        arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))
        plt.draw()