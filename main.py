import time

import requests as req
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent
import pandas as pd

url = 'https://www.kinopoisk.ru/lists/movies/top-250-2020/?page=1'


def getSitePageInText(url: str):
    urlReq = req.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'})
    # urlReq = req.get(url, headers={'User-Agent': UserAgent().safari})
    time.sleep(1)
    print(urlReq)
    time.sleep(4)

    soupUrlReq = bs(urlReq.text, 'lxml')
    time.sleep(1)
    print(soupUrlReq)

    return soupUrlReq


def getMoviesList(soupUrlReq):
    movieMainList = soupUrlReq.findAll('div', class_="styles_root__ti07r")
    time.sleep(4)
    return movieMainList


def getMovieMainInfo(singleMovieText):
    singleMovieDict = {}
    movieMainInfo = singleMovieText.find(
        lambda tag: tag.name == 'a' and tag.get('class') == ['base-movie-main-info_link__YwtP1'])



    if movieMainInfo:
        try:
            movieLink = 'https://www.kinopoisk.ru' + movieMainInfo.get('href')

            movieNameRu = movieMainInfo.find('div', class_='base-movie-main-info_mainInfo__ZL_u3').find(
                'span', class_='styles_mainTitle__IFQyZ styles_activeMovieTittle__kJdJj').text

            movieNameOrig = movieMainInfo.find('div', class_='desktop-list-main-info_secondaryTitleSlot__mc0mI').find(
                'span', class_='desktop-list-main-info_secondaryTitle__ighTt')
            if movieNameOrig != None:
                movieNameOrig = movieNameOrig.text
                movieYearandDuration = movieMainInfo.find(
                    'span', class_="desktop-list-main-info_secondaryText__M_aus").contents[2]
            else:
                movieNameOrig = movieNameRu
                movieYearandDuration = movieMainInfo.find(
                    'span', class_="desktop-list-main-info_secondaryText__M_aus").contents[0]


            movieCountryTypeDirector = movieMainInfo.find(
                'span', class_="desktop-list-main-info_truncatedText__IMQRP").contents[0]

            singleMovieDict = {'Name': movieNameRu,
                               'Original name': movieNameOrig,
                               'Main information': movieCountryTypeDirector,
                               'Additional information': movieYearandDuration,
                               'Link': movieLink
                               }
            print('Created singleDict')
        except Exception as err:
            print(err)
            print('Error single dict')
    else:
        print('Error single dict')

    return singleMovieDict


def dataToTable(dictsList: list[dict]):
    path = 'Films.xlsx'
    try:
        readyTable = pd.DataFrame([dictsList[0].values()], columns=list(dictsList[0].keys()))
        for i in range(1, len(dictsList)):
            tempDF = pd.DataFrame([dictsList[i].values()], columns=list(dictsList[i].keys()))
            readyTable = pd.concat([readyTable, tempDF], ignore_index=True)
        readyTable.to_excel(path)
    except:
        return 'Something went wrong...'
    return f'Success! Please check {path}'


if __name__ == '__main__':
    moviesList = getMoviesList(getSitePageInText(url))
    print('Passed 1st func')
    movieDicts = [getMovieMainInfo(movie) for movie in moviesList]
    print('Created list of dicts')

    print(dataToTable(movieDicts))
