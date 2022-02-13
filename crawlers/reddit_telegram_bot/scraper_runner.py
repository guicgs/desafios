import json
import os
import sys

from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from twisted.internet import reactor

from redditscraper.spiders.reddit_top_threads_scraper import (
    RedditTopThreadsScraper,
)


class ScraperRunner:
    def __init__(self, subreddits: str) -> None:
        self.subreddits = subreddits
        self.results_json_path = "./results/items.json"
        self.runner = CrawlerRunner(
            {
                "FEEDS": {
                    "results/items.json": {
                        "format": "json",
                        "overwrite": True,
                    },
                },
            }
        )

    def run_scraper(self) -> None:
        d = self.runner.crawl(
            RedditTopThreadsScraper, subreddits=self.subreddits
        )
        d.addBoth(lambda _: reactor.stop())
        reactor.run()

    def load_and_print_scraping_results(self) -> list:
        if (
            os.path.isfile(self.results_json_path)
            and os.path.getsize(self.results_json_path) > 0
        ):
            with open(self.results_json_path) as file:
                results_json = json.load(file)
                print(json.dumps(results_json, indent=2))
                return results_json


if __name__ == "__main__":
    configure_logging()

    try:
        subreddits = str(sys.argv[1]).split("=")[1]
    except IndexError:
        raise IndexError(
            """É necessário enviar pelo menos um subreddit
        da seguinte forma: `--subreddit="cats;sports"`"""
        )

    scraper_runner = ScraperRunner(subreddits=subreddits)
    scraper_runner.run_scraper()
    scraper_runner.load_and_print_scraping_results()
