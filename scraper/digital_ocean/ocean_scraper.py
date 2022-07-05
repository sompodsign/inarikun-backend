from blog.models import Article
from ..digital_ocean.digital_ocean_selenium import DigitalOcean
import csv
import pandas as pd

digitalOcean = DigitalOcean('https://www.digitalocean.com/community/tutorials')

total_links = len(digitalOcean.get_all_tutorial_links())


def is_last_page(total_amount, current_amount):
    return total_amount > current_amount


def store_in_csv(tutorial_href):
    file = open('.digital_ocean_tutorials.csv', 'a')
    writer = csv.writer(file)

    existing_links = pd.read_csv('./digital_ocean_tutorials.csv')['href'].to_list()
    if tutorial_href and tutorial_href not in existing_links:
        print("new link: " + tutorial_href)
        writer.writerow([tutorial_href])

    file.close()


while True:
    digitalOcean.click_show_more_button()
    digitalOcean.get_html()
    current_amount_of_links = len(digitalOcean.get_all_tutorial_links())
    print(f'Current amount of links: {current_amount_of_links}')

    tutorial_links = digitalOcean.get_all_tutorial_links()

    if is_last_page(current_amount_of_links, total_links):
        total_links = current_amount_of_links

        for link in tutorial_links:
            store_in_csv(link)

    else:
        break

