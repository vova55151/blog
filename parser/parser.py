import json
import os
import urllib

import requests
import codecs
from bs4 import BeautifulSoup as BS
from random import randint

import apps.blogapp.models
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


# TODO : rosetta
# TODO : https://docs.djangoproject.com/en/3.2/ref/contrib/admin/actions/
def parse():
    """
    Парсит https://www.championat.com
    :return:
    """
    domain = 'https://www.championat.com'
    data = []
    for page in range(100, 0, -1):  # пагинация
        url = f'https://www.championat.com/articles/{page}.html'  # url страницы
        resp = requests.get(url, headers=headers[randint(0, 2)])
        if resp.status_code == 200:
            soup = BS(resp.content, 'lxml')
            main_div = soup.find('div', attrs={'class': 'article-preview-list'})  # основной div
            if main_div:
                divl = main_div.find_all('div', attrs={'class': 'article-preview__info'})
                for div in divl:
                    try:
                        href = div.a['href']
                        href = domain + href  # url каждой статьи
                        category = div.find('div', attrs={'class': 'article-preview__details'}).a.text
                        print(href)
                        resp = requests.get(href, headers=headers[randint(0, 2)])
                        soup = BS(resp.content, 'lxml')
                        page_main = soup.find('div', attrs={'class': 'page-main'})
                        date_created = page_main.find('div', attrs={'class': 'article-head__details'}).find('time').text
                        name = page_main.find('div', attrs={'class': 'article-head__title'}).text
                        descr = page_main.find('div', attrs={'class': 'article-head__subtitle'}).text
                        content_p = page_main.find_all('p')
                        content = []
                        for i in content_p:
                            content.append(i.text)
                        content = ' '.join(content)
                        img = page_main.find('div', attrs={'class': 'article-head__photo'}).img['src']
                        img2 = page_main.find('div', attrs={'class': 'content-photo'}).img['src']
                        image_name = img.rpartition('/')[2]
                        image_name2 = img2.rpartition('/')[2]
                        urllib.request.urlretrieve(img, f'/home/wcpc/proj/blog/media/{image_name}')
                        urllib.request.urlretrieve(img2, f'/home/wcpc/proj/blog/media/{image_name2}')
                        if apps.blogapp.models.Article.objects.filter(name=name).exists():
                            print('Статья уже существует')
                        else:
                            data.append(
                                [
                                    {'name': name},
                                    {'descr': descr},
                                    {'category': category},
                                    {'content': content},
                                    {'img': image_name},
                                    {'img2': image_name2},
                                    {'date_created': date_created}
                                ]
                            )
                    except Exception as e:
                        pass
    with open('data.json', 'w') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
