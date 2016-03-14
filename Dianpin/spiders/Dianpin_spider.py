
from scrapy.selector import Selector
from scrapy.spiders import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from Dianpin.items import *
from scrapy.utils.response import open_in_browser

class DianpinSpider(CrawlSpider):
    name = "Dianpin"
    allowed_domains = ['dianping.com']
    start_urls = ["https://www.dianping.com/search/category/8/95/g25147"]

    # can not use 'parse' as callback, because crawspider use it, you can't override it
    rules = [
        Rule(LinkExtractor(allow=('^.*search/category/8/95/g25147.*$')), follow=True, callback='parse_list')
    ]

    def parse_list(self, response):
        self.log('Hi, this is an article page! %s' % response.url)
        shops = response.xpath('//*[@id="shop-all-list"]/ul')
        for shop in shops:
            item = DianpinItem()
            item['star'] = shop.xpath('//*[@id="shop-all-list"]/ul/li[2]/div[2]/div[2]/span/@title').extract()[0].strip()
            item['name'] = shop.xpath('//*[@id="shop-all-list"]/ul/li[1]/div[2]/div[1]/a[1]/@title').extract()[0].strip()
            detail_url = 'https://www.dianping.com' + shop.xpath('//*[@id="shop-all-list"]/ul/li[1]/div[2]/div[1]/a[1]/@href').extract()[0]
            yield scrapy.Request(detail_url, self.parse_shop, meta={'item': item})
            # yield item
            #
            
    def parse_shop(self, response):
        item = response.meta['item']
        item['address'] = response.xpath('//*[@id="basic-info"]/div[2]/span[2]/@title').extract()[0].strip()
        item['phone'] = response.xpath('//*[@id="basic-info"]/p[1]/span[2]/text()').extract()[0].strip()
        return item


