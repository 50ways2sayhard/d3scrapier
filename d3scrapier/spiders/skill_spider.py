import scrapy
from scrapy import Request
from d3scrapier.spiders import base_url
import json


class SkillSpider(scrapy.Spider):
    name = "skills"

    def start_requests(self):
        menus = json.load(open('/Users/GJT/workspace/d3scrapier/catalogue.json', 'r'))
        skills = menus['技能']
        for values in skills.values():
            for url in values.values():
                yield Request(base_url + url, callback=self.parse)
        
    def parse(self, response):
        _ = response.xpath('//p[@class="m-seach-posi"]/a/text()').extract()
        job, kind = _[-2], _[-1]
        for raw_skill in response.xpath('//tbody/tr'):
            desc = raw_skill.xpath('./td')
            name, ref = self.extract_name_ref(desc[0])
            icon = self.extract_icon(desc[0])
            attr = desc[1].xpath('./span/text()').extract_first()
            runes = desc[2].xpath('.//a/@name').extract()
            learn_level = desc[3].xpath('./text()').extract_first()
            yield {
                "job":job,
                "kind": kind,
                "name": name,
                "ref": ref,
                'icon': icon,
                'attr': attr,
                'runes': runes,
                'learn_level': learn_level
            }

    def extract_icon(self, response):
        import re
        raw_url = response.xpath('.//span/@style').extract_first()
        return re.search('\((.+)\)', raw_url).group(1)

    def extract_name_ref(self, response):
        name = response.xpath('.//a/@name').extract_first()
        ref = response.xpath('.//a/@href').extract_first()
        return name, ref