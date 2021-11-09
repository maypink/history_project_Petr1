import pandas as pd
from typing import List
from bs4 import BeautifulSoup
import requests as req
import os
from pathlib import Path


def check_dir(path: Path):
    if os.path.exists(path):
        if os.path.exists(path + '/' + 'raw'):
            return True
        else:
            os.mkdir(path)
    else:
        os.mkdir(path)


def get_links(url: str) -> List[str]:
    resp = req.get(url)

    soup = BeautifulSoup(resp.text, 'lxml')
    items = soup.find_all('div', class_='alphabet-column__symbol_column')
    links = []
    for item in items[0].find_all('a'):
        links.append(item.get('href'))
    return links


if __name__ == '__main__':

    russia_monuments_url = 'http://petersmonuments.ru/russia/memorials/'
    europe_monuments_url = 'http://petersmonuments.ru/europe/memorials/'

    rus_links = get_links(russia_monuments_url)
    eur_links = get_links(europe_monuments_url)

    df_rus = pd.DataFrame({'link': rus_links})
    df_eur = pd.DataFrame({'link': eur_links})

    check_dir(Path('../data/raw/'))
    df_rus.to_csv('../data/raw/rus_links.csv')
    df_eur.to_csv('../data/raw/eur_links.csv')

