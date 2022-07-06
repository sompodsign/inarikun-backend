import logging

from django.contrib.auth import get_user_model
import re
import pandas as pd

from ..bs_base import BaseSoupScraper

from blog.models import Article, ArticleTag

User = get_user_model()


def get_content(link):
    """get content from link"""
    tutorial_soup = BaseSoupScraper(link)
    tutorial_soup.get_html()
    tags = tutorial_soup.soup.find_all('a', class_=re.compile('TagStyles__StyledTag'))
    tags = [tag.text for tag in tags]
    title = tutorial_soup.soup.find('h1', class_=re.compile('HeadingStyles__StyledH1')).text
    content = tutorial_soup.soup.find('div', class_=re.compile('Markdown_markdown__'))
    return {'title': title, 'content': str(content), 'tags': tags}


def get_tutorial_links(csv):
    """get links from csv"""
    df = pd.read_csv(csv)
    return df['href'].to_list()


def save_tutorial_content_in_db(tutorial_content):
    """save content in db"""
    article = Article(
        title=tutorial_content['title'],
        content=tutorial_content['content'],
        author=User.objects.get(username='shampad'),
    )
    article.save()
    for tag in tutorial_content['tags']:
        existing_tags = ArticleTag.objects.all()
        if tag in [existing_tag.name for existing_tag in existing_tags]:
            article.articletag_set.add(existing_tags.get(name=tag))
        else:
            article.articletag_set.create(name=tag)
    article.save()


def get_and_save_content():
    """get content from all links in csv and save in db"""
    links = get_tutorial_links('scraper/digital_ocean/digital_ocean_tutorials.csv')
    for i in range(len(links)):
        print(f'{i+1}/{len(links)}')
        tutorial_content = get_content(links[i])
        save_tutorial_content_in_db(tutorial_content)


def get_new_articles():
    """
    check for new tutorials and returns links of new tutorials if available
    """
    existing_articles = [article.title.strip().lower() for article in Article.objects.all()]
    new_articles = []
    ocean = BaseSoupScraper('https://www.digitalocean.com/community/tutorials')
    link_elems = ocean.soup.find_all('a', href=re.compile('/community/tutorials/.*'))
    link_title_elems = [link_elem.find('h3', class_=re.compile('HeadingStyles__StyledH3')) for link_elem in link_elems]
    link_titles = [link_title_elem.text.strip().lower() for link_title_elem in link_title_elems]

    for link_title in link_titles:
        if link_title not in existing_articles:
            new_link = "https://digitalocean.com/community/tutorials" + link_elems[link_titles.index(link_title)].get('href')
            new_articles.append(new_link)
    return new_articles if new_articles else []  # list of new articles


def get_new_articles_content_and_save_to_db():
    """check for new tutorial and save to db if new available"""
    new_articles = get_new_articles()
    if new_articles:
        for i in range(len(new_articles)):
            tutorial_content = get_content(new_articles[i])
            save_tutorial_content_in_db(tutorial_content)
        logging.info(f'{len(new_articles)} new articles found and saved')
    else:
        logging.info('No new articles found')

