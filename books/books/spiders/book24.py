import scrapy
from scrapy.http import HtmlResponse
from books.items import BooksItem


class Book24Spider(scrapy.Spider):
    name = 'book24'
    url = 'https://book24.ru'
    allowed_domains = ['book24.ru']
    start_urls = ['https://book24.ru/novie-knigi/']

    def parse(self, response):
        links = response.xpath('//div[@class="product-card__image-holder"]/a/@href').extract()
        total_pages = re.findall(r'\d+', re.search(r'totalPages:\d+,', response.text).group())[0]
        for link in links:
            yield response.follow(self.url + link, callback=self.parse_item)

        for page in range(2, int(total_pages)+1):
            yield response.follow(self.url + '/novie-knigi/page-%s' % page, callback=self.parse)

    @staticmethod
    def parse_item(response: HtmlResponse):
        title = response.xpath('//h1/text()').extract_first()
        link = response.url
        author = response.xpath('//dd[@class="product-characteristic__value"]/a[contains(@href, "author")]/text()').extract_first()
        own_price = response.xpath('//span[contains(@class, "product-sidebar-price__price-old")]/text()').extract_first()
        if not own_price:
            own_price = response.xpath('//meta[@itemprop = "price"]/@content').extract_first()
            sale_price = None
        else:
            sale_price = response.xpath('//div[contains(@itemprop, "offers")]/span/text()').extract_first()
        rating = response.xpath('//div[contains(@class, "product-ratings-widget__item")]/div/div/button/span[contains(@class, "rating-widget__main-text")]/text()').extract_first()
        yield BooksItem(title=title, link=link, author=author, own_price=own_price, sale_price=sale_price, rating=rating)
