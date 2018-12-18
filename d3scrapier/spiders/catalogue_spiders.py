import scrapy


class CatalogueSpider(scrapy.Spider):
    name = 'catalogue'
    start_urls = [
        "http://db.d.163.com/cn/",
    ]

    def parse(self, response):
        res = {}
        menu = response.css('div.m-nav')
        items_lists = menu.css('h3+ul')
        catalogues = menu.css('h3.m-nav-t')

        for i in range(5):
            res[catalogues[i].css('::text').extract_first()] \
                            = self.parse_item(items_lists[i])

        return res

    def parse_item(self, response):
        res = {}
        for item in response.xpath('./li'):
            d = {}
            if item.xpath('./ul') == []:
                res[item.xpath('./a/text()').extract_first().strip()] \
                                = item.xpath('./a/@href').extract_first()
            else:
                for each in item.xpath('./ul/li'):
                    d[each.xpath('./a/text()').extract_first().strip()] \
                                = each.xpath('./a/@href').extract_first()
                res[item.xpath('./a/text()').extract_first()] = d

        return res
