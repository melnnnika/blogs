# -*- coding: utf-8 -*-
import scrapy


class MainSpider(scrapy.Spider):
    name = "blogs_spider"
    start_urls = [
        "http://www.hubspot.com/"
        "http://sethgodin.typepad.com/"
        "http://www.toprankblog.com/"
        "http://www.conversationagent.com/"
        "http://www.adverblog.com/"
        "http://www.twistimage.com/blog/"
        "http://darmano.typepad.com/"
        "http://thefuturebuzz.com/"
        "http://www.mobilemarketingwatch.com/"
        "http://theinspirationroom.com/daily/"
    ]

    def parse(self, response):
        pass
