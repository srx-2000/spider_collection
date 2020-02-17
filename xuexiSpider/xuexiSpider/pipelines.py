# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os
class XuexispiderPipeline(object):

    def process_item(self, item, spider):
        base = os.getcwd()
        file = base + "\学习强国.doc"
        with open(file,'a',encoding='utf-8') as f:
            f.writelines(item["content"])
        return item
