import requests as req
from bs4 import BeautifulSoup as bs

url = 'https://www.kinopoisk.ru/lists/movies/top-250-2020/'


def prepare(url: str):
    urlReq = req.get(url)
    soupUrlReq = bs(urlReq.text, 'lxml')
    movieLink = 'https://www.kinopoisk.ru' + soupUrlReq.find(
        'div', class_='styles_root__ti07r').find(
        'a', class_='base-movie-main-info_link__YwtP1').get('href')
    print(movieLink)


if __name__ == '__main__':
    prepare(url)
