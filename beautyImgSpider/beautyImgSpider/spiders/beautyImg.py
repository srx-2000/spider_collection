# -*- coding: utf-8 -*-
import scrapy

from ..items import BeautyimgspiderItem
from scrapy.pipelines.images import ImagesPipeline
import PIL
import logging
class BeautyimgSpider(scrapy.Spider):
    name = 'beautyImg'
    allowed_domains = ['desk.zol.com.cn']
    start_urls = ['http://desk.zol.com.cn/meinv/']

    def parse(self, response):
        list_next_page = response.xpath("//a[@id='pageNext']/@href").extract()
        if list_next_page:
            for i in list_next_page:
                list_next_page_url=response.urljoin(i)
                yield scrapy.Request(list_next_page_url,callback=self.parse)
        img_list=response.xpath("//a[@class='pic']/@href").extract()
        if img_list:
            for i in img_list:
                img_list_url=response.urljoin(i)
                yield scrapy.Request(img_list_url,callback=self.img_parse)
    def img_parse(self,response):
        img_next_page=response.xpath("//a[@id='pageNext']/@href").extract()
        if img_next_page:
            for i in img_next_page:
                img_next_page_url=response.urljoin(i)
                yield scrapy.Request(img_next_page_url,callback=self.img_parse)
        img_url= response.xpath("//img[@id='bigImg']/@src").extract()
        img_name=response.xpath("//a[@id='titleName']/text()").extract()
        item=BeautyimgspiderItem()
        item["image_urls"]=img_url
        item["name"]=img_name
        yield item
        # for i in item['name']:
        logging.debug("使用一次")