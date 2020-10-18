# tasks
from __future__ import absolute_import, unicode_literals
from celery import Celery, app, shared_task
import requests
from bs4 import BeautifulSoup
import lxml
import json
from datetime import datetime
# loggin
from celery.utils.log import get_task_logger
from .models import News
from django.utils import timezone
from django.utils.timezone import now, pytz
from django.conf import settings


logger = get_task_logger(__name__)
user_timezone = pytz.timezone(settings.TIME_ZONE)


# save function
@shared_task(serializer='json')
def save_function(article_list):
    print('starting saving')
    source = article_list[0]['source']
    new_count = 0
    print(source)

    error = True
    try:
        latest_article = News.objects.filter(source=source).order_by('-id')[0]
        print(latest_article.published)
    except Exception as e:
        print('Exception at latest_article 1 ', source)
        print(e)
        error = False
        pass
    finally:
        if error is not True:
            latest_article = None

    for article in article_list:
        if latest_article is None:
            try:
                News.objects.create(
                    title=article['title'],
                    link=article['link'],
                    published=article['published'],
                    source=article['source'],
                    category="Sports"
                )
                new_count += 1
            except Exception as e:
                print('Failed at latest_article is none {}'.format(source))
                print(e)
                break
        elif latest_article.published is None:
            try:
                News.objects.create(
                    title=article['title'],
                    link=article['link'],
                    published=article['published'],
                    source=article['source'],
                    category="Sports"
                )
                new_count += 1
            except:
                print('failed at latest_article.published == None {}'.format(source))
                break
        elif latest_article.source is None:
            try:
                News.objects.create(
                    title=article['title'],
                    link=article['link'],
                    published=article['published'],
                    source=article['source'],
                    category="Sports"
                )
                new_count += 1
            except:
                print('failed at latest_article.source == None ', source)
                break
        elif latest_article.published.astimezone(user_timezone) < article['published'].astimezone(user_timezone):
            try:
                News.objects.create(
                    title=article['title'],
                    link=article['link'],
                    published=article['published'],
                    source=article['source'],
                    category="Sports"
                )
                new_count += 1
            except:
                print(
                    'failed at latest_article.published < article[published]', latest_article.published, " ", article['published'], " ",source)
                break
        else:
            return print('news scraping failed, date was more recent than last published date {}'.format(source))
    logger.info(f'New articles: {new_count} article(s) added.')
    return print('finished')


# scraping function
@shared_task
def sports_rss():
    article_list = []
    try:
        print('Starting scraping of Sports')
        r = requests.get('https://www.sports.ru/figure-skating/')
        soup = BeautifulSoup(r.content, 'html.parser')
        articles = soup.find_all('p')
        for a in articles:
            if (a.find('span', class_='date') is not None and a.find('a', class_='short-text', href=True) is not None):
                title = a.find('a', class_='short-text', href=True).text
                link = a.find('a', class_='short-text', href=True)
                if "figure-skating" in link.get('href'):
                    published_wrong_1 = datetime.date(datetime.now())
                    published_wrong_2 = a.find('span', class_='date').text
                    published_wrong = str(published_wrong_1) + \
                        " " + str(published_wrong_2)
                    published = datetime.strptime(
                        published_wrong, '%Y-%m-%d %H:%M')

                    if link.get('href').startswith("https://www.sports.ru/"):
                        new_link = link.get('href')
                    else:
                        new_link = "https://www.sports.ru/" + link.get('href')

                    article = {
                        'title': title,
                        'link': new_link,
                        'published': published,
                        'source': 'sports',
                        'category': "Sports"
                    }

                    article_list.append(article)
        for i in article_list:
            print(i)
        print('Finished scraping the article')
        return save_function(article_list)
    except Exception as e:
        print('The scraping job failed. See exception: ', "SPORTS")
        print(e)

# scraping function


@shared_task
def hackernews_rss():
    article_list = []

    try:
        print('Starting the scraping tool hacks')
        # execute my request, parse the data using XML
        # parser in BS4
        r = requests.get('https://news.ycombinator.com/rss')
        soup = BeautifulSoup(r.content, features='xml')

        # select only the "items" I want from the data
        articles = soup.findAll('item')

        # for each "item" I want, parse it into a list
        for a in articles:
            title = a.find('title').text
            link = a.find('link').text
            published_wrong = a.find('pubDate').text
            published = datetime.strptime(
                published_wrong, '%a, %d %b %Y %H:%M:%S %z')
            # print(published, published_wrong) # checking correct date format

            # create an "article" object with the data
            # from each "item"
            article = {
                'title': title,
                'link': link,
                'published': published,
                'source': 'HackerNews RSS',
                'category': "hacks_news"
            }

            # append my "article_list" with each "article" object
            article_list.append(article)

        print('Finished scraping the articles')
        # after the loop, dump my saved objects into a .txt file
        return save_function(article_list)
    except Exception as e:
        print('The scraping job failed. See exception: ', "HACKS")
        print(e)


# scraping function
@shared_task
def games_rss():
    article_list = []

    try:
        print('Starting the scraping tool games')
        # execute my request, parse the data using XML
        # parser in BS4
        r = requests.get('https://ru.ign.com/')
        soup = BeautifulSoup(r.content, features='xml')

        # select only the "items" I want from the data
        articles = soup.find_all('div', class_='m')

        # for each "item" I want, parse it into a list
        for a in articles:
            if (a.find('h3') is not None and a.find('a').get('href') is not None):
                title = a.find('h3').text
                link = a.find('a').get('href')
                published3 = a.find('time').get('datetime')
                published2 = published3.replace('T', ' ')
                published1 = published2.replace('+03:00', '')
                published = datetime.strptime(published1, '%Y-%m-%d %H:%M:%S')
                article = {
                    'title': title,
                    'link': link,
                    'published': published,
                    'source': "Games",
                    'category': "Games"
                }

                # append my "article_list" with each "article" object
                article_list.append(article)
        # print(article_list)

        print('Finished scraping the articles')
        # after the loop, dump my saved objects into a .txt file
        return save_function(article_list)
    except Exception as e:
        print('The scraping job failed {}. See exception: ', "GAMES")
        print(e)

# MOVIES


@shared_task
def movies_rss():
    article_list = []

    try:
        print('Starting the scraping tool movies')
        # execute my request, parse the data using XML
        # parser in BS4
        r = requests.get('https://www.kinoafisha.info/news/')
        soup = BeautifulSoup(r.content, features='html.parser')

        # select only the "items" I want from the data
        articles = soup.find_all('div', class_='newsV2_item')

        # for each "item" I want, parse it into a list
        for a in articles:
            if (a.find('span', class_='newsV2_date') is not None and a.find('a').get('href') is not None and a.find('span', class_='newsV2_date') is not None):
                title = a.find('img', class_='picture_image').get('alt')
                link = a.find('a').get('href')
                published_wrong1 = a.find('span', class_='newsV2_date').text
                months = {
                    'октября': 10,
                    'ноября': 11
                }
                print(published_wrong1)
                for key in months:
                    if key in published_wrong1:
                        published_wrong = published_wrong1.replace(
                            key, str(months[key]))

                published = datetime.strptime(published_wrong, '%d %m %Y %H:%M')
                article = {
                    'title': title,
                    'link': link,
                    'published': published,
                    'source': "Movies",
                    'category': "Movies"
                }

                # append my "article_list" with each "article" object
                article_list.append(article)

        print('Finished scraping the articles')
        # after the loop, dump my saved objects into a .txt file
        return save_function(article_list)
    except Exception as e:
        print('The scraping job failed. See exception:', "MOVIES")
        print(e)

