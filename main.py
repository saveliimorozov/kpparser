import requests as req
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent

url = 'https://www.kinopoisk.ru/lists/movies/top-250-2020/'


def prepare(url: str):
    urlReq = req.get(url, headers={'User-Agent': UserAgent().chrome})
    # print(urlReq)

    soupUrlReq = bs(urlReq.text, 'lxml')
    # print(soupUrlReq.prettify())

    movieMainInfo = soupUrlReq.find('div', class_='styles_root__ti07r').find(
        'a', class_='base-movie-main-info_link__YwtP1')

    movieLink = 'https://www.kinopoisk.ru' + movieMainInfo.get('href')

    movieNameRu = movieMainInfo.find('div', class_='base-movie-main-info_mainInfo__ZL_u3').find(
        'span', class_='styles_mainTitle__IFQyZ styles_activeMovieTittle__kJdJj').text

    print(movieMainInfo.prettify())
    print(movieLink)
    print(movieNameRu)
#

if __name__ == '__main__':
    prepare(url)
