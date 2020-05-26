# -*- coding: utf-8 -*-
import scrapy


class TheinspirationroomSpider(scrapy.Spider):
    name = "theinspirationroom"
    start_urls = ["https://theinspirationroom.com/daily/"]
    custom_settings = {
        "ROBOTSTXT_OBEY": False,
    }

    def parse(self, response):
        next_page = response.xpath("//div[@class='navright']/a/@href").extract_first()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)
        for post in response.xpath("//h2[@class='title']/a/@href").extract():
            yield scrapy.Request(url=post, callback=self.parse_post)

    def parse_post(self, response):
        yield {
            "Date": response.xpath("//span[@class='date']/text()").extract_first(),
            "Site url": self.start_urls[0],
            "Article url": response.url,
            "Author": response.xpath("//span[@class='author']//text()").extract_first(),
            "Title": response.xpath("//h1/text()").extract_first(),
            "Article body text": " ".join(
                response.xpath("//div[@class='content']/p//text()").extract()
            ),
        }
