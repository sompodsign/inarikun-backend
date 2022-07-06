import requests
from bs4 import BeautifulSoup


class BaseSoupScraper:

    def __init__(self, url):
        self.url = url
        response = requests.get(url)
        self.soup = BeautifulSoup(response.content.decode('utf-8'), 'html.parser')

    def get_title(self):
        return self.soup.title.text

    def get_html(self):
        return self.soup

    def get_links(self):
        self.get_html()
        return self.soup.find_all('a')

    def get_all_images(self):
        return self.soup.find_all('img')


