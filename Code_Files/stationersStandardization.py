import pandas as pd

'''From a CSV of publishers' alternative names, generate a standardizer dictionary'''
publishers = input("Enter the path to a CSV of publishers or write Default to use ours: ")
if 'Default' in publishers or 'default' in publishers: 
    file = 'Standardization_Files/EML Authors_Publishers 2022-Public - Publisher Names.csv'
else: 
    file = publishers
data = pd.read_csv(file)
data = data.fillna(0)
nameDict = {}
for idx, name in enumerate(data['Standard']):
    for num in range(1,10+1):
        entry = data[str(num)][idx]
        if entry != 0: 
            nameDict[entry.strip()] = name.strip()         
print(f'publishers = {nameDict}')

'''From a CSV of printers' alternative names, generate a standardizer dictionary'''
printers = input("Enter the path to a CSV of printers or write Default to use ours: ")
if 'Default' in publishers or 'default' in printers:
    file = 'Standardization_Files/EML Authors_Publishers 2022-Public - Printer Names.csv'
else: 
    file = printers 
data = pd.read_csv(file)
data = data.fillna(0)
nameDict = {}
for idx, name in enumerate(data['Standard']):
    for num in range(1,6+1):
        entry = data[str(num)][idx]
        if entry != 0: 
            nameDict[entry.strip()] = name.strip()         
print(f'printers = {nameDict}')

'''From a CSV of booksellers' locations, generate a location dictionary'''
locations = input("Enter the path to a CSV of publishers' locations or write Default to use ours: ")
if 'Default' in locations or 'default' in locations:
    file = 'Standardization_Files/EML Authors_Publishers 2022-Public - Publisher Locations.csv'
else: 
    file = locations 
data = pd.read_csv(file)
data = data.fillna(0)
placeDict = {}
for idx, name in enumerate(data['Publisher']):
    placeDict[name.strip()] = []
    for num in range(1,3+1):
        entry = data[f'Shop{num}'][idx]
        if entry != 0: 
            placeDict[name.strip()].append(entry)
                     
print(f'pubplaces = {placeDict}')