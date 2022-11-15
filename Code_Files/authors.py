import csv, os,re
import pandas as pd 

'''Getting all TCP metadata for certain authors'''

def getAuthorTCPMetadata(outputfilepath, authors, metadataFolder): 
    '''
    Args: 
        outputfilepath (string): Path to your desired output CSV file of metadata
        authors (list of strings): A list of authors, with each name written exactly how it is like in EEBO, e.g., 'Haughton, William'
        metadataFolder (string): Path to the input folder of all TCP metadata CSV files (can be downloaded from the ECBC-Data-2022 git repository) 
    '''
    outFile = open(outputfilepath,'w')
    columns = ['id','title','author','publisher','pubplace','keywords','date']
    writer = csv.DictWriter(outFile, fieldnames=columns)
    writer.writeheader()
    count = 0
    authSearch = re.compile('|'.join(authors))
    for csvFile in os.listdir(metadataFolder):
        data = pd.read_csv(os.path.join(metadataFolder,csvFile))
        for idx,entry in enumerate(data['author']):
            found = False
            if re.search(authSearch,str(entry)):
                found = True
            if found:
                names = entry.split('; ')
                names = '; '.join(list(set(names)))
                count += 1
                row = {'id':data['id'][idx],
                        'title':data['title'][idx],
                        'author':names,
                        'publisher':data['publisher'][idx],
                        'pubplace':data['pubplace'][idx],
                        'keywords':data['keywords'][idx],
                        'date':data['date'][idx]}
                writer.writerow(row)
                found = False
    print(f'There are {str(count)} TCP files for your input list of authors.\n')

# Example call: 
# getAuthorTCPMetadata('milton.csv', ['Milton, John'], '/Users/amycweng/Digital Humanities/ECBC-Data-2022/TCP metadata')