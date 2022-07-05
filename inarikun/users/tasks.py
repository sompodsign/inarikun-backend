from config import celery_app
from scraper.digital_ocean.ocean_content_scraper import get_new_articles_content_and_save_to_db


@celery_app.task()
def check_new_articles_and_save():
    """check for new tutorials and save to db if new available"""
    get_new_articles_content_and_save_to_db()

