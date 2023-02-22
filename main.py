import requests as req
from bs4 import BeautifulSoup as bs

url = 'https://www.kinopoisk.ru/lists/movies/top-250-2020/'


def prepare(url: str):
    urlReq = req.get(url)
    soupUrlReq = bs(urlReq.text, 'lxml')
    movieClass = soupUrlReq.find('div', class_='styles_root__ti07r')
    print(movieClass)


if __name__ == '__main__':
    prepare(url)
