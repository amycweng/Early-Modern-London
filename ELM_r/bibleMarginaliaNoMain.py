'''
This code extracts biblical citations from the marginal notes, i.e., marginalia, encoded in TCP XML files under the <note> tags. 

Takes in a single TCP XML file and outputs the following:
    1. A list of singular citations (i.e., "<book> <chapter> <line>"), 
    2. A list of citations that cannot be properly formatted by the current code, and 
    3. A list of possible citations, i.e., "<word> <int1> <int2>" where <word> is not found in the standardizer bible dictionary. The standardizer dict can then be updated accordingly. 
'''
import re 
from bs4 import BeautifulSoup, SoupStrainer

# Dictionary that maps the abbreviatons of Bible books to their full titles for standardization purposes
bible = {
    'gen gens ge gn genes gene':'genesis',
    'ex exod exo':'exodus',
    'lev le lv lu leu leuiticus leuit levit':'leviticus',
    'num nu nm numb nb':'numbers',
    'deut de dt deu deuter':'deuteronomy',
    'josh iosh jos ios jsh ish ioshua iosua josua':'joshua',
    'judg jdg jg jdgs iudg idg ig idgs iudges': 'judges',
    'ruth rth ru':'ruth',
    'samuell sam sm':'samuel',
    'kin king knig kinges':'kings',
    'chron chr ch chro':'chronicles',
    'ezr ez':'ezra',
    'neh ne nehem nehe':'nehemiah',
    'est esth es ester':'esther',
    'job jb iob ib':'job',
    'ps psalm psl pslm psa psm pss psal psalme':'psalms',
    'prov pro prv pr prou pru prouerb prouerbs pou pov proverb':'proverbs',
    'eccles eccl eccle ecc ec ecls ecles':'ecclesiastes',
    'cant cantic canticle cantica carm':'canticles',
    'isa isai isay es esi esa esai esay esaiae':'isaiah',
    'jer je jr ier ie ir ieremiah ierem jerem ierm iere':'jeremiah',
    'lam la lament':'lamentations',
    'ezek eze ezk ezech ezck ezec':'ezekiel',
    'dan da dn':'daniel',
    'hos ho hoshea hosh hose hsea hsh':'hosea',
    'jl ioel il':'joel',
    'am':'amos',
    'obad ob':'obadiah',
    'jnh jon ion inh ionah jona iona':'jonah',
    'mic mc mica':'micah',
    'na nah':'nahum',
    'hab hb habb habbak habba habbac habac':'habakkuk',
    'zeph zep zp zephan':'zephaniah',
    'hag hg hagg':'haggai',
    'zech zec zc zch zach zachar zac':'zechariah',
    'mal ml malac malach mala':'malachi',
    'matt matth mt math mat mattth':'matthew',
    'mrk mar mk mr marc marke':'mark',
    'luk lk luc lc':'luke',
    'joh jhn ioh ihn iohn ioan joan':'john',
    'act ac acta':'acts',
    'rom ro rm roman':'romans',
    'cor co cr or corinth corin':'corinthians',
    'gal ga galat':'galatians',
    'eph ephes ephe ephs ehes':'ephesians',
    'phil php pp phillip philip':'philippians',
    'col coloss colos':'colossians',
    'thess thes th thss':'thessalonians',
    'tim timoth':'timothy',
    'tit tius':'titus',
    'philem phm pm':'philemon',
    'heb hebr':'hebrews',
    'jas jm iam ias im iames jam iaes':'james',
    'pet pe pt p petr':'peter',
    'jud jd iud id iude':'jude',
    'rev re reu reuelation reuel reuelations reve revel':'revelation',
    'apoc apo apoc': 'apocrypha',
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

'''This function takes a string and standardizes all instances of the abbreviations found in the keys of the "bible" dictionary.'''
def replaceBible(text):
    for key,value in zip(bible.keys(), bible.values()):
        variations = key.split(' ')
        for v in variations: 
            text = re.sub(rf'\b{v}\b|\b{v}\.\b|^{v}\.\b|^{v}\b', value, text)
    return text

'''This function converts all instances of numbered books into single words with the "numBooks" dictionary.'''
def replaceNumBook(text):
    for key,value in zip(numBook.keys(), numBook.values()):
        text = re.sub(rf'\b{key}\b', value, text)
        text = re.sub(r'\s+',' ',text)
    return text

# Get all of the names of the Bible's books 
bibleBooks = [x for x in bible.values()]
bibleBooks.extend([x for x in numBook.values()])
# Capitalize the books for final output 
original_titles = {v.capitalize():k for k,v in numBook.items()}

'''Checks if a text string contains any instances of a Biblical citation'''
def verify(text): 
    for book in bibleBooks:
        if re.search(rf'{book} \d+', text): 
            return True

'''Master function to extract all the Biblical citations from the marginalia of one file.''' 
def getMarginalia(filepath):
    # read the input XML file 
    with open(filepath,'r') as file: 
        data = file.read()
    # use soupstrainer to only parse the main text body (excluding dedicatory materials etc)
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
    soups = [soup1, soup2,soup3,soup4]
    # initialize list to keep track of the notes that might have citations
    possible_citations = []
    # keep track of all the cleaned and standardized notes for later processing of special cases 
    notes = []
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
            # next, replace all instances of two or more spaces with a single space. Thus, all the citation formats have been standardized. 
            n = re.sub(r'\s+',' ',n)
            # now, standardize all abbreviations in the text of this note tag  
            n = replaceBible(n)
            # Reformat the numbered books, which ensures that the later regex searches do not produce duplicates for these numbered books. 
            n = replaceNumBook(n)
            # check if the text has a biblical citation. 
            if verify(n): 
                # if so, then append it to the possible_citations list for later processing 
                possible_citations.append(n)
            # append the cleaned and standardized note to the master list of notes 
            notes.append(n)
    # call another function to actually return a list of actual Biblical citations 
    margins = findCitations(possible_citations)
    # The special cases are the possibly "missing" citations, 
    # i.e., words that are followed by two integers but not found in the keys of the standardizer Bible dictionary
    special_cases = findMissing(notes)
    # return both the list of citations and special cases 
    return margins,special_cases

'''
Helper function to extract citations from a marginal note that contain commas 
(i.e., multiple line citations from the same chapter of the same book)
'''
def comma(book, passage): 
    # initialize a list of citations 
    phrases = []
    # account for the edge case in which there is a full citation following a comma
    # i.e., given the phrase "isaiah 1 2, 3, 4 5, jeremiah 12 7", this code should return "isaiah 4 5" as its own citation 
    # The other citations would be "isaiah 1 2", "isaiah 1 3", and "jeremiah 12 7" (returned either by the comma() or the simple() functions)
    edge_case = re.search(', \d+ \d+',passage)
    if edge_case: 
        # if there is an instance of the edge case, call the simple() function 
        phrases.append(simple(book, edge_case.group()))
        # add the returned string to the list of citations 
        passage = re.sub(edge_case.group(), '',passage)
    # the remaining cases are those that are like "isaiah 1 2, 3"
    # find all the integers 
    nums = re.findall(f'(\d+)',passage)
    # The first number will be the chapter number, and all the ensuing ones are line numbers 
    for num in nums[1:]: 
        phrases.append(f'{book} {nums[0]}:{num}')
    # return list of citations 
    return phrases 

'''
Helper function to extract citations from a marginal note that does not contain commas

Target format is "<book> <chapter> <line>" 
'''
def simple(book, passage): 
    # the simple case of just having "<book> <chapter> <line>" 
    passage = re.findall('(\d+) (\d+)',passage)[0]
    # return citation 
    return f'{book} {passage[0]}:{passage[1]}'

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
'''
def hyphen(book, phrase):
    phrases = []
    if re.search(r'[a-z]+ \d+ \d+—\d+|[a-z]+ \d+ \d+ —\d+',phrase): 
        # case of continuous citation, e.g, "Genesis 3 9-14" --> "Genesis 3:9", "Genesis 3:10", etc. until "Genesis 3:14"
        nums = re.findall(r'\d+',phrase)
        chapter, start, end = nums[0], int(nums[1]), int(nums[2])
        for idx in range(end-start+1): 
            phrases.append(f'{book} {chapter}:{start+idx}')
    else: 
        # case of discrete citations, e.g., "Psalms 1 2 - 3 4" --> "Psalms 1:2" and "Psalms 3:4"
        passages = phrase.split('—')
        chapters = []
        for passage in passages: 
            if not re.search('\d+', passage): continue

            if not re.search('\d+ \d+',passage): 
                phrases.append(f'{book} {chapters[-1]} {passage.strip()}')
            else:
                chapters = re.findall('\d+',passage)[0]
                phrases.append(simple(book,passage))
    return phrases


'''Main function to actually extract all of the Biblical citations'''
def findCitations(notes_list): 
    # initialize lists to keep track of the properly formatted citations and possible formats that this code cannot currently account for 
    citations, outliers = [], []

    # iterate through every single item of the notes_list
    for n in notes_list: 
        # initialize even more local variables of citations and outliers 
        # iterate through every single book of the bible because each note line can have citations from multiple different books 
        for book in bibleBooks:
            phrases, pesky = [], []
            # search whether the current phrase an instance of this book
            phrase = re.search(rf'\b{book}\b(.*?)(?=[a-z])|\b{book}\b(.*?)$',n)
            # if the current note phrase does not have an instance of this book, continue on to the next book 
            if phrase is None: continue
            # if there is an instance, then group the regex search result together 
            # so that the phrase only contains the citation for a SINGLE book 
            # i.e., "isaiah 5 5 "
            phrase = phrase.group().strip()
            n = re.sub(phrase,'',n)
            # if there is no instance of the book followed by at least two decimals, skip to the next book  
            if not re.search(r'[a-z]+ \d+ \d+',phrase): continue
            
            # if the note is simply a single citation, call simple() to append the citation to the list of citations 
            if re.search(r'^[a-z]+ \d+ \d+$',phrase):  
                phrases.append(simple(book, phrase))
            # Case of having "<book> <chapter> <line1> <line2>"
            elif re.search(r'^[a-z]+ \d+ \d+ \d+$|^[a-z]+ \d+ \d+ \d+ \d+$|^[a-z]+ \d+ \d+ \d+ \d+ \d+$',phrase):  
                phrases.extend(othersimple(book, phrase))
            # if there are ampersands in the note, split the note up by the ampersands 
            elif re.search('&',phrase): 
                passages = phrase.split('&')
                for passage in passages: 
                    passage = passage.strip()
                    # call comma() if the substring as a comma 
                    if re.search(',',passage):
                        phrases.extend(comma(book, passage))
                    else:
                        if re.search(r'\-',passage): 
                            passages = passage.split('-')
                            for passage in passages: 
                                phrases.append(simple(book,passage))
                        # call othersimple() to account for the case of "<chapter> <line1> <line2>" 
                        elif re.search(r'\d+ \d+ \d+$', passage): 
                            phrases.extend(othersimple(book, passage))
                        # call simple() to account for "<chapter> <line1>"
                        elif re.search(r'\d+ \d+$',passage): 
                            phrases.append(simple(book, passage))
            # if there are no ampersands, call comma() to account for the multiple citations of the same chapter 
            elif re.search(',',phrase): 
                phrases.extend(comma(book, phrase))
            # if there are hyphens dividing individual citations, 
            # i.e., "2 King. 6. 22.—9. 24.—13 15." --> "2 Kings 6:22", "2 Kings 9:24" and "2 Kings 13:15"
            elif re.search(r'\—',phrase): 
                phrases.extend(hyphen(book, phrase))
            # else, there is a format that this code cannot account effectively for 
            else: 
                # hard coding some special cases for the charity sermons dataset
                if 'psalms 119 5 10 32 57 93 106 173 40' in phrase: 
                    # original is Psal 119.5 10.32.57.93.106 173.40.
                    phrases.extend(['psalms 119:5', 'psalms 10:32', 'psalms 10:57','psalms 10:93','psalms 10:106', 'psalms 173:40'])
                elif 'romans 8 1 3 5 8 9' in phrase: 
                    # original is Rm. 8.1.3 5.8.9
                    phrases.extend(['romans 8:1','romans 8:2', 'romans 8:3', 'romans 5:8', 'romans 5:9'])
                else: 
                    pesky.append(phrase)
            # capitalize the book of each citation and append to the list of citations to return
            for phrase in phrases:
                citations.append(phrase.capitalize())
            # do the same for the outliers 
            for p in pesky: 
                outliers.append(p.capitalize())
    # change numbered books into original formatting for pretty output 
    citations, outliers = proper_title(citations, outliers)
    # return both citations and outliers  
    return citations, outliers

'''Main function to find special cases of "<word> <int1> <int2>" in which the <word> is not part of the standardizer dictionary'''
def findMissing(missing_list): 
    special_cases = []
    for m in missing_list: 
        if re.search('[a-z]+ \d+ \d+',m): 
            missing = re.findall('[a-z]+ \d+ \d+',m)
            for phrase in missing: 
                found = False
                for book in bibleBooks:
                    if re.search(rf'\b{book}\b', phrase): 
                        found = True 
                        break
                if found: 
                    # if the <word> is actually a known Bible book title, skip onto the next phrase
                    continue
                # else, there is a special case 
                special_cases.append(phrase)
    return sorted(special_cases)

'''For pretty formatting, convert the numbered books back into their original formats, i.e., "Onecorinthians" to "1 Corinthians"'''
def proper_title(citations_list, pesky_list): 
    for idx, passage in enumerate(citations_list): 
        book = passage.split(' ')[0]
        if book in original_titles.keys():
            orig_title = original_titles[book].split(' ')
            orig_title[1] = orig_title[1].capitalize()
            passage = re.sub(book, ' '.join(orig_title), passage)
            citations_list[idx] = passage

    for idx, passage in enumerate(pesky_list): 
        book = passage.split(' ')[0]
        if book in original_titles.keys():
            orig_title = original_titles[book].split(' ')
            orig_title[1] = orig_title[1].capitalize()
            passage = re.sub(book, ' '.join(orig_title), passage)
            pesky_list[idx] = passage

    return citations_list, pesky_list 