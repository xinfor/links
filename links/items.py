# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class LinksItem(scrapy.Item):
    """
    电影信息
    """
    name = scrapy.Field()           # 名称
    url = scrapy.Field()            # 链接
    acts = scrapy.Field()           # 演员
    categorys = scrapy.Field()      # 分类
    description = scrapy.Field()    # 描述
    hot = scrapy.Field()            # 人气
    rank = scrapy.Field()           # 评分
    download_url = scrapy.Field()  # 下载链接
    size = scrapy.Field()           # 资源大小
