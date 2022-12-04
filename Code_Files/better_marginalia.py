bible = {
    'gen gens ge gn genes':'genesis',
    'ex exod exo':'exodus',
    'lev le lv lu leu leuiticus leuit levit':'leviticus',
    'num nu nm numb nb':'numbers',
    'deut de dt':'deuteronomy',
    'josh iosh jos ios jsh ish ioshua iosua':'joshua',
    'judg jdg jg jdgs iudg idg ig idgs iudges': 'judges',
    'ruth rth ru':'ruth',
    'samuell sam sm':'samuel',
    'kin king knig':'kings',
    'chron chr ch':'chronicles',
    'ezr ez':'ezra',
    'neh ne':'nehemiah',
    'est esth es':'esther',
    'job jb iob ib':'job',
    'ps psalm psl pslm psa psm pss psal psalme':'psalms',
    'prov pro prv pr prou pru prouerb prouerbs':'proverbs',
    'eccles eccl eccle ecc ec ecls qoh':'ecclesiastes',
    'cant cantic canticle cantica':'canticles',
    'isa isai isay es esi esa esai esay esaiae':'isaiah',
    'jer je jr ier ie ir ieremiah ierem jerem':'jeremiah',
    'lam la lament':'lamentations',
    'ezek eze ezk ezech ezck':'ezekiel',
    'dan da dn':'daniel',
    'hos ho hoshea hosh':'hosea',
    'jl ioel il':'joel',
    'am':'amos',
    'obad ob':'obadiah',
    'jnh jon ion inh ionah jona':'jonah',
    'mic mc':'micah',
    'na nah':'nahum',
    'hab hb':'habakkuk',
    'zeph zep zp':'zephaniah',
    'hag hg':'haggai',
    'zech zec zc':'zechariah',
    'mal ml malac':'malachi',
    'matt matth mt math mat':'matthew',
    'mrk mar mk mr':'mark',
    'luk lk luc lc':'luke',
    'joh jhn ioh ihn iohn':'john',
    'act ac acta':'acts',
    'rom ro rm':'romans',
    'cor co cr or':'corinthians',
    'gal ga galat':'galatians',
    'eph ephes ephe ephs':'ephesians',
    'phil php pp phillip philip':'philippians',
    'col coloss':'colossians',
    'thess thes th thss':'thessalonians',
    'tim ti':'timothy',
    'tit ti':'titus',
    'philem phm pm':'philemon',
    'heb hebr':'hebrews',
    'jas jm iam ias im iames jam':'james',
    'pet pe pt p petr':'peter',
    'jud jd iud id iude':'jude',
    'rev re reu reuelation reuel reuelations':'revelation',
    'apoc apo apoc': 'apocrypha',
    'tob tobi':'tobit',
    'jth jdth jdt ith idth idt iudith':'judith',
    'ecclus':'ecclesiasticus',
    'bar':'baruch',
    'ep epist epist':'epistle'
}

numBook = {
    '1 samuel':'onesamuel',
    '2 samuel':'twosamuel',
    '1 kings':'onekings',
    '2 kings':'twokings',
    '1 chronicles':'onechronicles',
    '2 chronicles':'twochronicles',
    '1 corinthians':'onecorinthians',
    '2 corinthians':'twocorinthians',
    '1 thessalonians':'onethessalonians',
    '2 thessalonians':'twothessalonians',
    '1 timothy':'onetimothy',
    '2 timothy':'twotimothy',
    '1 peter':'onepeter',
    '2 peter':'twopeter',
    '1 john':'onejohn',
    '2 john':'twojohn',
    '3 john':'threejohn'
}

import re 
from bs4 import BeautifulSoup, SoupStrainer

def replaceBible(text):
    for key,value in zip(bible.keys(), bible.values()):
        variations = key.split(' ')
        for v in variations: 
            text = re.sub(rf'\b{v}\b|\b{v}\.\b|^{v}\.\b|^{v}\b', value, text)
    return text

def replaceNumBook(text):
    for key,value in zip(numBook.keys(), numBook.values()):
        text = re.sub(rf'\b{key}\b', value, text)
        text = re.sub(r'\s+',' ',text)
    return text

bibleBooks = [x for x in bible.values()]
bibleBooks.extend([x for x in numBook.values()])
original_titles = {v.capitalize():k for k,v in numBook.items()}


def verify(text): 
    for book in bibleBooks:
        if re.search(rf'{book} \d+', text): 
            return True
        
def getMarginalia(filepath):
    with open(filepath,'r') as file: 
        data = file.read()
    noteTag = SoupStrainer("note")
    soup = BeautifulSoup(data,parse_only=noteTag,features='html.parser')
    possible_citations = []
    possible_missing = []
    for note in soup.find_all('note'): 
        n = note.text.lower()
        n = re.sub(r'(\.)',r' ',n)
        n = re.sub(r'\s+',' ',n)
        n = replaceBible(n)
        n = replaceNumBook(n)
        if verify(n): 
            possible_citations.append(n)
        else: 
            possible_missing.append(n)
            
    margins = findCitations(possible_citations)
    special_cases = findMissing(possible_missing)
    return margins,special_cases

def comma(book, passage): 
    phrases = []
    edge_case = re.search(', \d+ \d+',passage)
    if edge_case: 
        phrases.append(simple(book, edge_case.group()))
        passage = re.sub(edge_case.group(), '',passage)
    nums = re.findall(f'(\d+)',passage)
    for num in nums[1:]: 
        phrases.append(f'{book} {nums[0]}:{num}')
    return phrases 

def simple(book, passage): 
    passage = re.findall('(\d+) (\d+)',passage)[0]
    return f'{book} {passage[0]}:{passage[1]}'

def findCitations(notes_list): 
    citations, outliers = [], []

    for n in notes_list: 
        phrases, pesky = [], []
        n = re.sub(r'(\.)',r' ',n)
        n = re.sub(r'[^A-Za-z0-9\,\& ]','',n)
        n = re.sub(r'\s+',' ',n)
        n = replaceBible(n)
        n = replaceNumBook(n)
        for book in bibleBooks:
            phrase = re.search(rf'\b{book}\b(.*?)(?=[a-z])|\b{book}\b(.*?)$',n)
            if phrase is None: continue
            phrase = phrase.group().strip()
            if not re.search(r'[a-z]+ \d+ \d+',phrase): continue
            
            if re.search(r'^[a-z]+ \d+ \d+$',phrase):  
                phrases.append(simple(book, phrase))
            elif re.search(r'^[a-z]+ \d+ \d+ \d+$',phrase):  
                phrase = phrase.split(' ')
                phrases.append(f'{phrase[0]} {phrase[1]}:{phrase[2]}')
                phrases.append(f'{phrase[0]} {phrase[1]}:{phrase[3]}')
            elif re.search('&',phrase): 
                passages = phrase.split('&')
                for passage in passages: 
                    passage = passage.strip()
                    if re.search(',',passage):
                        phrases.extend(comma(book, passage))
                    else:
                        phrases.append(simple(book, passage))
            elif re.search(', ',phrase): 
                phrases.extend(comma(book, phrase))
            else: 
                pesky.append(phrase)

            for phrase in phrases:
                citations.append(phrase.capitalize())
            for p in pesky: 
                outliers.append(p.capitalize())

    return citations, outliers

def findMissing(missing_list): 
    special_cases = []
    for m in missing_list: 
        if re.search('\w+ \d+ \d+',m): 
            missing = re.findall('\w+ \d+ \d+',m)
            for phrase in missing: 
                special_cases.append(phrase)
    return sorted(special_cases)

def proper_title(citations_list, pesky_list): 
    for idx, passage in enumerate(citations_list): 
        book = passage.split(' ')[0]
        if book in original_titles.keys():
            orig_title = original_titles[book].split(' ')
            orig_title[1] = orig_title[1].capitalize()
            passage = re.sub(book, ' '.join(orig_title), passage)
            citations_list[idx] = passage

    for idx, passage in pesky_list: 
        book = passage.split(' ')[0]
        if book in original_titles.keys():
            orig_title = original_titles[book].split(' ')
            orig_title[1] = orig_title[1].capitalize()
            passage = re.sub(book, ' '.join(orig_title), passage)
            pesky_list[idx] = passage

    return citations_list, pesky_list 

import warnings
warnings.simplefilter("ignore", UserWarning)

if __name__ == '__main__': 
    # sample filepath: /Users/amycweng/Digital Humanities/TCP/P1A6/A68088.P4.xml
    filepath = input('Enter the path of a TCP XML file: ')
    margin, possibly_missing = getMarginalia(filepath)
    margin = proper_title(margin[0], margin[1])
    print(f'Here are the biblical passages cited in the margins of this book and formatted as singular lines: {margin[0]}\n')
    print(f'Here are the citations that cannot be formatted at the moment: {margin[1]}\n')
    print(f'Here are the potential Biblical passages that the current standardization dictionary missed: {possibly_missing}. Please update the standardizer dictionary accordingly.')