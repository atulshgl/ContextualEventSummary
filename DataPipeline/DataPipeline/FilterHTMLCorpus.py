from bs4 import BeautifulSoup
import os
import io 
import json
from urllib.request import urlopen

current_path = os.path.dirname(os.path.realpath(__file__))
relative_path = "\spanish\\"
datasource_path = current_path + relative_path
webpage = ''
filteredDataCorpus = []

def filterEventLine(unfilteredLine):
    if (unfilteredLine.find('<sup>') > -1): 
        return ''

    timeTagStartIndex = unfilteredLine.find('<ttag>')
    if (timeTagStartIndex > - 1):
       timeTagEndIndex = unfilteredLine.find('</ttag>')
       return unfilteredLine[timeTagStartIndex+7: timeTagEndIndex-1]

    eventTagStartIndex = unfilteredLine.find('<etag>')
    if (eventTagStartIndex > -1):
        eventTagEndIndex = unfilteredLine.find('</etag>')
        return unfilteredLine[eventTagStartIndex+7 : eventTagEndIndex-1]
    
    return unfilteredLine

for file in os.listdir(datasource_path):
    if file.endswith(".html"):
        filename = os.path.join(datasource_path, file)
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                webpage = f.read()
        except:
             print('Encoding error in doc: ' + filename)

        bs = BeautifulSoup(webpage)
        corpusLine = bs.find_all("p", class_="line")
        for line in corpusLine:
            tempFilteredLineHolder = []
            tempTaggedLineHolder = []
            for unfilteredLine in line.contents:
                filteredContent = filterEventLine(str(unfilteredLine))
                tempFilteredLineHolder.append(filteredContent)
                tempTaggedLineHolder.append(str(unfilteredLine))

            filteredDataCorpus.append( { 'filteredLine': ''.join(tempFilteredLineHolder), 'originalLine': ''.join(tempTaggedLineHolder)})

with open('eventData.txt', 'w', encoding='utf-8') as outfile:
    json.dump(filteredDataCorpus, outfile)

