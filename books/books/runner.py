import sys
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
import settings
from spiders.book24 import Book24Spider


def _main():
    """Entry point."""
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(Book24Spider)

    process.start()


if __name__ == '__main__':
    sys.exit(_main())