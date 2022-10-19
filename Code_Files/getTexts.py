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


EP = '/Users/amycweng/Digital Humanities/eebotcp/texts'
TCP = '/Users/amycweng/Digital Humanities/TCP'
underscores = []
def findText(id,getActs):
    foundEP = False
    for file in os.listdir(f'{EP}/{id[0:3]}'):
        if id in file: 
            foundEP = True                 
            if '_' in file and not getActs:
                trueID = file.split('.')[0]
                if trueID in underscores: path = f'{EP}/{id[0:3]}/{file}'
                else: 
                    path = ''
                    underscores.append(trueID)
            else: 
                path = f'{EP}/{id[0:3]}/{file}'    
    if foundEP:
        return path, 'EP'
    else: 
        # Not in EP, so extract from TCP
        if re.match('B1|B4',id[0:2]):
            path = f'{TCP}/P2{id[0:2]}/{id}.P4.xml'
        else: 
            if f'{id}.P4.xml' in os.listdir(f'{TCP}/P1{id[0:2]}'):
                path = f'{TCP}/P1{id[0:2]}/{id}.P4.xml'
            elif f'{id}.P4.xml' in os.listdir(f'{TCP}/P2{id[0:2]}'): 
                path = f'{TCP}/P2{id[0:2]}/{id}.P4.xml'
        return path, 'TCP'

def textEP(soup):
    '''
    Gets the body of the text file into string format.
    -----------------------------------
    Does not grab any text in the tag <front> which contains div tags such as ['title_page', 'dedication',
    'to_the_reader', 'list'...] that are not part of the main text. 
    Does not grab any text in the tag <back> which contains div tags such as ['errata', 'index', 
    'supplied_by_editor', ...] that are not part of the main text. 
    Does not grab any text under the <table>, <note>, <speaker>, <foreign>, <pc>, <head> or <stage> tags
    Does not grab any text under div type 'coat_of_arms' or attribute 'lat'

    '''
    text_list = []
    for sibling in soup.find_all('w'):
        parent_name = [parent.name for parent in sibling.parents]
        parent_attrs = [parent.attrs for parent in sibling.parents]
        divType = [ats['type'] for ats in parent_attrs if 'type' in ats.keys() and ats['type'] == 'coat_of_arms']
        divLat = [ats['xml:lang'] for ats in parent_attrs if 'xml:lang' in ats.keys() and ats['xml:lang'] == 'lat']
        ignoreTags = ['front', 'table', 'back','foreign','note','speaker','head','stage','pc']
        if not any(x in parent_name for x in ignoreTags) and 'coat_of_arms' not in divType and 'lat' not in divLat and re.search('lemma',str(sibling)) and str(sibling['lemma']) != 'n/a':
            text_list.append(sibling['lemma'])
    return ' '.join(text_list)

def convert(tcpIDs,outputfolder):
    folder = f'/Users/amycweng/Digital Humanities/{outputfolder}'
    count = 0
    for id in tcpIDs:
        path,source = findText(id,False)
        if path == '': continue
        with open(path,'r') as file: 
            data = file.read()
        bodyTag = SoupStrainer("body")
        soup = BeautifulSoup(data,parse_only=bodyTag,features='html.parser')
        if source == 'TCP': 
            print(f'{id} is not in EP')
            bodytext = text(soup).lower()
        if source == 'EP': 
            bodytext = textEP(soup).lower()
            bodytext = re.sub('●','^',bodytext)
        with open(f'{folder}/{id}.txt', 'w+') as file:
            cleaned = cleanText(bodytext)
            bodytext = replaceTextLemma(cleaned,lemmaDict)
            file.write(bodytext) 
        count += 1 
        if not count % 10: print(f'processed {count}')
