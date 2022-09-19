from bs4 import BeautifulSoup,SoupStrainer
import re,ast,os
from bible import bible, numBook

def text(soup):
    text_list = []
    for part in soup.find_all('p'):  
        text = str(part)
        pattern1 = re.compile(r'</seg>', re.DOTALL)
        text = pattern1.sub('',text)
        pattern2 = re.compile(r'</hi>|<hi>', re.DOTALL)
        text = pattern2.sub(' ',text)
        pattern3 = re.compile(r'<note place="marg">(.*?)</note>', re.DOTALL)
        text = pattern3.sub(' ',text)
        pattern4 = re.compile(r'<.*?>|\n', re.DOTALL)
        text = pattern4.sub(' ',text)
        text = text.strip()
        text_list.append(text)   
    return ' '.join(text_list)

def notes(soup):
    notes_list = []
    for note in soup.find_all('note'): 
        n = note.text
        n = re.sub(r'[^a-zA-Z0-9 ]','',n)
        notes_list.append(n)
    return '\n'.join(notes_list)

def cleanText(text):    
    dashes = text.replace('-',' ')
    tokens = [x for x in re.sub(r'[^a-zA-Z\s\u25CF]','', dashes).split(' ') if x != '']
    tokens = ' '.join(tokens)
    tokens = tokens.replace('  ',' ')
    return tokens
    
def getLemmaDict(path):
    with open(path) as f:
        data = f.read()
    lemmaDict = ast.literal_eval(data)
    print(type(lemmaDict))
    return lemmaDict

def replaceTextLemma(textString,lemmaDict):
    for key,value in zip(list(lemmaDict.keys()), list(lemmaDict.values())):
        textString = re.sub(rf' {key} ', f' {value} ', textString)
    return textString

def replaceBible(text,bibledict):
    for key,value in zip(list(bibledict.keys()), list(bibledict.values())):
        variations = key.split(' ')
        for v in variations: 
            text = re.sub(rf'\b{v}\b| {v} ', f' {value} ', text)
    return text

def replaceNumBook(text,numBook):
    for key,value in zip(list(numBook.keys()), list(numBook.values())):
        text = re.sub(rf'\b{key}\b| {key} ', f' {value} ', text)
    return text


for file in os.listdir('perkins'):
    pathName = f'/Users/amycweng/Digital Humanities/perkins/{file}'
    name = file[0:6]
    print(f'processing {name}')
    data = open(pathName,'r')
    data = data.read()
    bodyTag = SoupStrainer("body")
    soup = BeautifulSoup(data,parse_only=bodyTag,features='html.parser')
    lemmaDict = getLemmaDict('/Users/amycweng/Digital Humanities/ECBC-Data-2022/2b) stageTwo/lemmas.txt')
    with open(f'perkinsTXT/{name}.txt', 'w+') as file:
        bodytext = text(soup).lower()
        bodytext = replaceBible(bodytext,bible)
        bodytext = replaceNumBook(bodytext,numBook)
        cleaned = cleanText(bodytext)
        bodytext = replaceTextLemma(cleaned,lemmaDict)
        file.write(bodytext) 
    # with open(f'perkinsTXT/{name}NOTES.txt',"w+") as file:
    #     notetext = notes(soup)
    #     file.write(notetext)
 