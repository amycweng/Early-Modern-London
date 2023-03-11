import os,re
import pandas as pd 

metadataFolder = '/Users/amycweng/Digital Humanities/ECBC-Data-2022/TCP metadata'
sermons = []
patterns = ["sermon",'preached by', 'preached in','preached for','preached before','preached at','preached to',
            "preacht by", "preacht in", "preacht for", "preacht before","preacht at",'preacht to']
move = False
for csvFile in os.listdir(metadataFolder):
    data = pd.read_csv(os.path.join(metadataFolder,csvFile))

    for idx,tcpID in enumerate(data['id']):
        t = data['title'][idx].lower().replace("'",'')
        s = data['keywords'][idx].lower().replace("'",'')
        for pattern in patterns: 
            if re.search(rf'{pattern}', t): 
                sermons.append(tcpID)
                move = True 
                break
            if re.search(rf'{pattern}', s): 
                sermons.append(tcpID)
                move = True
                break
print(len(set(sermons)))

found=0
# EP = '/Users/amycweng/Digital Humanities/eebotcp/texts'
# TCP = '/Users/amycweng/Digital Humanities/TCP'
from getTexts import findText
for s in sermons:
    if 'B43' in s: continue
    if findText(s,False)[1] == 'EP': 
        found += 1 
print(found)
