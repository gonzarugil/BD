import csv


def writeCsv(tdm, dayformatted):
    # Esto escribe la matriz en un archivo csv (El cutoff define el numero mínimo de apariciones de cada término)
    tdm.write_csv("csv/" + dayformatted + '.csv', cutoff=1)


def loadcsv(name):
    reader = csv.reader(open(name, 'r', encoding='utf-8'), delimiter=',')
    x = list(reader)
    return x


def writeListToCsv(name, l):
    resultfile = open(name, 'w', encoding='utf-8')
    wr = csv.writer(resultfile, dialect='excel')
    wr.writerow(l)
    return 1


def getListFromCsv(path):
    resultfile = open(path, "r", encoding='utf-8')
    reader = csv.reader(resultfile)
    l = next(reader)
    return l


def loadLexicon(filename):
    txt = open(filename)
    # print ("Loaded %r " % filename)
    return set(txt.read().split())
