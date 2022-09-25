from bs4 import BeautifulSoup,SoupStrainer
import re,ast,os

def text(soup):
    text_list = []
    for part in soup.find_all('p'):  
        text = str(part)
        pattern1 = re.compile(r'</seg>', re.DOTALL)
        text = pattern1.sub('',text)
        pattern2 = re.compile(r'</hi>|<hi>', re.DOTALL)
        text = pattern2.sub(' ',text)
        pattern3 = re.compile(r'<note(.*?)place="marg">(.*?)</note>', re.DOTALL)
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
lemmaDict = getLemmaDict('/Users/amycweng/Digital Humanities/ECBC-Data-2022/2b) stageTwo/lemmas.txt')

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

def getfromfolder(inputfolder):
    for file in os.listdir(inputfolder):
        pathName = f'{inputfolder}/{file}'
        tcpid = file[0:6]
        folder = f'{inputfolder}TXT'
        getTextandNotes(pathName,tcpid, folder)

def getTextandNotes(pathname, name,folder):
    print(f'processing {name}')
    data = open(pathname,'r')
    data = data.read()
    bodyTag = SoupStrainer("body")
    soup = BeautifulSoup(data,parse_only=bodyTag,features='html.parser')
    with open(f'{folder}/{name}.txt', 'w+') as file:
        bodytext = text(soup).lower()
        cleaned = cleanText(bodytext)
        bodytext = replaceTextLemma(cleaned,lemmaDict)
        file.write(bodytext) 
    with open(f'{folder}/{name}NOTES.txt',"w+") as file:
        notetext = notes(soup)
        file.write(notetext)

# tcpID = 'A19588'
# TCPfolder = '/Users/amycweng/Digital Humanities/TCP'
# found = False
# for file in os.listdir(f'{TCPfolder}/P1{tcpID[0:2]}'): 
#     if file[0:6] == tcpID: 
#         path = f'{TCPfolder}/P1{tcpID[0:2]}/{tcpID}.P4.xml'
#         found = True
#         break
# if not found: 
#     for file in os.listdir(f'{TCPfolder}/P2{tcpID[0:2]}'):
#         if file[0:6] == tcpID: 
#             path = f'{TCPfolder}/P2{tcpID[0:2]}/{tcpID}.P4.xml'
# getTextandNotes(path,tcpID,'/Users/amycweng/Digital Humanities/')

# getfromfolder('/Users/amycweng/Digital Humanities/charity')
getfromfolder('/Users/amycweng/Digital Humanities/perkins')