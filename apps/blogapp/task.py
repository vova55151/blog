import json
import uuid

from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy

import apps.blogapp.models
from blg.celery import app
from blg.utils import from_cyrillic_to_eng
from parser.parser import parse


@app.task
def send_email(author_pk, url):
    """
    отправляет email
    """
    author = get_user_model().objects.filter(pk=author_pk).first()
    for user in author.subscribers.all():
        user.email_user(ugettext_lazy('Новая статья'),  # TODO: проверить через sendgrid(перед этим убрать расслку из сейва)
                        ugettext_lazy(f'{user.email},{author} выложил новую статью.{url}'), 'from_email@test.com')


@app.task
def pars():
    parse()


@app.task
def load_from_json():
    """
    загружает данные в базу
    :return:
    """
    user = get_user_model().objects.first()
    with open('/home/wcpc/proj/blog/data.json', 'r') as data:
        dataset = json.loads(data.read())
        for lst in dataset:
            category = apps.blogapp.models.Category.objects.filter(name=lst[2]['category']).first()
            if apps.blogapp.models.Category.objects.filter(name=lst[2]['category']).exists():
                article = apps.blogapp.models.Article(name=lst[0]['name'],
                                                      slug=from_cyrillic_to_eng(lst[0]['name']),
                                                      category=category,
                                                      preview=lst[4]['img'].rpartition('/')[2],
                                                      descr=lst[1]['descr'],
                                                      author=user,
                                                      content=lst[3]['content'])
                article.save()
                apps.blogapp.models.Image(img=lst[5]['img2'].rpartition('/')[2],
                                          alt=str(uuid.uuid4()),
                                          article=article).save()
                print(article)
            else:
                category = apps.blogapp.models.Category(name=lst[2]['category'],
                                                        slug=from_cyrillic_to_eng(lst[2]['category']),
                                                        depth=1,
                                                        path=str(uuid.uuid4()), ).save()
                article = apps.blogapp.models.Article(name=lst[0]['name'],
                                                      slug=from_cyrillic_to_eng(lst[0]['name']),
                                                      category=category,
                                                      preview=lst[4]['img'].rpartition('/', )[2],
                                                      descr=lst[1]['descr'],
                                                      author=user,
                                                      content=lst[3]['content'])
                article.save()
                apps.blogapp.models.Image(img=lst[5]['img2'].rpartition('/')[2],
                                          alt=str(uuid.uuid4()),
                                          article=article).save()
                print(article)
