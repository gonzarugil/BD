import collections

import sklearn
from sklearn import manifold


def makeRelationsMatrix(ced, allnews):
    relationsmatrix = []
    cedwords = list(ced.keys())
    for i in range(0, len(ced)):
        currentrow = []
        for j in range(0, i + 1):  # We only need half of the matrix due to symmetry
            if i == j:
                currentrow.append(1)
            else:
                currentrow.append(calculaterelation(i, j, cedwords, allnews))
        relationsmatrix.append(currentrow)
    # format relationsmatrix to be a nxn matrix
    formatRelationsMatrix(relationsmatrix)
    return relationsmatrix


def makeCumulativeRelationsMatrixes(ced, allnews):
    buffer = []
    output = []
    for newday in allnews:
        # We store in buffer the days progressively as we calculate the relations of it and store them in output
        buffer.append(newday)
        output.append(makeRelationsMatrix(ced, buffer))
    return output


def calculaterelation(i, j, cedwords, allnews):
    w1 = cedwords[i]
    w2 = cedwords[j]
    w1appearances = 0
    w2appearances = 0
    w1andw2 = 0
    for day in allnews:  # for each day
        for wordlist in day:  # for each new
            if (w1 in wordlist) and (w2 in wordlist):
                w1appearances += 1
                w2appearances += 1
                w1andw2 += 1
            elif w1 in wordlist:
                w1appearances += 1
            elif w2 in wordlist:
                w2appearances += 1
    if (w1andw2 > 0) or (w1appearances > 0) or (w2appearances > 0):
        return 1 - (w1andw2 / (w1appearances + w2appearances - w1andw2))  # Distance matrix varying between 0 and 1
    else:
        return 1


def formatRelationsMatrix(relationsmatrix):
    long = len(relationsmatrix)  # the number of rows
    for i in range(0, len(relationsmatrix)):
        for j in range(len(relationsmatrix[i]), long):
            relationsmatrix[i].append(relationsmatrix[j][i])
    # each term distance(dissimilarity) with itself has to be 0!!
    for k in range(0, len(relationsmatrix)):
        relationsmatrix[k][k] = 0
    relationsmatrix = sklearn.metrics.pairwise_distances(relationsmatrix)
    return relationsmatrix


def calculaterelevance(cedwords, newsdays):
    relevance = collections.OrderedDict()
    for word in cedwords:
        relevance[word] = 0
    for newday in newsdays:
        for new in newday:
            for word in cedwords:
                relevance[word] += new.count(word)
    return relevance


def MakeRelevanceList(cedwords, allnews):
    output = []
    buffer = []
    for newday in allnews:
        # we calculate the cumulative relevance for each day
        buffer.append(newday)
        output.append(calculaterelevance(cedwords, buffer))
    return output


def compute_mds_coords(relationsmatrixes):
    output = []
    for matrix in relationsmatrixes:
        mds = manifold.MDS(n_components=2, metric=True, dissimilarity="precomputed", random_state=6)
        results = mds.fit(matrix)
        coords = results.embedding_
        output.append(coords)
    return output
