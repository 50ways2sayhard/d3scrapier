import scrapy
from scrapy import Request
from d3scrapier.spiders import base_url
import re
import json


class ItemSpider(scrapy.Spider):
    name = 'items'
    items = {}

    def start_requests(self):
        pass
        menus = json.load(
            open('/Users/GJT/workspace/d3scrapier/catalogue.json', 'r'))
        catalogue = {**menus['护甲'], **menus['武器'], **menus['其他']}
        for v in catalogue.values():
            for k, url in v.items():
                yield Request(base_url + url, callback=self.parse)
        
    def parse(self, response):
        kind = ''
        for tdody in response.xpath('//tbody'):
            for tds in tdody.xpath('./tr'):
                # 处理每一条记录
                d = {}
                name_icon, others = tds.xpath(
                    './td')[0], tds.xpath('./td/text()')[2:].extract()
                kind = others[1]
                d['icon'] = self.extract_icon(name_icon)
                d['name'], d['ref'] = self.extract_name_ref(name_icon)
                d['quality'] = others[0]
                d['part'] = others[1]
                d['source'] = others[2]
                d['item_level'] = others[3]
                d['equip_level'] = others[4]
                yield d

    def extract_icon(self, response):
        raw_url = response.xpath('.//span/@style').extract_first()
        return re.search('\((.+)\)', raw_url).group(1)

    def extract_name_ref(self, response):
        a = response.xpath('./div/p/a')
        return a.xpath('./text()').extract_first(), a.xpath('./@href').extract_first()