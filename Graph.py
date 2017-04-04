# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 14:08:51 2015

@author: Gonzalo
"""


import matplotlib.pyplot as plt
import collections
from sklearn import manifold
import numpy as np

flagr = 0
flage = 0
flags = 0

colors = ['b','g','r','m','y','k','c']


def plotEM(input):
    days = []
    for day in input:
        days.append(day[0])  # append the string day, this will be the x axis
    words = []
    for word in input[0][1].keys():
        words.append(word)  # append the words, we will draw one graph for each word

    showabledays = []
    for day in days:
        showabledays.append(day[12:])
    emgraph = plt.figure("Grafica de Emociones")
    emgraph.clear()
    plt.xticks(range(len(days)), showabledays, color="blue")
    for word in words:
        values = []
        for day in input:
            values.append(day[1][word])  # append the value of the word in each day
        plt.plot(range(len(days)), values, label=word)
        plt.legend(loc="lower left")
    plt.draw()


def plotEMfigure(figure, input, dayinterval):
    global flage
    plt.figure(figure.number)
    if flage == 1:
        plt.clf()
    else:
        flage = 1
    days = []
    for day in dayinterval:
        days.append(day)  # append the string day, this will be the x axis
    words = []
    for word in input[0][1].keys():
        words.append(word)  # append the words (from the first element), we will draw one graph for each word

    showabledays = []
    for day in days:
        showabledays.append(day[12:])
    plt.xticks(range(len(days)), showabledays, color="blue")
    for word in words:
        values = []
        for day in input:
            values.append(day[1][word])  # append the value of the word in each day
        plt.plot(range(len(days)), values, label=word)
        plt.legend(loc="lower left")
    plt.axhline(0, linestyle='--',color='black',lw=0.5)
    plt.draw()


def plotRelations(relationsmatrixes, relevancelist, cedwords):
    # version to compute the global relevance (this will change in the future)
    """allrelevances=collections.OrderedDict()
    for word in cedwords:
        allrelevances[word]=0
    for newsday in relevancelist:
        for word in cedwords:
            #we have to check if the word appears in newsday
            if word in list(newsday.keys()):
                allrelevances[word]+=newsday[word]"""
    # -------------------------------------------------------------------------
    for i in range(len(relevancelist)):

        # Getting the relevance and relations of the day to plot
        relevance = relevancelist[i]
        relations = relationsmatrixes[i]
        if relations == [[1, 0, 0, 0, 0.0],
                         [0, 1, 0, 0, 0.0],
                         [0, 0, 1, 0, 0.0],
                         [0, 0, 0, 1, 0.0],
                         [0.0, 0.0, 0.0, 0.0, 1]]:
            print("There is no Relation at all")
        else:
            mds = manifold.MDS(n_components=2, metric=True, dissimilarity="precomputed", random_state=6)
            results = mds.fit(relations)
            coords = results.embedding_
            plt.figure(i)
            plt.subplots_adjust(bottom=0.1)
            # for having better visibility, this can be changed for another function(exponential?)
            for word in cedwords:
                relevance[word] *= 10

            sizes = list(relevance.values())
            plt.scatter(coords[:, 0], coords[:, 1], marker='o', s=sizes)
            for label, x, y in zip(cedwords, coords[:, 0], coords[:, 1]):
                plt.annotate(label,
                             xy=(x, y),
                             xytext=(-20, 20),
                             textcoords='offset points',
                             ha='right', va='bottom',
                             bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
                             arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))


def plotRelationsDay(coords, relevance, cedwords):
    global flagr
    if flagr == 1:
        plt.close(plt.figure("Relations"))
    else:
        flagr = 1
    relevanceaux = relevance.copy()
    relfig = plt.figure("Relations")
    relfig.clear()
    plt.subplots_adjust(bottom=0.1)
    # for having better visibility, this can be changed for another function(exponential?)
    for word in cedwords:
        relevanceaux[word] *= 10

    sizes = list(relevanceaux.values())
    plt.scatter(coords[:, 0], coords[:, 1], marker='o', s=sizes)
    for label, x, y in zip(cedwords, coords[:, 0], coords[:, 1]):
        plt.annotate(label, xy=(x, y), xytext=(-20, 20),
                     textcoords='offset points', ha='right', va='bottom',
                     bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
                     arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
    plt.draw()


def plotRelationsDayfigure(figure, coords, relevance, cedwords):
    plt.figure(figure.number)
    global flagr
    if flagr == 1:
        plt.clf()
    else:
        flagr = 1
    relevanceaux = relevance.copy()
    plt.subplots_adjust(bottom=0.1)
    # for having better visibility, this can be changed for another function(exponential?)
    for word in cedwords:
        relevanceaux[word] *= 10

    sizes = list(relevanceaux.values())
    plt.scatter(coords[:, 0], coords[:, 1], marker='o', s=sizes)
    for label, x, y in zip(cedwords, coords[:, 0], coords[:, 1]):
        plt.annotate(label, xy=(x, y), xytext=(-20, 20), textcoords='offset points',
                     ha='right', va='bottom',
                     bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
                     arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
    plt.autoscale(enable=False)
    plt.axis([-1,1,-1,1])
    plt.draw()

def plotRelationsEvolution(mds_coords,cedwords):
    coord_dict = collections.OrderedDict()
    for word in cedwords:
        coord_dict[word] = []
    for day in mds_coords:
        for i in range(len(cedwords)):
            coord_dict[cedwords[i]].append(day[i])
    for j in range(len(cedwords)):
        plt.plot([e[0] for e in coord_dict[cedwords[j]]],
                 [e[1] for e in coord_dict[cedwords[j]]],
                 label=cedwords[j],
                 marker='o')
    plt.legend()
    plt.draw()
    plt.show()

def plotRelationsEvolutionFigure(figure,mds_coords,cedwords):
    global flags
    plt.figure(figure.number)
    if flags == 1:
        plt.clf()
    else:
        flags = 1
    coord_dict = collections.OrderedDict()
    for word in cedwords:
        coord_dict[word] = []
    for day in mds_coords:
        for i in range(len(cedwords)):
            coord_dict[cedwords[i]].append(day[i])
    for j in range(len(cedwords)):
        x = np.array([e[0] for e in coord_dict[cedwords[j]]], dtype='f')
        y = np.array([e[1] for e in coord_dict[cedwords[j]]], dtype='f')
        line = plt.plot(x,y,
                label=cedwords[j])
        plt.quiver(x[:-1], y[:-1], x[1:] - x[:-1], y[1:] - y[:-1], scale_units='xy', angles='xy', scale=1,color=line[0].get_color())

    plt.legend()
    plt.draw()