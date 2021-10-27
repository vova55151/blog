import json
import uuid

from apps.blogapp.models import Category, Image, Article
from blg.celery import app
from blg.utils import from_cyrillic_to_eng
from parser.parser import parse


@app.task
def send_email(lst, author, url):
    """
    отправляет email
    :param lst: список получателей
    :param author: автор
    :param url: ссылка на пост
    :return:
    """
    for user in lst:
        user.email_user('Новая статья', f'{user.email},{author} выложил новую статью.{url} ', 'from_email@test.com')


@app.task
def pars():
    parse()


@app.task
def load_from_json(user):
    """
    загружает данные в базу
    :param user: автор
    :return:
    """
    with open('/home/wcpc/proj/blog/parser/data.json', 'r') as data:
        dataset = json.loads(data.read())
        for lst in dataset:
            category = Category.objects.filter(name=lst[2]['category']).first()
            if Category.objects.filter(name=lst[2]['category']).exists():
                article = Article(name=lst[0]['name'],
                                  slug=from_cyrillic_to_eng(lst[0]['name']),
                                  category=category,
                                  preview=lst[4]['img'].rpartition('/')[2],
                                  descr=lst[1]['descr'],
                                  author=user,
                                  content=lst[3]['content'])
                article.save()
                img = Image(img=lst[5]['img2'].rpartition('/')[2],
                            alt=str(uuid.uuid4()),
                            article=article).save()

            else:
                category = Category(name=lst[2]['category'],
                                    slug=from_cyrillic_to_eng(lst[2]['category']),
                                    depth=1,
                                    path=str(uuid.uuid4()), ).save()
                article = Article(name=lst[0]['name'],
                                  slug=from_cyrillic_to_eng(lst[0]['name']),
                                  category=category,
                                  preview=lst[4]['img'].rpartition('/', )[2],
                                  descr=lst[1]['descr'],
                                  author=user,
                                  content=lst[3]['content'])
                article.save()
                img = Image(img=lst[5]['img2'].rpartition('/')[2],
                            alt=str(uuid.uuid4()),
                            article=article).save()
