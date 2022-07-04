import re
import pandas as pd

from bs_base import BaseSoupScraper


def get_content(link):
    tutorial_soup = BaseSoupScraper(link)
    tutorial_soup.get_html()
    tags = tutorial_soup.soup.find_all('a', class_=re.compile('TagStyles__StyledTag'))
    tags = [tag.text for tag in tags]
    title = tutorial_soup.soup.find('h1', class_=re.compile('HeadingStyles__StyledH1')).text
    content = tutorial_soup.soup.find('div', class_=re.compile('Markdown_markdown__'))
    return {'title': title, 'content': content, 'tags': tags}


def get_tutorial_links(csv):
    df = pd.read_csv(csv)
    return df['href'].to_list()


def get_tutorial_content():
    links = get_tutorial_links('digital_ocean_tutorials.csv')
    for link in links:
        content = get_content(link)
        return content


get_tutorial_content()
