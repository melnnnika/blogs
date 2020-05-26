# -*- coding: utf-8 -*-
import scrapy


class DreamgrowSpider(scrapy.Spider):
    name = "dreamgrow"
    start_urls = ["https://www.dreamgrow.com/"]

    def parse(self, response):
        next_page = response.xpath("//a[@class='nextpostslink']/@href").extract_first()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)
        for post in response.xpath("//h2/a/@href").extract():
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
            "Author": response.xpath("//a[@rel='author']/text()").extract_first(),
            "Title": response.xpath("//h1/text()").extract_first(),
            "Article body text": " ".join(
                response.xpath(
                    "//div[@class='entry-inner']/*[not(self::aside)]//text()"
                ).extract()
            ),
        }
