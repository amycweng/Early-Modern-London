import os
from collections import Counter 

folder = 'perkinsTXT'

latin = ['A54390','A09452','A09447','A09349']
welsh = ['A90503','A90506']
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
    tokens = ' '.join(tokens)
    return tokens

def getTexts(folder):
    alltext = []
    for file in os.listdir(folder):
        if 'NOTES' not in file: 
            name = file.split('.')[0]
            if name in latin: continue
            elif name in welsh: continue
            else:  
                path = os.path.join(folder,file)
                f = open(path,'r')
                data = f.readlines()[0]
                data = remove_stopwords(data)
                alltext.append(data)
                f.close()
    return ' '.join(alltext)

texts = getTexts('/Users/amycweng/Digital Humanities/perkinsTXT')
with open('mostcommon.txt','w+') as file: 
    file.write(str(Counter(texts.split(' ')).most_common(10000)))