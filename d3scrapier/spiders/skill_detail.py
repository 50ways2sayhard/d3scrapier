import scrapy

from d3scrapier.tools.url_tools import extract_url


class SkillDetailSpider(scrapy.Spider):
    name = "SkillDetailSpider"
    start_urls = ['http://db.d.163.com/cn/skill/barbarian/active/bash.html']

    def parse(self, response):
        skill_detail = response.xpath(
            '//div[@class="db-detail-box skill-detail icon-size-default"]')
        runes = response.xpath('//div[@id="cizhui"]//table')

        yield {
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
        unlock_level = details.xpath(
            './/div[@class="fs12"]/p/text()').extract_first()
        hit_percent = details.xpath(
            './/div[@class="skill-hit"]/p/span/text()').extract_first()
        desc = details.xpath('./div[@class="skill-desc"]')

        description = ''.join(desc.xpath('./p[3]//text()').extract()).strip()
        consumes = ''.join(desc.xpath('./p[2]//text()').extract())

        return {
            'name': name,
            'type': stype,
            'description': description,
            'consume': consumes,
            'unlock_level': unlock_level,
            'hit_percent': hit_percent
        }

    def parse_runes(self, response):
        theads = response.xpath('./thead/tr/th//text()').extract()
        r_runes = response.xpath('./tbody/tr')
        runes = []

        for r in r_runes:
            d = {
                'unlock_level': r.xpath('./td[1]/span/text()').extract_first(),
                'rune': {
                    'name':
                    r.xpath('./td[2]//div[@class="fuwentext"]/text()').
                    extract_first(),
                    'icon':
                    r.xpath('./td[2]/div/span/span/@class').extract_first()
                },
                'element': r.xpath('./td[3]/span/text()').extract_first(),
                'description': ''.join(r.xpath('./td[4]/p//text()').extract()),
                'proc_coefficient':
                r.xpath('./td[5]/span/text()').extract_first(),
            }
            runes.append(d)
        
        return runes
