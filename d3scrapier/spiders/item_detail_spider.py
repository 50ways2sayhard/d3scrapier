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
        raw_armor_weapon = details.xpath(
            './/ul[@class="item-armor-weapon"]/li')
        armor_weapon = self.parse_armor_weapon(raw_armor_weapon)

        # 效果
        raw_effects = details.xpath('.//ul[@class="item-effects"]/li')
        effects = self.parse_effect(raw_effects)

        # 套装效果
        raw_set = details.xpath('.//ul[@class="item-itemset"]')
        set_effects = self.parse_set_effects(raw_set) if raw_set != [] else {}

        # 物品等级、耐久等
        raw_extras = details.xpath('.//ul[@class="item-extras"]')
        extras = self.parse_extras(raw_extras)

        # 描述
        desc = self.parse_description(response)

        # wiki
        wiki = self.parse_wiki(response)

        # 词缀
        raw_cizhui = response.xpath('//div[@id="cizhui_table"]//table')
        cizhui = self.parse_cizhui(raw_cizhui)

        # 掉落
        raw_drop_table = response.xpath('//div[@class="m-diaoluo"]/table')
        drop = self.parse_drop(raw_drop_table)

        yield {
            'name': name,
            'kind': kind,
            'clazz': clazz,
            'limit': limit,
            'slot': slot,
            'armor_weapon': armor_weapon,
            'effects': effects,
            'set': set_effects,
            'extras': extras,
            "description": desc,
            "drop": drop,
            "cizhui": cizhui
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
        d = {}
        for each in response.xpath('./li'):
            ex = each.xpath('./span/text()').extract()
            d[ex[0]] = ex[1]

        return d

    def parse_description(self, response):
        return response.xpath(
            '//div[@class="item-flavor d3-color-orange serif"]/text()'
        ).extract_first()

    def parse_wiki(self, response):
        return ''.join(
            response.xpath('//div[@class="item-disc mb20 ovh"]//text()').
            extract()).strip()

    def parse_cizhui(self, response):
        thead = response.xpath('./thead/tr/th//text()').extract()
        cizhuis = []
        for cizhui in response.xpath('./tbody/tr'):
            values = []
            for each in cizhui.xpath('./td'):
                values.append(''.join(each.xpath('.//text()').extract()))
            cizhuis.append(dict(zip(thead, values)))

        return cizhuis

    def parse_set_effects(self, response):
        # 套装名
        set_name = ''.join(response.xpath('./li[1]//text()').extract())

        # 套装部件名
        pieces = response.xpath(
            './li[@class="item-item-set-piece indent d3-color-gray"]//text()'
        ).extract()

        # 套装效果
        amount = response.xpath(
            './li[@class="d3-color-gray item-itemset-bonus-amount"]//text()'
        ).extract()
        bonus = []
        # for b in response.xpath(
        #     './li[@class="d3-color-orange"]'):
        bonus = [
            ''.join(b.xpath('.//text()').extract())
            for b in response.xpath('./li[@class="d3-color-orange"]')
        ]
        set_bonus = dict(zip(amount, bonus))

        return {"set_name": set_name, "pieces": pieces, "bonus": set_bonus}

    def parse_drop(self, response):
        thead = response.xpath('./thead/tr/th//text()').extract()
        body = response.xpath('./tbody/tr/td//text()').extract()
        return dict(zip(thead, body))