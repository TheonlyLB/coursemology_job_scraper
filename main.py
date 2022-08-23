from scraper import SXCScraper, OSPScraper, JobStreetScraper, FastJobsScraper
from datetime import datetime
import pandas as pd
import requests

datetime_str = str(datetime.now().strftime("%d%m%Y"))


def merge_txt():
    # merges text files from different scrapers
    filenames = [r'sxc%s.txt'%datetime_str, r'osp%s.txt'%datetime_str,
                 r'jobstreet%s.txt'%datetime_str,r'fastjobs%s.txt'%datetime_str]
    with open('output%s.txt'%datetime_str, 'a',encoding='utf-8') as outfile:
        for fname in filenames:
            with open(fname,'r',encoding='utf-8') as infile:
                for line in infile:
                    outfile.write(line)


def merge_csv():
    # merges csv files from different scrapers
    filenames = [
                r'sxc%s.csv'%datetime_str,
                 #r'osp%s.csv'%datetime_str,
                 #r'jobstreet%s.csv'%datetime_str,
                 #r'fastjobs%s.csv'%datetime_str
                 ]
    output = pd.concat([pd.read_csv(f) for f in filenames])
    output.to_csv('output%s.csv'%datetime_str, index=False)


if __name__ == '__main__':
    scrapers = [
        OSPScraper(),
        SXCScraper(),
        JobStreetScraper(),
        FastJobsScraper(),
    ]

    for scraper in scrapers:
        print(f"Scraper {scraper.name} started!")
        scraper.scrape()
        scraper.censor()
        # Handle exception raised when no jobs are scraped
        # scraper.save_as_csv()
        # scraper.save_as_txt()
        print(f"Scraping completed for {scraper.name}, valid jobs scraped: {len(scraper.job_list)}")
        scraper.save_to_wp(limit=100)
    #merge_txt()
    #merge_csv()