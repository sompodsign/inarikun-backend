from config import celery_app
from scraper.digital_ocean.ocean_content_scraper import get_and_save_content, get_new_articles_content_and_save_to_db


@celery_app.task()
def crawl_tutorials_from_digital_ocean():
    """crawl tutorials from digital ocean"""
    get_and_save_content()


@celery_app.task()
def crawl_new_tutorials_from_digital_ocean():
    """crawl new tutorials from digital ocean"""
    get_new_articles_content_and_save_to_db()
