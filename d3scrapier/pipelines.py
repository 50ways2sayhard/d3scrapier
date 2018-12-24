# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from d3scrapier.tools.path_tools import get_data_folder


class D3ScrapierPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonWriterPipeline(object):
    def open_spider(self, spider):
        data_folder = get_data_folder()
        print('*'*50)
        print('Start serialize...')
        if spider.name != 'default':
            self.file = open(data_folder + '/' + spider.name + '.json', 'w')

    def close_spider(self, spider):
        print('*'*50)
        print('Finish serialize....')
        if spider.name != 'default':
            self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + '\n'
        if spider.name != 'default':
            self.file.write(line)
        return item
