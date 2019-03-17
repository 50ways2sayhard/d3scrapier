import scrapy
from scrapy import Request
from d3scrapier.spiders import base_url
from d3scrapier.tools.url_tools import extract_url
from d3scrapier.spiders.skill_detail import SkillDetailSpider
import json


class SkillSpider(scrapy.Spider):
    name = "skills"

    def start_requests(self):
        menus = json.load(
            open(
                '/Users/GJT/workspace/d3scrapier/d3scrapier/data/catalogue.json',
                'r'))
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
            # runes = desc[2].xpath('.//a/@name').extract()
            # learn_level = desc[3].xpath('./text()').extract_first()
            skill = {
                'item_type': 'skill',
                "job": job,
                "kind": kind,
                "name": name,
                "ref": ref,
                'icon': icon,
                'type': attr,
                # 'runes': runes,
            }
            yield Request(
                base_url + ref,
                callback=self.parse_detail,
                meta={'skill': skill})
            # yield {
            #     'item_type': 'skill',
            #     "job": job,
            #     "kind": kind,
            #     "name": name,
            #     "ref": ref,
            #     'icon': icon,
            #     'type': attr,
            #     # 'runes': runes,
            #     'description': details['description'],
            #     'unlock_level': learn_level,
            #     'hit_percent': details['hit_percent'],
            #     'runes': details['runes'],
            # }

    def extract_icon(self, response):
        raw_url = response.xpath('.//span/@style').extract_first()
        return extract_url(raw_url)

    def extract_name_ref(self, response):
        name = response.xpath('.//a/@name').extract_first()
        ref = response.xpath('.//a/@href').extract_first()
        return name, ref

    def parse_detail(self, response):
        skill_detail = response.xpath(
            '//div[@class="db-detail-box skill-detail icon-size-default"]')
        runes = response.xpath('//div[@id="cizhui"]//table')
        skill = response.meta['skill']
        details = self.parse_skill_detail(skill_detail)
        runes = self.parse_runes(runes)

        yield {
            'item_type': 'skill',
            'descp': {
                # 'text': self.parse_skill_detail(skill_detail),
                "job": skill['job'],
                "kind": skill['kind'],
                "name": skill['name'],
                "ref": skill['ref'],
                'icon': skill['icon'],
                'type': details['type'],
                # 'runes': runes,
                'description': details['description'],
                'unlock_level': details['unlock_level'],
                'hit_percent': details['hit_percent'],
                #     'runes': details['runes'],
            },
            'runes': runes
        }

    def parse_skill_detail(self, response):
        icon = response.xpath(
            '//span[@class="d3-icon d3-icon-skill d3-icon-skill-64 "]/@style'
        ).extract_first()
        icon = extract_url(icon)

        details = response.xpath('.//div[@class="detail-text"]')
        name = details.xpath('./h1/text()').extract_first()
        stype = details.xpath('./div[1]/text()').extract_first()
        unlock_level = int(
            details.xpath('.//div[@class="fs12"]/p/text()').extract_first().
            split('：')[1])
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
                int(float(pc[:-1]) * 100) if pc != '-' else 0,
            }
            runes.append(d)

        return runes
