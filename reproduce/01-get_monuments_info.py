import pandas as pd
from pathlib import Path
from typing import List
import json
import os
from tqdm import tqdm
from bs4 import BeautifulSoup
import requests as req
from history_project_Petr1.entities.monument import Monument
import googlemaps


gmaps = googlemaps.Client(key='AIzaSyDPZrHhcjXo8jFH0_dhJnU46UXGgb6h4tI')


def remove_useless(string: str):
    return string.replace('\r', '').replace('\n', '').replace('\t', '')


def get_coords(address: str):
    geocode_result = gmaps.geocode(address)
    try:
        lat = geocode_result[0]['geometry']['location']['lat']
        lng = geocode_result[0]['geometry']['location']['lng']
    except Exception as e:
        print(e)
        lat = 0
        lng = 0
        
    return {'lat': lat, 'lng': lng}


def get_info(df: pd.DataFrame):
    monuments = []
    for i in tqdm(df.iterrows(), total = df.shape[0]):
        cur_url = 'http://petersmonuments.ru' + i[1].link
        resp = req.get(cur_url)
        soup = BeautifulSoup(resp.text, 'lxml')
        name = soup.find_all('div', class_='full-description')[0].find_all('h1')[0].contents[0].strip()
        info = soup.find_all('div', class_='full-description__mini-desc')[0].find_all('p')
        location = info[0].contents[2]

        type = ''
        if len(info) > 1:
            type = info[1].contents[2]
        type.strip()

        status = ''
        if len(info) > 2:
            status = info[2].contents[2]
        status.strip()

        desc_raw = soup.find_all('div', class_='full-description__text')[0].find_all('p')[1:-1]
        description = []
        for par in desc_raw:
            if len(par) == 1:
                description.append(par.contents)

        coords = get_coords(location)
        monument = Monument(0, name, location, coords, type, status, description)
        monuments.append(monument)
    return monuments


def check_dir(path: Path, key = 1):
    if os.path.exists(path):
        if os.path.exists(os.path.join(path, 'processed')):
            return True
        elif os.path.exists(os.path.join(path, 'processed')) == False & key == 1:
            os.mkdir(os.path.join(path, 'processed'))
    else:
        os.mkdir(path)


def save_info(root: Path, monuments: List[Monument]):

    for monument in monuments:
        monument.id = id(monument)
        file_name = str(monument.id) + '.json'
        check_dir(root)

        path_coords = os.path.join(root, 'processed', 'coords', file_name)
        check_dir(os.path.join(root, 'processed', 'coords'), 2)

        path_info = os.path.join(root, 'processed', 'info', file_name)
        check_dir(os.path.join(root, 'processed', 'info'), 2)

        try:
            with open(path_coords, 'w', encoding='utf8') as file:
                json.dump(monument.coords_to_json(), file, ensure_ascii=False)

            with open(path_info, 'w', encoding='utf8') as file2:
                json.dump(monument.info_to_json(), file2, ensure_ascii=False)

        except OSError:
            pass


if __name__ == '__main__':

    rus_links = pd.read_csv('../data/raw/rus_links.csv')
    eur_links = pd.read_csv('../data/raw/eur_links.csv')

    rus_monuments = get_info(rus_links)
    eur_monuments = get_info(eur_links)

    root = Path('../data/')

    save_info(root, rus_monuments)
    save_info(root, eur_monuments)


