# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 14:08:51 2015

@author: Gonzalo
"""

import matplotlib.pyplot as plt
from sklearn import manifold

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
    plt.show
    
def plotRelations(relationsmatrix,cedwords):
    mds = manifold.MDS(n_components=2,metric = False, dissimilarity="precomputed", random_state=6)
    results = mds.fit(relationsmatrix)
    coords = results.embedding_
    plt.figure("Grafica de Relaciones")
    plt.subplots_adjust(bottom = 0.1)
    plt.scatter(coords[:, 0], coords[:, 1], marker = 'o')
    for label, x, y in zip(cedwords, coords[:, 0], coords[:, 1]):
        plt.annotate(label,xy = (x, y), xytext = (-20, 20),textcoords = 'offset points', ha = 'right', va = 'bottom',
        bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
        arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))
    plt.show

        