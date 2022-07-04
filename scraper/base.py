from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from driver_actions import DriverActions


class BaseScraper:

    OPTIONS = Options()
    OPTIONS.add_argument('--headless')

    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.OPTIONS)
        self.driver.maximize_window()
        self.driver.get(url)
        self.soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        self.driver_actions = DriverActions(self.driver)

    @staticmethod
    def parse_html(page_source):
        return BeautifulSoup(page_source, 'html.parser')

    def get_prettify(self, page_source):
        return self.parse_html(page_source).prettify()

    def get_title(self):
        return self.driver.title

    def get_html(self):
        self.driver_actions = DriverActions(self.driver)
        self.soup = self.parse_html(self.driver.page_source)

    def get_driver(self):
        return self.driver

    def get_soup(self):
        return self.soup

    def get_links(self):
        self.get_html()
        return self.soup.find_all('a')

    def get_all_images(self):
        self.get_html()
        return self.soup.find_all('img')

    def convert_to_csv(self, data):
        pass

    def convert_to_json(self, data):
        pass

    def convert_to_xml(self, data):
        pass

    def convert_to_yaml(self, data):
        pass

    def convert_to_html(self, data):
        pass

    def convert_to_markdown(self, data):
        pass

    def close(self):
        self.driver.close()
