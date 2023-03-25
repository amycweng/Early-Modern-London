'''
@author Amy Weng 

This code extracts biblical citations from the marginal notes, i.e., marginalia, encoded in TCP XML files under the <note> tags. 

Takes in a single TCP XML file and outputs the following:
    1. A list of singular citations (i.e., "<book> <chapter> <line>"), 
    2. A list of citations that cannot be properly formatted by the current code, and 
    3. A list of possible citations, i.e., "<word> <int1> <int2>" where <word> is not found in the standardizer bible dictionary. The standardizer dict can then be updated accordingly. 
'''
import re 
from bs4 import BeautifulSoup, SoupStrainer
from collections import Counter

# Dictionary that maps the abbreviatons of Bible books to their full titles for standardization purposes
bible = {
    'gen gens ge gn genes gene':'genesis',
    'ex exod exo':'exodus',
    'lev le lv lu leu leuiticus leuit levit':'leviticus',
    'num nu nm numb nb':'numbers',
    'deut de dt deu deuter dut':'deuteronomy',
    'josh iosh jos ios jsh ish ioshua iosua josua iosu':'joshua',
    'judg jdg jg jdgs iudg idg ig idgs iudges': 'judges',
    'ruth rth ru':'ruth',
    'samuell sam sm':'samuel',
    'kin king knig kinges':'kings',
    'chron chr ch chro':'chronicles',
    'ezr ez':'ezra',
    'neh ne nehem nehe':'nehemiah',
    'est esth es ester':'esther',
    'job jb iob ib':'job',
    'ps psalm psl pslm psa psm pss psal psalme psol':'psalms',
    'prov pro prv pr prou pru prouerb prouerbs pou pov proverb':'proverbs',
    'eccles eccl eccle ecc ec ecls ecles eccls eecles':'ecclesiastes',
    'cant cantic canticle cantica carm':'canticles',
    'isa isai isay es esi esa esai esay esaiae esal':'isaiah',
    'jer je jr ier ie ir ieremiah ierem erem jerem ierm iere':'jeremiah',
    'lam la lament lamnt':'lamentations',
    'ezek eze ezk ezech ezck ezec':'ezekiel',
    'dan da dn':'daniel',
    'hos ho hoshea hosh hose hsea hsh':'hosea',
    'jl ioel il':'joel',
    'am':'amos',
    'obad ob':'obadiah',
    'jnh jon ion inh ionah jona iona':'jonah',
    'mic mc mica micha':'micah',
    'na nah':'nahum',
    'hab hb habb habbak habba habbac habac abakk':'habakkuk',
    'zeph zep zp zephan':'zephaniah',
    'hag hg hagg':'haggai',
    'zech zec zc zch zach zachar zac':'zechariah',
    'mal ml malac malach mala':'malachi',
    'matt matth mt math mat mattth mattb':'matthew',
    'mrk mar mk mr marc marke':'mark',
    'luk lk luc lc':'luke',
    'joh jhn ioh ihn iohn ioan joan':'john',
    'act ac acta':'acts',
    'rom ro rm roman':'romans',
    'cor co cr or corinth corin':'corinthians',
    'gal ga galat':'galatians',
    'eph ephes ephe ephs ehes':'ephesians',
    'phil php pp phillip philip hilip phi':'philippians',
    'col coloss colos':'colossians',
    'thess thes th thss thoss':'thessalonians',
    'tim timoth tom timo':'timothy',
    'tit tius':'titus',
    'philem phm pm':'philemon',
    'heb hebr':'hebrews',
    'jas jm iam iams ias im iames jam iaes':'james',
    'pet pe pt p petr':'peter',
    'jud jd iud id iude':'jude',
    'rev re reu reuelation reuel reuelations reve revel':'revelation',
    'tob tobi':'tobit',
    'jth jdth jdt ith idth idt iudith':'judith',
    'ecclus':'ecclesiasticus',
    'bar':'baruch',
    'ep epist epist':'epistle'
}

# Turn the numbered books into one word for convenience in later regex tasks 
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

'''Standardizes known abbreviations'''
def replaceBible(text):
    for key,value in bible.items():
        variations = key.split(' ')
        variations.append(value)
        for v in variations: 
            if re.search(rf'\b{v}\b|^{v}\b', text): 
                return True,re.sub(rf'\b{v}\b|^{v}\b', value, text)
    return False,text

'''Converts numbered books into a single string, e.g., '1 corinthians' to '1corinthians' for ease of processing'''
def replaceNumBook(text):
    for key,value in numBook.items():
        if key in text: 
            return re.sub(rf'{key}', value, text)
    return None

# Get all of the names of the Bible's books 
bibleBooks = [x for x in bible.values()]
bibleBooks.extend([x for x in numBook.values()])

'''Master function to extract all the citations from the marginalia of one file.''' 
def getMarginalia(filepath):
    # read the input XML file 
    with open(filepath,'r') as file: 
        data = file.read()
    # use soupstrainer to only parse the main text body (excluding dedicatory materials etc)
    # each xml file only has one of these, so there will only be one none-empty soup for each file 
    bodyText1 = SoupStrainer("div1",attrs={"type":"text"})
    bodyText2 = SoupStrainer("div1",attrs={"type":"part"})
    bodyText3 = SoupStrainer("div1",attrs={"type":"sermon"})
    bodyText4 = SoupStrainer("div1",attrs={"type":"exegesis"})
    # create a parsed tree, i.e., soup, of the body text using the html parser
    # (the file is an XML but the HTML parser is sufficient.)
    soup1 = BeautifulSoup(data,parse_only=bodyText1,features='html.parser')
    soup2 = BeautifulSoup(data,parse_only=bodyText2,features='html.parser')
    soup3 = BeautifulSoup(data,parse_only=bodyText3,features='html.parser')
    soup4 = BeautifulSoup(data,parse_only=bodyText4,features='html.parser')
    # only one of these soups will actually have content 
    soups = [soup1, soup2,soup3,soup4]
    # phrases with known scriptural abbreviations 
    citations = []
    # phrases with unknown abbreviations 
    unknown = []
    # iterate through every note tag of this file 
    for soup in soups: 
        for note in soup.find_all('note'): 
            # make all letters lowercase
            n = note.text.lower()
            # replace all periods with spaces. This is to make sure that all citations are 
            # in the format of "<book> <chapter> <line>", i.e., "Ecclesiastes 9 4". 
            # Some citations are originally inconsistently formatted as "<book> <chapter>.<line>" at times 
            # and "<book> <chapter>. <line>." at other times, so replacing periods with spaces is the first step to standardizing all the citation formats 
            n = re.sub(r'(\.)',r' ',n)
            # remove everything that is not an alphabetical character, integer, comma, ampersand or a single space
            n = re.sub(r'[^a-z0-9\,\&\— ]','',n)
            # replace all instances of "and" with ampersands 
            n = re.sub(r'\band\b','&', n)
            # next, replace all instances of two or more spaces with a single space. 
            n = re.sub(r'\s+',' ',n)

            # find instances of possible numbered books 
            pattern1 = re.findall(rf'([1|2|3] [a-z]+ [^a-z]+)',n)
            if len(pattern1) > 0: 
                for item in pattern1: 
                    if re.search(rf'\d+ \d+',item): 
                        found, standard = replaceBible(item)
                        # if there is a known abbreviation, standardize and append to appropriate list  
                        if found: 
                            standard = replaceNumBook(standard)
                            # delete the current instance from the entire string
                            # this prevents repeats when we process pattern2 citations below  
                            n = re.sub(item,' ',n) 
                            citations.append(standard)
                        else: 
                            # there is an unknown abbreviation
                            item = item.split(' ')
                            unknown.append(item[1])

            # find instances of other scriptural citations 
            pattern2 = re.findall(rf'([a-z]+ [^a-z]+)', n)
            if len(pattern2) > 0: 
                for item in pattern2: 
                    if re.search(rf'\d+ \d+',item): 
                        found, standard = replaceBible(item) 
                        # if there is a known abbreviation, standardize and append to appropriate list  
                        if found and standard:
                            citations.append(standard)
                        else: 
                            # there is an unknown abbreviation
                            item = item.split(' ')
                            unknown.append(item[0])
    # call another function to actually return a list of actual scriptural citations 
    citations = findCitations(citations)
    # return both the list of citations and unknown abbreviations
    return citations,Counter(unknown)

'''
Helper function to extract citations from a marginal note that contains commas 
(i.e., multiple line citations from the same chapter of the same book)
'''

def comma(book, passage): 
    # initialize a list of citations 
    phrases = []
    if re.search('\-', passage):
        passage = re.sub(' -|- ','-',passage)
        passage = re.sub('\,-','-',passage)
        edge_cases = re.findall(', (\d+ \d+-\d+)$|, (\d+ \d+-\d),',passage)
        # if there are hyphens indicating range of citations, 
        # e.g., "2 Kings 1 2-4" -->"2 Kings 1:2", "2 Kings 1:3", & "2 Kings 1:4"
        if len(edge_cases) > 0: 
            for tuple in edge_cases:
                if tuple[0] != '':  edge_case = tuple[0]
                else: edge_case = tuple[1]
                phrases.extend(hyphen(book,edge_case))
                # erase the passage from consideration
                passage = re.sub(edge_case, '',passage)
        else: 
            # case of discrete citations, e.g., "Psalms 1 2 - 3 4" --> "Psalms 1:2" and "Psalms 3:4"
            # i.e., "2 King. 6. 22.—9. 24.—13 15." --> "2 Kings 6:22", "2 Kings 9:24" and "2 Kings 13:15"
            passages = passage.split('—')
            for case in passages: 
                nums = re.findall(r'\d+',case)
                phrases.append(f'{book} {nums[0]}:{nums[1]}')
    # the remaining cases are those that are like "isaiah 1 2, 3, 4, 5 5"
    # which this code turns into "isaiah 1:2", "isaiah 1:3", "isaiah 1:4", "Isaiah 5:5"
    # find all the integers 
    passage = re.sub(rf'{book}| ,','',passage).strip()
    nums = passage.split(' ')
    chapter,line = nums[0],0
    for num in nums[1:]: 
        if ',' in num: 
            line = num 
            phrases.append(f'{book} {chapter}:{line}')
        else: 
            chapter = num
    return phrases  

'''
Helper function to extract citations from a marginal note that does not contain commas

Target format is "<book> <chapter> <line>" 
'''
def simple(book, passage): 
    # the simple case of just having "<book> <chapter> <line>" 
    nums = re.findall('\d+',passage)
    return f'{book} {nums[0]}:{nums[1]}'

'''
Helper function to extract citations from a marginal note that does not contain commas
Target format is "<book> <chapter> <line1> <line2>" or "<book> <chapter1> <line1> <chapter2> <line2>" 
    or "<book> <chapter> <line1> <line2> <line3> <line4>" 
'''
def othersimple(book, passage): 
    phrases = []
    if re.search('\d+ \d+ \d+ \d+ \d+', passage): 
        passage = re.findall('(\d+) (\d+) (\d+) (\d+) (\d+)',passage)[0]
        phrases.append(f'{book} {passage[0]}:{passage[1]}')
        phrases.append(f'{book} {passage[0]}:{passage[2]}')
        phrases.append(f'{book} {passage[0]}:{passage[3]}')
        phrases.append(f'{book} {passage[0]}:{passage[4]}')
    elif re.search('\d+ \d+ \d+ \d+', passage): 
        passage = re.findall('(\d+) (\d+) (\d+) (\d+)',passage)[0]
        phrases.append(f'{book} {passage[0]}:{passage[1]}')
        phrases.append(f'{book} {passage[2]}:{passage[3]}')
    else: 
        passage = re.findall('(\d+) (\d+) (\d+)',passage)[0]
        phrases.append(f'{book} {passage[0]}:{passage[1]}')
        phrases.append(f'{book} {passage[0]}:{passage[2]}')
    return phrases 

'''
Helper function to extract citations from a marginal note that contains hyphens 

These are cases of continuous citation, 
e.g, "Genesis 3 9-14" --> "Genesis 3:9", "Genesis 3:10", etc. until "Genesis 3:14"
'''
def hyphen(book, phrase):
    phrases = [] 
    nums = re.findall(r'\d+',phrase)
    chapter, start, end = nums[0], int(nums[1]), int(nums[2])
    for idx in range(end-start+1): 
        phrases.append(f'{book} {chapter}:{start+idx}')
    return phrases


'''Main function to actually extract all of the Biblical citations'''
def findCitations(notes_list): 
    # initialize lists to keep track of the properly formatted citations and possible formats that this code cannot currently account for 
    citations, outliers = [], []

    # iterate through every single item of the notes_list
    for phrase in notes_list: 
        if phrase == None: continue
        phrase = phrase.strip()
        # if there is no instance of the book followed by at least two decimals, skip to the next instance   
        if not re.search(r'[a-z]+ \d+ \d+',phrase): continue
        
        book = phrase.split(' ')[0]
        # if the note is simply a single citation, call simple() to append the citation to the list of citations 
        if re.search(r'[a-z]+ \d+ \d+$',phrase):  
            citations.append(simple(book, phrase))
        elif re.search(r'^[a-z]+ \d+ \d+ \d+$|^[a-z]+ \d+ \d+ \d+ \d+$|^[a-z]+ \d+ \d+ \d+ \d+ \d+$',phrase):  
            citations.extend(othersimple(book, phrase))
        # if there are ampersands in the note, split the note up by the ampersands 
        elif re.search('&',phrase): 
            passages = phrase.split('&')
            for passage in passages: 
                passage = passage.strip()
                # call comma() if the substring as a comma 
                if re.search(',',passage):
                    citations.extend(comma(book, passage))
                else:
                    if re.search(r'\-',passage): 
                        phrase = re.sub(' -|- ','-',phrase)
                        phrase = re.sub('\,-','-',phrase)
                        if re.search(r'[a-z]+ \d+ \d+—\d+$',phrase): 
                            # if there are hyphens indicating range of citations, 
                            # e.g., "2 Kings 1 2-4" -->"2 Kings 1:2", "2 Kings 1:3", & "2 Kings 1:4"
                            citations.extend(hyphen(book, phrase))
                        else: 
                            # case of discrete citations, e.g., "Psalms 1 2 - 3 4" --> "Psalms 1:2" and "Psalms 3:4"
                            # i.e., "2 King. 6. 22.—9. 24.—13 15." --> "2 Kings 6:22", "2 Kings 9:24" and "2 Kings 13:15"
                            passages = phrase.split('—')
                            for case in passages: 
                                nums = re.findall(r'\d+',case)
                                citations.append(f'{book} {nums[0]}:{nums[1]}')
                    # call othersimple() to account for the case of "<chapter> <line1> <line2>" 
                    elif re.search(r'\d+ \d+ \d+', passage): 
                        citations.extend(othersimple(book, passage))
                    
                    # call simple() to account for "<chapter> <line1>"
                    elif re.search(r'\d+ \d+$',passage): 
                        citations.append(simple(book, passage))
        # if there are no ampersands, call comma() to account for the multiple citations of the same chapter 
        elif re.search(',',phrase): 
            citations.extend(comma(book, phrase))
        # if there are no commas and ampersands but there are hyphens
        elif re.search(r'\—',phrase):
            phrase = re.sub(' -|- ','-',phrase)
            phrase = re.sub('\,-','-',phrase)
            if re.search(r'[a-z]+ \d+ \d+—\d+$',phrase): 
                citations.extend(hyphen(book, phrase))
            else: 
                passages = phrase.split('—')
                for case in passages: 
                    if re.search('\d+ \d+', case):
                        nums = re.findall('\d+',case)
                        citations.append(f'{book} {nums[0]}:{nums[1]}')
        # else, there is a format that this code cannot account effectively for 
        else: 
            # hard coding some special cases for the charity sermons dataset
            if 'psalms 119 5 10 32 57 93 106 173 40' in phrase: 
                # original is Psal 119.5 10.32.57.93.106 173.40.
                citations.extend(['psalms 119:5', 'psalms 10:32', 'psalms 10:57','psalms 10:93','psalms 10:106', 'psalms 173:40'])
            elif 'romans 8 1 3 5 8 9' in phrase: 
                # original is Rm. 8.1.3 5.8.9
                citations.extend(['romans 8:1','romans 8:2', 'romans 8:3', 'romans 5:8', 'romans 5:9'])
            else: 
                outliers.append(phrase)
    # pretty formatting 
    citations, outliers = proper_title(citations, outliers)
    # return both citations and outliers  
    return citations, outliers

'''Convert the numbered books back into their original formats, i.e., "Onecorinthians" to "1 Corinthians"'''
def proper_title(citations_list, pesky_list): 
    for idx, citation in enumerate(citations_list):
        citation = re.sub(f'\,','',citation)
        citation = citation.split(' ') 
        book = citation[0]
        if re.search('one',book):
            book = re.sub('one','',book)
            citations_list[idx] = f'1 {book.capitalize()} {citation[1]}'
        elif re.search('two',book):
            book = re.sub('two','',book)
            citations_list[idx] = f'2 {book.capitalize()} {citation[1]}'
        elif re.search('three',book):
            book = re.sub('three','',book)
            citations_list[idx] = f'3 {book.capitalize()} {citation[1]}'
        else: 
            citations_list[idx] = f'{book.capitalize()} {citation[1]}'

    for idx, citation in enumerate(pesky_list): 
        citation = re.sub(f'\,','',citation)
        citation = citation.split(' ') 
        book = citation[0]
        if re.search('one',book):
            book = re.sub('one','',book)
            pesky_list[idx] = f'1 {book.capitalize()} {citation[1]}'
        elif re.search('two',book):
            book = re.sub('two','',book)
            pesky_list[idx] = f'2 {book.capitalize()} {citation[1]}'
        elif re.search('three',book):
            book = re.sub('three','',book)
            pesky_list[idx] = f'3 {book.capitalize()} {citation[1]}'
        else: 
            pesky_list[idx] = f'{book.capitalize()} {citation[1]}'
    return citations_list, pesky_list 