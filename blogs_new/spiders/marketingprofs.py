# -*- coding: utf-8 -*-
import scrapy


class MarketingprofsSpider(scrapy.Spider):
    name = "marketingprofs"
    start_urls = ["https://www.marketingprofs.com/marketing/library/articles/"]

    def parse(self, response):
        for page in response.xpath("//a[contains(@class,'page-link')]/@href").extract():
            yield scrapy.Request(url=page, callback=self.parse)
        for post in response.xpath("//div[@class='article']//a/@href").extract():
            yield scrapy.Request(url=post, callback=self.parse_post)

    def parse_post(self, response):
        yield {
            "Date": response.xpath("//script[contains(text(),'datePublished')]/text()")
            .re_first('"datePublished" : "(.+?)",')
            .split("T")[0],
            "Site url": self.start_urls[0],
            "Article url": response.url,
            "Author": response.xpath(
                "//a[contains(@href,'/authors/')]/text()"
            ).extract_first(),
            "Title": response.xpath("//h1/text()").extract_first(),
            "Article body text": " ".join(
                response.xpath(
                    "//div[@class='entry-inner']/*[not(self::aside)]//text()"
                ).extract()
            ),
        }
