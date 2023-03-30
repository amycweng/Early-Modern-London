import os, re
import pandas as pd 
from collections import Counter

'''
Feature extraction functions 
'''     
def remove_stopwords(text):
    stop = ['i', 'amp','me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 
                "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 
                'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', 
                "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 
                'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 
                'am', 'in','is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 
                'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'or', 
                'as', 'until', 'while', 'at', 'by', 'for', 'with', 'about', 'between', 'into', 
                'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 
                'down', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 
                'there', 'when', 'whence','where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',
                'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 
                'than', 'too', 'very', 's', 't', 'can', 'will', 'don', "don't", "should've", 'now', 
                'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 
                'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', 
                "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', 
                "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', 
                "weren't", 'won', "won't", 'wouldn', "wouldn't", 'neve', 'earlier', 'may', 
                'unto', 'whereof', 'began', 'inasmuch', 'shall', 'de', 'we', 'sir', 'later', 'until', 
                'could', 'two', 'years', 'mr', 'long', 'till', 'thereof', 'indeed', 'ie', 'himself', 
                'neither', 'doth', 'thence', 'seem', 'part', 'old', 'definite', 'would', 'iq', 
                'aforesaid', 'ever', 'might', 'upon', 'how', 'therein', 'through', 'done', 'begin', 
                'little', 'last', 'also', 'ew', 'etc', 'full', 'second', 'though', 'more', 'his', 
                'whereas', 'thy', 'thee', 'themselves', 'he', 'why', 'seldom', 'hear', 'what', 
                'think', 'matter', 'et cetera', 'present', 'do', 'before', 'made', 'there', 
                'thereforeunto', 'when', 'whilst', 'herself', 'definitely', 'her', 'arrived', 
                'per', 'afterward', 'far', 'dr', 'saying', 'char', 'whereby', 'or', 'third', 
                'seems', 'mentioned', 'go', 'esq', 'year', 'likewise', 'must', 'know', 'pag', 
                'conerning', 'earliest', 'ditto', 'hath', 'without', 'self', 'lib', 'three', 
                'and', 'itself', 'suchtwo', 'otherwise', 'seeing', 'him', 'latest', 'often', 
                'cannot', 'et', 'thou', 'est', 'it', 'which', 'can', 'most', 'let', 'almost', 
                'say', 'late', 'hereby', 'every', 'wherein', 'either', 'much', 'come', 'said', 
                'else', 'near', 'cap', 'esq', 'viz', 'heard', 'fol', 'like', 
                'within', 'have', 'thus', 'certainly', 'one', 'make', 'rather', 'she', 
                'eg', 'where', 'ne', 'since', 'four', 'fourth', 'includes', 'even', 'us', 
                'gone', 'five', 'anno', 'went', 'thing','according','hove','set',
                'ettling', 'hee', 'bee', 'wee', 'mat', 'gen','rom',
                'if','of','because','since','part','yet','whether',
                'many','day','great','qua','out','man','time',
                'first','one','two','second','well','see','call',
                'against','never','word','place','therefore',
                'way','still']

    tokens = [x for x in text.split(' ') if x not in stop]
    return ' '.join(tokens)
    
def getTexts(folder,search,stopwords = False):
    texts = {}
    for file in os.listdir(folder):
        name = file.split('.')[0]
        if name in search: 
            path = os.path.join(folder,file)
            with open(path,'r') as file: 
                data = file.readlines()
            if len(data) != 0: 
                data = data[0]
                if stopwords:
                    data = remove_stopwords(data)
                texts[name] = data
    return texts

def get_features(filePath,type): 
    '''
    Returns a dictionary in this format {id : features}
    '''
    readFile = open(filePath,'r')
    dict = {}
    for line in readFile:
        if type == 'citations': 
            tcpID =  line.split(' -- ')[0]
            features = line.split(' -- ')[1]
            features = re.sub('\n','',features)
            features = features.split('; ')
            if '' in features: features.remove('')
            dict[tcpID] = features
        else: 
            tcpID =  line.split(':')[0]
            features = line.split(':')[1]
            if type == 'topic' or type == 'ngrams': 
                features = re.sub('\n|--','',features)
                features = features.split(' ')
                if '' in features: features.remove('')
                dict[tcpID] = features
            elif type == 'subject': 
                final_features = []
                features = re.sub('\n','',features)
                features = features.split(' -- ')
                for feature in features: 
                    if not re.search('Sermons\, English|Early works to 1800.|17th century.|Sermons.|Sermons|Bible.',feature):
                        final_features.append(feature.strip())
                if '' in features: final_features.remove('')
                dict[tcpID] = final_features
    readFile.close()
    return dict

def count_features(feature_dict,ids,type=''): 
    all_features = []
    for tcpID, features in feature_dict.items(): 
        if tcpID in ids and len(features) > 0: 
            all_features.extend(features)
    if type == 'all citations': 
        print(f'\tThere are {len(all_features)} marginal citations in total.')
    elif type == 'charity citations': 
        print(f'\tThere are {len(all_features)} marginal citations relating to charity.')

    return Counter(all_features).most_common(n=20)

def find_titles(ids_list,idToTitle): 
    titles_list = [] 
    for tcpID in ids_list: 
        title = idToTitle[tcpID]
        title = title.split(' ')
        titles_list.append(f'{tcpID}: {" ".join(title[0:10])}')
    return titles_list

'''
Charity sermons dataset feature extraction (for use in the sermon_clustering and hierarchical_clustering Jupyter Notebook files)
'''
csv_data = pd.read_csv('/Users/amycweng/Digital Humanities/Early-Modern-London/Sermons_Info/sermons.csv')
all_info = pd.read_csv('/Users/amycweng/Digital Humanities/Early-Modern-London/Relevant_Metadata/charityTCP.csv')
tcpIDs = [ _ for _ in csv_data['id']]
idToTitle = {}
idToAuthor = {}
for idx, title in enumerate(all_info['title']):
    curr_id = all_info['id'][idx]
    idToTitle[curr_id] = title 
    idToAuthor[curr_id] = all_info['author'][idx]

# William Whately, William Crashaw, Joseph Hall, John Preston, William Gouge, Thomas Gataker
authors = ['Whately','Crashaw','Hall','Preston','Gouge','Gataker'] 
idAuthor = []
for tcpID in tcpIDs: 
    for author in authors: 
        if author in idToAuthor[tcpID]: 
            idAuthor.append(f'{author}_{tcpID}')
            break

important_info = pd.read_csv('/Users/amycweng/Digital Humanities/Early-Modern-London/Sermons_Info/audience.location.etc.csv')
location, audience, help_poor = {}, {}, {}
for idx, tcpID in enumerate(important_info['id']):
    location[tcpID] = [important_info['location_name'][idx]]
    audience[tcpID] = [important_info['audience'][idx]]
    help_poor[tcpID] = [important_info['help_poor'][idx]]

topics = get_features('/Users/amycweng/Digital Humanities/Early-Modern-London/Sermons_Info/topics.charity.sermons.txt','topic')
subjects = get_features('/Users/amycweng/Digital Humanities/Early-Modern-London/Sermons_Info/sermons.subject.headings.txt','subject')
all_citations = get_features('/Users/amycweng/Digital Humanities/Early-Modern-London/Sermons_Info/marginalia.all.sermons.txt','citations')
charity_citations = get_features('/Users/amycweng/Digital Humanities/Early-Modern-London/Sermons_Info/marginalia.charity.sermons.txt','citations')
ngrams = get_features('/Users/amycweng/Digital Humanities/Early-Modern-London/Sermons_Info/gramsEachcharityText.txt','ngrams')
