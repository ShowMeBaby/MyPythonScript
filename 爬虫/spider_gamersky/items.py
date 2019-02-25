# -*- coding: utf-8 -*-
import scrapy

class SpiderGamerskyItem(scrapy.Item):
	#标题
    title = scrapy.Field()
    #标题图
    img = scrapy.Field()
    #简要
    content = scrapy.Field()
    #时间
    timte = scrapy.Field()