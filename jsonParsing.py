import re
import json
import time
import pickle
import pandas as pd
from tqdm import tqdm
from pandas.io.json import json_normalize

def timer(func):
    def function(*args, **kwargs):
        start_time = time.time()
        print('[info] Filtering data in progress.')
        result = func(*args, **kwargs)
        stop_time = time.time()
        print('[info] Algorithm work time: {}sec.'.format(stop_time - start_time))
        return result
    
    return function

def filterData(column, endFileName):
        parametersDictionary = {}
        #if isinstance(column, list) == True:
        
        # Open file insert one opening bracket
        with open(endFileName, 'a') as file:
                file.write('[')

        # Fill file with dictionaries
        for row in tqdm(column):
            if isinstance(row, float) == True:
                pass
            else:
                for dictionary in row:
                    key = dictionary['name']
                    parametersDictionary[key] = dictionary['value']
                    '''
                    if dictionary['measure'] != None:
                        parametersDictionary[key] = dictionary['value'] + dictionary['measure']
                    else:
                        parametersDictionary[key] = dictionary['value']
                    '''
                    #print(parametersDictionary)
                with open(endFileName, 'a') as file:
                    file.write(str(parametersDictionary)+',\n')

        # Open file insert one closing bracket
        with open(endFileName, 'a') as file:
                file.write(']')
        
        return parametersDictionary

@timer  
def saveData(fileToParse, endFileName):
    with open(fileToParse, encoding = 'utf-8') as f:
        data = json.load(f)
        #data = json.loads(f)

    try:
        data = json_normalize(data['items'])
    except:
        data = json_normalize(data)
    createdParametersDictionary = filterData(data['properties'], endFileName)

    #with open('parametersNotebook.pickle', 'wb') as handle:
    #    pickle.dump(createdParametersDictionary, handle, protocol=pickle.HIGHEST_PROTOCOL)

    print('[info] Normalized json has been created.\n[prep] Preparing data.')
    with open(endFileName, 'r', encoding = 'utf-8') as file:
        data = file.read()

    data = re.sub('\"', '\\"', data);
    data = re.sub('\w+(\')\w.', '\\"', data); 
    data = re.sub('\'', '\"', data)
    data = re.sub('},\n]', '}]', data)
    # It was working.
    data = re.sub(r': \"', ': "', data);

    with open(endFileName, 'w', encoding = 'utf-8') as file:
        file.write(data)

    print('[info] Everything is done.')

# Example
saveData('./example.json', './parsed.json')
