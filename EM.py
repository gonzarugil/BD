# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 17:16:57 2015

@author: Gonzalo
"""

# Epsilon defines the rate of attenuation of a word if it doesnt appear the next day
epsilon = 0.8


def setEpsilon(n):
    global epsilon
    epsilon = n


def computeword(word, negativelist, positivelist, ced):
    if word in negativelist:
        return -1.0
    elif word in positivelist:
        return 1.0
        # elif word in ced.keys():
        # return float(ced[word]) The words in ced dont affect to the result to avoid snwoball effect
    else:
        return 0


def computewordlist(wordlist, negativelist, positivelist, ced):
    result = 0
    for word in wordlist:
        result = result + computeword(word, negativelist, positivelist, ced)
    for cedword in ced.keys():
        if cedword in wordlist:
            updateCEDword(cedword, ced, result)  # it doesnt count multiple occurrences of the word
    return result


def computeday(newslist, negativelist, positivelist, ced):
    for new in newslist:
        computewordlist(new, negativelist, positivelist, ced)
    for cedword in ced.keys():
        flag = 0
        for new in newslist:
            if cedword in new:
                flag = 1
        if (flag == 0):
            attenuateCEDword(cedword, ced)


def updateCEDword(word, ced, value):
    ced[word] = ced[word] + value


def attenuateCEDword(word, ced):
    ced[word] = ced[word] * epsilon  # epsilon has to be >0
