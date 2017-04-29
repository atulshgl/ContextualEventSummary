# -*- coding: utf-8 -*-
import codecs, sys
import xml.etree.ElementTree as ET
from lxml import etree
from BeautifulSoup import BeautifulSoup
from difflib import SequenceMatcher

trainingFile = sys.argv[1]

def readInput(filepath):
    with codecs.open(filepath, 'r', 'utf-8') as f:
        text = u''
        lines = f.readlines()
        for line in lines:
            text += line.strip()
    return text

def extractEvents(text):
    events = []
    for article in ET.fromstring(text):
        for text in article:
            if text.tag == 'text':
                e = {}
                for event in text:
                    if event.tag in e.keys():
                        e[event.tag] += ' ' + event.text
                    else:
                        e[event.tag] = event.text
                events.append(e)
    return events

def getEventList(events):
    eventList = []
    for article in events:
        x = []
        for tag, event in article.iteritems():
            x.append(event)
        eventList.append(x)
    return eventList

def getSummaryList(text):
    summary = []
    for article in ET.fromstring(text):
        for text in article:
            if text.tag == 'summary':
                summary.append(text.text)
    return summary


def substringSieve(string_list):
    string_list.sort(key=lambda s: len(s), reverse=True)
    out = []
    for s in string_list:
        if not any([s in o for o in out]):
            out.append(s)
    return out

def getTextFromXML(filepath):
    tree = etree.parse(filepath)
    notags = etree.tostring(tree, encoding='utf8', method='text')
    return notags

def removeTags(text):
    return ''.join(ET.fromstring(text).itertext())

def getListFromXML(text,label):
    articles = []
    tree = etree.fromstring(text)
    articleText = tree.xpath('//' + label)
    
    for at in articleText:
        if at.text:
            aText = (at.text + ''.join(map(etree.tostring, at))).strip()
            aText = ('<' + label + '>' + aText + '</' + label + '>').encode('utf-8')
            cleantext = removeTags(aText)
            articles.append(cleantext)
  
    return articles

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def matchEvents(str1, str2):
    if str1 in str2:
        return True
    elif str2 in str1:
        return True
    elif similar(str1,str2) >= 0.25:
        return True
    return False
    
def f1Score(predictedEvents,taggedEvents):
    pn, tn = len(predictedEvents), len(taggedEvents)
    t = [0]*tn
    p = [0]*pn
    
    for i in range(tn):
        for j in range(pn):
            if p[j]==0 and matchEvents(taggedEvents[i],predictedEvents[j]):
                t[i] = 1
                p[j] = 1
                break
        
    truePositive = sum(t)
    falsePositive = pn - sum(p)
    falseNegative = tn - truePositive
    trueNegative = None

    precision = truePositive / float(pn)
    recall = truePositive / float(tn)

    print '#predictedEvents', '#taggedEvents'
    print pn, tn
    print ''
    print 'truePositive', 'falsePositive', 'falseNegative', 'trueNegative'
    print truePositive, falsePositive, falseNegative, trueNegative
    print ' '
    print 'precision', 'recall'
    print precision, recall
    print ''
    if precision + recall > 0:
        F1 = 2*(precision * recall) / (precision + recall)
    else:
        F1 = None
    return F1, [truePositive, tn, pn]


def getF1Score(truePositive, tn, pn):
    precision = truePositive / float(pn)
    recall = truePositive / float(tn)


    print 'precision', 'recall'
    print precision, recall
    print ''
    if precision + recall > 0:
        F1 = 2*(precision * recall) / (precision + recall)
    else:
        F1 = None
    return F1

'''
driver code:

text = readInput(trainingFile)

events = extractEvents(text.encode('utf-8'))

corpus = getTextFromXML(trainingFile)

articles = getListFromXML(text.encode('utf-8'))
    
for a in articles:
    print 'article x:'
    print a
    print ''

for e in events:
    print 'article y:'
    for tag,line in e.iteritems():
        print tag, line
'''
