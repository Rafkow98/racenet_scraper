import time

from scraper import scraper
from app import app

if __name__ == '__main__':
    scraper()
    while True:
        try:
            app()
            break
        except Exception as e:
            print(e)
            time.sleep(1)
