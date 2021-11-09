import pandas as pd
from pathlib import Path
from typing import List
import json
import os
from tqdm import tqdm
from bs4 import BeautifulSoup
import requests as req
from history_project_Petr1.entities.monument import Monument


def get_info(df: pd.DataFrame):
    monuments = []
    for i in tqdm(df.iterrows(), total = df.shape[0]):
        cur_url = 'http://petersmonuments.ru' + i[1].link
        resp = req.get(cur_url)
        soup = BeautifulSoup(resp.text, 'lxml')
        name = soup.find_all('div', class_='full-description')[0].find_all('h1')[0].contents[0].lstrip().rstrip()
        info = soup.find_all('div', class_='full-description__mini-desc')[0].find_all('p')
        location = info[0].contents[2]

        type = ''
        if len(info) > 1:
            type = info[1].contents[2]

        status = ''
        if len(info) > 2:
            status = info[2].contents[2]

        desc_raw = soup.find_all('div', class_='full-description__text')[0].find_all('p')[1:-1]
        description = []
        for par in desc_raw:
            if len(par) == 1:
                description.append(par.contents)

        monument = Monument(name, location, type, status, description)
        monuments.append(monument)
    return monuments


def check_dir(path: Path):
    if os.path.exists(path):
        if os.path.exists(os.path.join(path, 'processed')):
            return True
        else:
            os.mkdir(path)
    else:
        os.mkdir(path)


def save_info(root: Path, monuments: List[Monument]):

    for monument in monuments:
        file_name = monument.name.replace(' ', '_')
        check_dir(root)
        path = os.path.join(root, 'processed', file_name)
        try:
            with open(path, 'w', encoding='utf8') as file:
                json.dump(monument.to_json(), file, ensure_ascii=False)
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


