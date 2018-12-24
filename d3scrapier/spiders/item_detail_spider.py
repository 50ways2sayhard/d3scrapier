import scrapy
import json
from scrapy import Request

from d3scrapier.tools.path_tools import get_data_file
from d3scrapier.tools.url_tools import extract_url
from d3scrapier.spiders import base_url


class ItemDetailSpider(scrapy.Spider):
    name = "ItemDetailSpider"
    start_urls = ['http://db.d.163.com/cn/item/prides-fall-80.html']

    # def start_requests(self):
    #     with open(get_data_file('items.json'), 'r') as items:
    #         for line in items:
    #             relative_url = json.loads(line)['ref']
    #             yield Request(url=base_url + relative_url)

    def parse(self, response):
        # icon
        icon = response.xpath(
            '//div[@class="detail-icon"]//span/@style').extract_first()
        details = response.xpath('//div[@class="detail-text"]')

        # 名称等基础
        name = self.parse_name(details)
        kind, clazz, limit, slot = self.parse_kind_class_limit_slot(details)

        # 护甲 攻击
        raw_armor_weapon = details.xpath('.//ul[@class="item-armor-weapon"]/li')
        armor_weapon = self.parse_armor_weapon(raw_armor_weapon)

        # 效果
        raw_effects = details.xpath('.//ul[@class="item-effects"]/li')
        effects = self.parse_effect(raw_effects)

        # 套装效果
        raw_set = details.xpath('.//ul[@class="item-itemset"]')

        # 物品等级、耐久等

        # 描述

        # wiki

        # 词缀

        # 掉落

        yield {
            'name': name,
            'kind': kind,
            'clazz': clazz,
            'limit': limit,
            'slot': slot,
            'armor_weapon': armor_weapon,
            'effects': effects
        }

    def parse_name(self, response):
        name = response.xpath('./h1/text()').extract_first().strip()
        return name

    def parse_kind_class_limit_slot(self, response):
        slot = response.xpath(
            './/span[@class="item-slot"]/text()').extract_first()
        limit = response.xpath(
            './/span[@class="item-class-specific"]/text()').extract_first()
        kt = response.xpath(
            './/div[@class="item-type"]//span/text()').extract_first().strip()
        kind, clazz = kt.split(' ')
        return kind, clazz, limit, slot

    def parse_armor_weapon(self, response):
        digit = response.xpath(
            './/span[@class="value"]/text()').extract_first().strip()
        kind = response.xpath('./text()').extract()[1].strip()
        return digit + kind

    def parse_effect(self, response):
        effects = []
        for each in response:
            if each.xpath('./@class').extract_first() == 'item-effects-choice':
                e = []
                for li in each.xpath('.//li'):
                    e.append(''.join(li.xpath('.//text()').extract()))
            else:
                e = ''.join(each.xpath('.//text()').extract())
            effects.append(e)

        return effects

    def parse_extras(self, response):
        pass

    def parse_description(self, response):
        pass

    def parse_wiki(self, response):
        pass

    def parse_cizhui(self, response):
        pass

    def parse_set_effects(self, response):
        # 套装名
        set_name = ''.join(response.xpath('./li[1]//text()').extract())
        
        # 套装部件名

        # 套装效果

    def parse_drop(self, response):
        pass