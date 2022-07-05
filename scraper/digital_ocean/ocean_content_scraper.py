from django.contrib.auth import get_user_model
import re
import pandas as pd

from ..bs_base import BaseSoupScraper

from blog.models import Category, Article, ArticleTag

User = get_user_model()


def get_content(link):
    tutorial_soup = BaseSoupScraper(link)
    tutorial_soup.get_html()
    tags = tutorial_soup.soup.find_all('a', class_=re.compile('TagStyles__StyledTag'))
    tags = [tag.text for tag in tags]
    title = tutorial_soup.soup.find('h1', class_=re.compile('HeadingStyles__StyledH1')).text
    content = tutorial_soup.soup.find('div', class_=re.compile('Markdown_markdown__')).text
    return {'title': title, 'content': content, 'tags': tags}


def get_tutorial_links(csv):
    df = pd.read_csv(csv)
    return df['href'].to_list()


def save_tutorial_content_in_db(tutorial_content):
    article = Article(
        title=tutorial_content['title'],
        content=tutorial_content['content'],
        author=User.objects.get(username='shampad'),
    )
    for tag in tutorial_content['tags']:
        article.articletag_set = ArticleTag(name=tag)
    article.save()


def get_and_save_content():
    links = get_tutorial_links('scraper/digital_ocean/digital_ocean_tutorials.csv')
    for link in links:
        content = get_content(link)
        save_tutorial_content_in_db(content)
