from requests import get 
import time 
import pandas as pd 
import os
import json


def list_pokemon():
    """
    Retrieves a full list of pokemon from the poke api

    Returns:
        A DataFrame
    """
    base_url  = 'https://pokeapi.co/api/v2/pokemon'
    
    pagelength = 1000
    i = 0 
    morepages = True
    pokemon_results = []
    # retrieving full list of pokemon
    while morepages == True:
        params = {'offset' : pagelength * i, 'limit': pagelength} # adjusting the offset AND limit parameters
        r = get(base_url, params = params)
        response = r.json()
        pokemon_results.append(response)
        time.sleep(.3)
        morepages = len(response['results'])> 0 
        print(i, end =" ")
        i+=1
    datalist = [pd.DataFrame(i['results']) for i in pokemon_results]
    df = pd.concat(datalist).reset_index()
    return df


def retrieve_pokemon_info(urls, wait=.3, store_data="pokemon_info/"):
    """
    Takes a list of urls. Retrieves the json file for each result and then stores it (or skips if there's already a matching file in the directory) 

    Arguments:
        urls: a list of URLS to be retrieved
        wait: the amount of time to wait between each request (defaults to .3)
        store_data: where to store the json file after each request
        
    Returns:
       None
    """
    count = 0
    os.makedirs(store_data, exist_ok=True) 
    current_files = set(os.listdir(store_data))
    for i in urls:
        fname = i.rsplit('/', 2)[-2] + ".json"
        if fname in current_files:
            print('data already exists, skipping')
            continue
        pokemon = get(i)
        data = pokemon.json()
        fpath = os.path.join(store_data , fname)
        with open(fpath, "w") as file:
            json.dump(data, file, indent = 4)
        time.sleep(wait)
        count = count + 1
    print(str(count) + " new files added to "  + store_data)

def pokemon_to_df(folder="pokemon_info/"):
    """
    Takes a directory with files downloaded using the 
    
    Arguments: 
        A directory with .json files from the poke api
    Returns:
        A data frame
    """
    files = [f for f in os.listdir(folder) if f.endswith('.json')]
    poke_info = []
    for i in files:
        file_path = folder  + i
        with open(file_path, 'r') as file:
            data = json.load(file)
        res = {
                'url' : i,
                'name' : data['name'],
                'weight': data['weight'], 
                'height': data['height'],
                'type' : ', '.join([i.get('type').get('name') for i in data['types']]),
                'sprite' : data['sprites']['front_default']

            }
        poke_info.append(res)
    return pd.DataFrame(poke_info)