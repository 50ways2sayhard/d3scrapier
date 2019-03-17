import scrapy
import json

from d3scrapier.tools.url_tools import extract_url
from d3scrapier.spiders import base_url
from scrapy import Request


class SkillDetailSpider(scrapy.Spider):
    name = "SkillDetailSpider"
    # skill = ''
    # start_urls = ['http://db.d.163.com/cn/skill/barbarian/active/bash.html']

    # def start_requests(self):
    #     for skill in open('/Users/GJT/workspace/d3scrapier/d3scrapier/data/skills.json', 'r'):
    #         s = json.loads(skill)
    #         self.skill = s
    #         yield Request(base_url + s['ref'], callback=self.parse)


    def parse(self, response):
        skill_detail = response.xpath(
            '//div[@class="db-detail-box skill-detail icon-size-default"]')
        runes = response.xpath('//div[@id="cizhui"]//table')

        yield {
            'item_type': 'skill',
            'text': self.parse_skill_detail(skill_detail),
            'runes': self.parse_runes(runes)
        }

    def parse_skill_detail(self, response):
        icon = response.xpath(
            '//span[@class="d3-icon d3-icon-skill d3-icon-skill-64 "]/@style'
        ).extract_first()
        icon = extract_url(icon)

        details = response.xpath('.//div[@class="detail-text"]')
        name = details.xpath('./h1/text()').extract_first()
        stype = details.xpath('./div[1]/text()').extract_first()
        unlock_level = int(details.xpath(
            './/div[@class="fs12"]/p/text()').extract_first().split('：')[1])
        hp = details.xpath(
            './/div[@class="skill-hit"]/p/span/text()').extract_first()
        if hp == '-':
            hit_percent = 0
        else:
            hit_percent = float(hp[:-1]) * 100
        desc = details.xpath('./div[@class="skill-desc"]')

        description = ''.join(desc.xpath('./p[3]//text()').extract()).strip()
        consumes = ''.join(desc.xpath('./p[2]//text()').extract())

        return {
            'name': name,
            'type': stype,
            'description': description + '\n' + consumes,
            'unlock_level': unlock_level,
            'hit_percent': int(hit_percent),
            # 'icon': self.skill['icon'],
            # 'kind': self.skill['kind'],
            # 'job': self.skill['job'],
            # 'ref': self.skill['ref']
        }

    def parse_runes(self, response):
        theads = response.xpath('./thead/tr/th//text()').extract()
        r_runes = response.xpath('./tbody/tr')
        runes = []

        for r in r_runes:
            pc = r.xpath('./td[5]/span/text()').extract_first()
            
            d = {
                'unlock_level':
                r.xpath('./td[1]/span/text()').extract_first(),
                'name':
                r.xpath('./td[2]//div[@class="fuwentext"]/text()').
                extract_first(),
                'icon':
                r.xpath('./td[2]/div/span/span/@class').extract_first(),
                'element':
                r.xpath('./td[3]/span/text()').extract_first(),
                'description':
                ''.join(r.xpath('./td[4]/p//text()').extract()),
                'proc_coefficient':
                int(float(pc[:-1])*100) if pc != '-' else 0,
            }
            runes.append(d)

        return runes
