# -*- coding: utf-8 -*-
import scrapy


class PegfitzpatrickSpider(scrapy.Spider):
    name = "pegfitzpatrick"
    start_urls = ["https://pegfitzpatrick.com/blog/"]

    def parse(self, response):
        for page in response.xpath("//li[@class='pagination-next']/a/@href").extract():
            yield scrapy.Request(url=page, callback=self.parse)
        for post in response.xpath("//a[@class='more-link']/@href").extract():
            yield scrapy.Request(url=post, callback=self.parse_post)

    def parse_post(self, response):
        yield {
            "Date": response.xpath(
                "//meta[@property='article:published_time']/@content"
            )
            .extract_first()
            .split("T")[0],
            "Site url": self.start_urls[0],
            "Article url": response.url,
            "Author": "Peg Fitzpatrick",
            "Title": response.xpath(
                "//h1[@class='entry-title']/text()"
            ).extract_first(),
            "Article body text": " ".join(
                response.xpath(
                    "//div[@class='entry-content']/*[not(self::iframe) and not(self::div) and not(self::figure) and not(self::noscript) and not(self::script) and not(self::img)]//text()"
                ).extract()
            ),
        }
