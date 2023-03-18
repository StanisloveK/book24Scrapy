# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class BooksPipeline:
    """Book24.ru parser pipeline."""
    def __init__(self):
        """Constructor."""
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.books

    def process_item(self, item, spider):
        """Process item."""
        collection = self.mongo_base[spider.name]
        item['own_price'] = item['own_price'].replace(r'\xa0', '').replace(r' ', '').replace(r'₽', '') + '₽'
        if item['sale_price']:
            item['sale_price'] = item['sale_price'].replace(r'\xa0', '').replace(r' ', '').replace(r'₽', '') + '₽'
        else:
            item['sale_price'] = 'Нет скидки'
        if item['rating']:
            item['rating'] = float(item['rating'])
        else:
            item['rating'] = 'Нет рейтинга'
        collection.update_one(item, {'$setOnInsert': item}, upsert=True)
        return item
