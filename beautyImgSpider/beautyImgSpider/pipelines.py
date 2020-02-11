# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
import logging
from scrapy.pipelines.images import ImagesPipeline
class BeautyimgspiderPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for i in item["image_urls"]:
            yield scrapy.Request(i)
            logging.debug("写入一个")
    def process_item(self, item, spider):
        return item
