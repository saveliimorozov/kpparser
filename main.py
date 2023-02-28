import time
import requestConfig as rc

import requests as req
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent
import pandas as pd
import random

url = 'https://www.kinopoisk.ru/lists/movies/top-250-2020/?page='


def getSitePageInText(url: str, params: dict):
    # headers = ['UserAgent().safari',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',

    #            'UserAgent().opera']
    # urlReq = req.get(url, headers={
    #         'User-Agent': headers[curPage % 3 - 1]})
    urlReq = req.get(url,
                     params=params,
                     cookies=rc.cookies,
                     headers=rc.headers)
    print(f'Cur page = {params["page"]}')
    # urlReq = req.get(url, headers={'User-Agent': UserAgent().safari})
    time.sleep(1)
    print(urlReq)
    time.sleep(2)

    soupUrlReq = bs(urlReq.text, 'lxml')
    time.sleep(1)
    # print(soupUrlReq)

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
    try:
        readyTable = pd.DataFrame([dictsList[0].values()], columns=list(dictsList[0].keys()))
        for i in range(1, len(dictsList)):
            tempDF = pd.DataFrame([dictsList[i].values()], columns=list(dictsList[i].keys()))
            readyTable = pd.concat([readyTable, tempDF], ignore_index=True)
    except Exception as err:
        readyTable = pd.DataFrame([f'Error create df...{err}'])
        return readyTable
    return readyTable


def dataToFile(dfDist: dict):
    path = 'Films.xlsx'
    try:
        readyTable = pd.concat(list(dfDict.values()), ignore_index=True)
        readyTable.to_excel(path)
    except Exception as err:
        return f'Error writing to file...\n{err}'
    return f'\nSuccess! Please check {path}'


if __name__ == '__main__':
    pagesNum = int(input('Input pages needed(1-5):'))

    if not 1 <= pagesNum <= 5:
        print('Wrong number')
        exit()
    else:
        curPage = 1
        params = {}
        dfDict = {}
        while curPage != pagesNum + 1:
            randTime = random.randint(3, 10)
            print(f'Sleep for {randTime} sec')
            time.sleep(randTime)

            params['page'] = str(curPage)
            moviesList = getMoviesList(getSitePageInText(url + str(curPage), params))
            print('First 3 movies from movieList:')
            print(moviesList[:3])
            print('\nPassed 1st func\n')
            movieDicts = [getMovieMainInfo(movie) for movie in moviesList]
            print('First 3 moviesDICT from movieDICTList:')
            print(movieDicts[:3])
            print('\nCreated list of dicts\n')

            df = dataToTable(movieDicts)
            print('Current df:')
            print(df)

            dfDict[curPage] = df
            print(f'{curPage} page(s) - done\n')
            curPage += 1
            # ranTime = random.randint(180, 200)
            # print(f'Sleep for {ranTime} sec')
            # time.sleep(ranTime)
        print(dataToFile(dfDict))
