import csv, os,re
import pandas as pd 

'''For any given list of authors, this file compiles all the metadata for their texts found in the TCP.'''

def getAuthorTCPMetadata(outputfilepath, authors, metadataFolder): 
    '''
    Args: 
        outputfilepath (string): Path to your desired output CSV file of metadata
        authors (list of strings): A list of authors, with each name written exactly how it is like in EEBO, e.g., 'Haughton, William'
        metadataFolder (string): Path to the input folder of all TCP metadata CSV files (can be downloaded from the ECBC-Data-2022 git repository) 
    '''
    # open a csv file to write the output to 
    outFile = open(outputfilepath,'w')
    # initialize the columns of the new output csv file 
    columns = ['id','title','author','publisher','pubplace','keywords','date']
    # create a writer object to dynamically write to the csv 
    writer = csv.DictWriter(outFile, fieldnames=columns)
    # write the column headers 
    writer.writeheader()
    # counter variable to keep track of the number of entries 
    count = 0
    # turn the input list of authors into a single regex search string 
    authSearch = re.compile('|'.join(authors))
    # iterate through every single TCP metadata file 
    for csvFile in os.listdir(metadataFolder):
        # read the current csv metadata file 
        data = pd.read_csv(os.path.join(metadataFolder,csvFile))
        # iterate through the author column to find hits 
        for idx,entry in enumerate(data['author']):
            if re.search(authSearch,str(entry)):
                # if there is an instance of a target author's name, 
                # make sure that the list of names written to the output file 
                # contains only unique values. The original TCP metadata entries 
                # sometimes have duplicate names 
                names = entry.split('; ')
                names = '; '.join(list(set(names)))
                count += 1
                # gather the entry as a dictionary 
                row = {'id':data['id'][idx],
                        'title':data['title'][idx],
                        'author':names,
                        'publisher':data['publisher'][idx],
                        'pubplace':data['pubplace'][idx],
                        'keywords':data['keywords'][idx],
                        'date':data['date'][idx]}
                # write the dictionary to the output csv file 
                writer.writerow(row)
    outFile.close()
    # inform the user about the number of files. 
    print(f'There are {str(count)} TCP files for your input list of authors.\n')

# Example call: 
# getAuthorTCPMetadata('milton.csv', ['Milton, John'], '/Users/amycweng/Digital Humanities/ECBC-Data-2022/TCP metadata')