import json
import os
import urllib

import requests
import codecs
from bs4 import BeautifulSoup as BS
from random import randint

from blg.settings import BASE_DIR

headers = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
]


# TODO : python-slugify django-unique-slugify
def sportexpress():
    jobs = []
    errors = []
    domain = 'https://www.sport-express.ru'
    url = 'https://www.sport-express.ru/reviews/'
    if url:
        resp = requests.get(url, headers=headers[randint(0, 2)])
        if resp.status_code == 200:
            soup = BS(resp.content, 'lxml')
            main_div = soup.find('div', attrs={'class': 'se-press-list-page__items'})

            if main_div:
                counter = 0
                divl = main_div.find_all('div', attrs={'class': 'se-press-list-page__item'})
                for div in divl:
                    href = div.a['href']
                    resp = requests.get(href, headers=headers[randint(0, 2)])
                    soup = BS(resp.content, 'lxml')
                    main_div = soup.find('div', attrs={'class': 'publication-content'})
                    name = main_div.find('h1', attrs={'class': 'publication-title title-h1 mh_auto'}).text
                    descr = main_div.find('div', attrs={'class': 'w610_text vrez'}).text
                    # descr = descr1.p.span.text
                    print(f"Название статьи : {name}")
                    print(f"Краткое описание : {descr}")
                    author = main_div.find('div', attrs={'class': 'by-author__author-title'})
                    content = main_div.find('div', attrs={'class': 'js-swiptable-holder'})
                    a = content.text.strip("\n")
                    print(f'Контент : {a}')
                    if author:
                        print(f"Автор : {author.text}")
                    content2 = content.find_all('p')
                    content3 = []
                    for i in content2:
                        content3.append(i.text)
                    img = main_div.find('img', id='slideshow_1_is_main')['src']
                    urllib.request.urlretrieve(img, f'/home/proj/blog/parser/img')

                    counter += 1
                    if counter > 2:
                        break



            else:
                errors.append({'url': url, 'title': "Div does not exists"})
        else:
            errors.append({'url': url, 'title': "Page do not response"})

    return jobs, errors


sportexpress()
