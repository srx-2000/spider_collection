# -*- coding: utf-8 -*-
import scrapy

from ..items import XuexispiderItem


class XuexiSpider(scrapy.Spider):
    name = 'xuexi'
    allowed_domains = ['hack520.com']
    start_urls = ['https://www.hack520.com/666.html']

    def parse(self, response):
        content=response.xpath("//div[@class='post_content']/p/text()").extract()
        item=XuexispiderItem()
        item['content']=content
        yield item