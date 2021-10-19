import site

from blg.celery import app
@app.task
def send_email(lst,author,url):
    for user in lst:
        user.email_user('Новая статья', f'{user.email},{author} выложил новую статью.{url} ', 'from_email@test.com')