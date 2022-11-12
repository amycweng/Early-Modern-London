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
    '1 samuel':'1samuel',
    '2 samuel':'2samuel',
    '1 kings':'1kings',
    '2 kings':'2kings',
    '1 chronicles':'1chronicles',
    '2 chronicles':'2chronicles',
    '1 corinthians':'1corinthians',
    '2 corinthians':'2corinthians',
    '1 thessalonians':'1thessalonians',
    '2 thessalonians':'2thessalonians',
    '1 timothy':'1timothy',
    '2 timothy':'2timothy',
    '1 peter':'1peter',
    '2 peter':'2peter',
    '1 john':'1john',
    '2 john':'2john',
    '3 john':'3john'
}

import re 
from bs4 import BeautifulSoup, SoupStrainer

def replaceBible(text):
    for key,value in zip(list(bible.keys()), list(bible.values())):
        variations = key.split(' ')
        for v in variations: 
            text = re.sub(rf'\b{v}\b|\b{v}\.\b|^{v}\.\b|^{v}\b', value, text)
    return text

def replaceNumBook(text):
    for key,value in zip(list(numBook.keys()), list(numBook.values())):
        text = re.sub(rf'\b{key}\b', value, text)
        text = re.sub(r'\s+',' ',text)
    return text

bibleBooks = [x for x in bible.values()]
bibleBooks.extend([x for x in numBook.values()])

def getMarginalia(filepath):
    with open(filepath,'r') as file: 
        data = file.read()
    noteTag = SoupStrainer("note")
    soup = BeautifulSoup(data,parse_only=noteTag,features='html.parser')
    notes_list = []
    special_cases = []
    for note in soup.find_all('note'): 
        n = note.text.lower()
        n = re.sub(r'\s+',' ',n)    
        n = re.sub(r'(?<=\d\.)(?!$)',r' ',n)
        n = replaceBible(n)
        n = replaceNumBook(n)
        if re.search(r'\b[A-Za-z]+. \d+\. \d+\.|\b[A-Za-z]+. \d+ \d+\.|\b[A-Za-z]+. \d+\. \d+|\b[A-Za-z]+. \d+ \d+',n):
            notes = re.findall(r'\b[A-Za-z]+. \d+\. \d+\.|\b[A-Za-z]+. \b \d+ \d+\.|\b[A-Za-z]+. \d+\. \d+|\b[A-Za-z]+. \d+ \d+',n)
            for n in notes:
                if re.search('|'.join(bibleBooks),n): 
                    notes_list.append(n.replace('.',''))
                else: 
                    special_cases.append(n.replace('.',''))

        elif re.search(r'\b[A-Za-z]+. \d+.',n):
            regex_list = [
            '\w+. \d+\. \d+\, \d+\, \d+.','\w+. \d+\. \d+\, \d+.', 
            '\w+. \d+\. \d+\, \d+\, \d+\, \d+.'
            ]
            multiple = False
            for regex in regex_list:
                if re.search(rf'{regex}',n): 
                    found = re.findall(rf'{regex}',n)
                    for f in found:
                        multiple = True
                        f = f.split(' ')
                        for num in f[2:]:
                            phrase = f'{f[0]} {f[1]} {num}'
                            if re.search('|'.join(bibleBooks),phrase):
                                notes_list.append(re.sub('\.|\,','',phrase))
                            else: 
                                special_cases.append(re.sub('\.|\,','',phrase))
            if not multiple: 
                found = re.findall(r'\b[A-Za-z]+. \d+.',n)
                for f in found: 
                    if re.search('|'.join(bibleBooks),f):
                        notes_list.append(re.sub(r'[^a-zA-Z0-9\s\u25CF]','',f))
                    else: 
                        special_cases.append(re.sub(r'[^a-zA-Z0-9\s\u25CF]','',f))
        
    return notes_list,special_cases

if __name__ == '__main__': 
    # sample filepath: /Users/amycweng/Digital Humanities/TCP/P1A0/A01523.P4.xml
    filepath = input('Enter the path of a TCP XML file: ')
    margin, specials = getMarginalia(filepath)
    print(margin)
    missing = []
    for entry in specials: 
        name = re.search(r'\b[A-Za-z]+\b',entry)
        if name is not None: 
            name = name.group()
            if len(name) < 2: continue
            if name not in bibleBooks and name not in missing:
                missing.append(name)
    print(f'Here are the potential Biblical citations that the current standardization dictionary missed: {missing}. Please update the standardizer dictionary accordingly.')

# test1 = 'rom. 12. 12. rom 12.      12. 2 cor 23. 23. 1 tim. 11.11.'
# test2 = '1 cor. 12. 4, 6, 11. 2 cor. 12, 27. 30. eccle 12. 12, 14, 15, 16. 1 sam. 7. 15, 16. iohn 11. , 36. zech. 5. 3, 4.'