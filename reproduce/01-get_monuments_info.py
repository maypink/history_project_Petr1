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
    return string.replace('\r', '').replace('\t', '')


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


def get_info(df: pd.DataFrame, offset_for_index = 0):
    monuments = []
    for i in tqdm(df.iterrows(), total = df.shape[0]):
        cur_url = 'http://petersmonuments.ru' + i[1].link
        resp = req.get(cur_url)
        soup = BeautifulSoup(resp.text, 'lxml')
        name = soup.find_all('div', class_='full-description')[0].find_all('h1')[0].contents[0].strip()
        info = soup.find_all('div', class_='full-description__mini-desc')[0].find_all('p')
        location = info[0].contents[2].strip()

        image_urls = []
        for image in soup.find_all('a', class_='gallery_monuments'):
            image_urls.append(f"http://petersmonuments.ru{image.attrs['href']}")

        type = ''
        if len(info) > 1:
            type = info[1].contents[2].strip()

        status = ''
        if len(info) > 2:
            status = info[2].contents[2].strip()

        desc_raw = soup.find_all('div', class_='full-description__text')[0].find_all('p')[1:-1]
        description = ''
        for par in desc_raw:
            if len(par) == 1:
                description += par.contents[0].strip() + '\n'
        coords = get_coords(location)
        # coords = {'lat': 0.0, 'lng': 0.0}
        monument = Monument(i[0] + offset_for_index, name, location, coords, type, status, remove_useless(description), image_urls.copy())
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


def save_info(root: Path, monuments: List[Monument], is_start: bool = False, is_end: bool = False):

    path_coords = os.path.join(root, 'processed', 'coords', "coords.json")
    check_dir(os.path.join(root, 'processed', 'coords'), 2)
    if is_start:
        with open(path_coords, 'w', encoding='utf8') as file:   
            file.write('[')


    for monument in monuments:
        file_name = str(monument.id) + '.json'
        check_dir(root)

        path_info = os.path.join(root, 'processed', 'info', file_name)
        check_dir(os.path.join(root, 'processed', 'info'), 2)

        try:
            with open(path_coords, 'a', encoding='utf8') as file:
                json.dump(monument.coords_to_json(), file, ensure_ascii=False)
                if not is_end or monuments.index(monument) != len(monuments) - 1:
                    file.write(',')

            with open(path_info, 'w', encoding='utf8') as file2:
                json.dump(monument.info_to_json(), file2, ensure_ascii=False)

        except OSError:
            pass
    
    if is_end:
        with open(path_coords, 'a', encoding='utf8') as file:
            file.write(']')


if __name__ == '__main__':

    root = Path('../data/')

    rus_links = pd.read_csv('../data/raw/rus_links.csv')
    save_info(root, get_info(rus_links[0:100]), is_start=True)
    for i in range(200, 1900, 100):
        save_info(root, get_info(rus_links[i - 100:i]))
    save_info(root, get_info(rus_links[1800:1809]))

    eur_links = pd.read_csv('../data/raw/eur_links.csv')
    save_info(root, get_info(eur_links, len(rus_links)), is_end=True)
