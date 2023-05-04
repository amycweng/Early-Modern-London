import os, re
import pandas as pd 
from collections import Counter

'''
Feature extraction functions 
'''     
def getTexts(folder,search):
    texts = {}
    for file in os.listdir(folder):
        name = file.split('.')[0]
        if name in search: 
            path = os.path.join(folder,file)
            with open(path,'r') as file: 
                data = file.readlines()
            if len(data) != 0: 
                data = data[0]
                data = [x for x in data.split(' ') if len(x) > 1]
                data = ' '.join(data)
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
            if type == 'topic': 
                features = re.sub('\n|--','',features)
                features = features.split(' ')
                if '' in features: features.remove('')
                dict[tcpID] = features
            elif type == 'ngrams': 
                line = line.split('--')
                tcp_id = line[0].split(':')[0].strip()
                dict[tcp_id] = line[1].strip().split(' ')
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

important_info = pd.read_csv('/Users/amycweng/Digital Humanities/Early-Modern-London/Sermons_Info/text_info.csv')
location, audience, help_poor = {}, {}, {}
for idx, tcpID in enumerate(important_info['id']):
    location[tcpID] = [important_info['location_name'][idx]]
    audience[tcpID] = [important_info['type/audience'][idx]]
    help_poor[tcpID] = [important_info['help_poor'][idx]]

topics = get_features('/Users/amycweng/Digital Humanities/Early-Modern-London/Sermons_Info/topics.charity.sermons.txt','topic')
subjects = get_features('/Users/amycweng/Digital Humanities/Early-Modern-London/Sermons_Info/sermons.subject.headings.txt','subject')
all_citations = get_features('/Users/amycweng/Digital Humanities/Early-Modern-London/Sermons_Info/marginalia.all.sermons.txt','citations')
charity_citations = get_features('/Users/amycweng/Digital Humanities/Early-Modern-London/Sermons_Info/marginalia.charity.sermons.txt','citations')
ngrams = get_features('/Users/amycweng/Digital Humanities/Early-Modern-London/Sermons_Info/gramsEachcharityText.txt','ngrams')
