from scrapy.exceptions import DropItem
import json


class TextPipeline(object):
    def __init__(self):
        self.limit = 50

    def process_item(self, item, spider):
        if item['text']:
            if len(item['text']) > self.limit:
                item['text'] = item['text'][0:self.limit].rstrip() + '...'
            return item
        else:
            return DropItem('Missing Text')


class JsonPipeline(object):
    def __init__(self, filename):
        self.filename = filename
        self.json_data = []
        self.file = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            filename=crawler.settings.get('JSON_FILENAME')
        )

    def open_spider(self, spider):
        self.file = open(self.filename, 'w', encoding='utf-8')

    def process_item(self, item, spider):
        self.json_data.append(dict(item))
        return item

    def close_spider(self, spider):
        self.file.write(json.dumps(self.json_data, ensure_ascii=False, indent=2))
        self.file.close()
