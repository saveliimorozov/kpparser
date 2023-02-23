import time

import requests as req
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent
import pandas as pd

url = 'https://www.kinopoisk.ru/lists/movies/top-250-2020/?page=1'


def getSitePageInText(url: str):

    urlReq = req.get(url, headers={'User-Agent': UserAgent().safari})
    time.sleep(1)
    print(urlReq)
    time.sleep(4)

    soupUrlReq = bs(urlReq.text, 'lxml')
    time.sleep(1)
    print(soupUrlReq)

    return soupUrlReq


def getMoviesList(soupUrlReq):
    # movieMainInfo = soupUrlReq.find('div', class_="styles_root__ti07r").find(
    #     'a', class_="base-movie-main-info_link__YwtP1")
    movieMainList = soupUrlReq.findAll('div', class_="styles_root__ti07r")
    time.sleep(4)
    return movieMainList


def getMovieMainInfo(singleMovieText):
    movieMainInfo = singleMovieText.find(
        lambda tag: tag.name == 'a' and tag.get('class') == ['base-movie-main-info_link__YwtP1'])

    movieLink = 'https://www.kinopoisk.ru' + movieMainInfo.get('href')

    movieNameRu = movieMainInfo.find('div', class_='base-movie-main-info_mainInfo__ZL_u3').find(
        'span', class_='styles_mainTitle__IFQyZ styles_activeMovieTittle__kJdJj').text

    movieNameOrig = movieMainInfo.find('div', class_='desktop-list-main-info_secondaryTitleSlot__mc0mI').find(
        'span', class_='desktop-list-main-info_secondaryTitle__ighTt').text

    movieYearandDuration = movieMainInfo.find(
        'span', class_="desktop-list-main-info_secondaryText__M_aus").contents[2]
    movieCountryTypeDirector = movieMainInfo.find(
        'span', class_="desktop-list-main-info_truncatedText__IMQRP").contents[0]

    singleMovieDict = {'Name' : movieNameRu,
                       'Original name' : movieNameOrig,
                       'Main information' : movieCountryTypeDirector,
                       'Additional information' : movieYearandDuration,
                       'Link' : movieLink
    }

    return singleMovieDict

def dataToTable(singleMovieDict:dict):
    readyTable = pd.DataFrame(columns=[key for key in singleMovieDict])
    # readyTable = readyTable.append(singleMovieDict, ignore_index=True )
    readyTable.loc[len(readyTable.index)] = list(singleMovieDict.values())
    readyTable.to_csv(r"C:\Users\morozsa\PycharmProjects\kpparser\ReadyTable.csv", sep='\t')

    return readyTable



if __name__ == '__main__':
    moviesList = getMoviesList(getSitePageInText(url))
    movieDict = getMovieMainInfo(moviesList[0])
    print(movieDict)
    with pd.option_context("display.max_rows", None, "display.max_columns", None):
        print(dataToTable(movieDict))
