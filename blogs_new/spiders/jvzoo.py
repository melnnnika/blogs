# -*- coding: utf-8 -*-
import scrapy


class JvzooSpider(scrapy.Spider):
    name = "jvzoo"
    start_urls = ["https://blog.jvzoo.com/"]
    custom_settings = {"ROBOTSTXT_OBEY": False}

    def parse(self, response):
        for page in response.xpath("//link[@rel='next']/@href").extract():
            yield scrapy.Request(url=response.urljoin(page), callback=self.parse)
        for post in response.xpath("//h1[@class='op-list-headline']/a/@href").extract():
            yield scrapy.Request(url=post, callback=self.parse_post)

    def parse_post(self, response):
        yield {
            "Date": response.xpath(
                "//meta[@property='article:published_time']/@content"
            )
            .extract_first()
            .split("T")[0],
            "Site url": "https://blog.jvzoo.com/",
            "Article url": response.url,
            "Author": response.xpath(
                "//a[@class='op-list-author']/span[@class='op-upercase']/text()"
            )
            .extract_first()
            .strip(),
            "Title": response.xpath("//h1//text()").extract_first(),
            "Article body text": " ".join(
                response.xpath(
                    "//div[@class='entry-content']/*[not(contains(@class,'cp-module'))]//text()"
                ).extract()
            ),
        }
