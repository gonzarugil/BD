# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 14:08:51 2015

@author: Gonzalo
"""

import matplotlib.pyplot as plt

def plotall(input):
    days = [];
    for day in input:
        days.append(day[0]) #append the string day, this will be the x axis
    words = [];
    for word in input[0][1].keys():
        words.append(word) #append the words, we will draw one graph for each word
    #trying to show just one word
    plt.xticks(range(len(days)),days,color="blue");
    for word in words:
        values = []
        for day in input:
            values.append(day[1][word]) #append the value of the word in each day
        plt.plot(range(len(days)),values, label=word)
        plt.legend( loc="upper left")
    


    plt.show
        