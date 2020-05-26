# -*- coding: utf-8 -*-
import scrapy


class RebekahradiceSpider(scrapy.Spider):
    name = "rebekahradice"
    start_urls = ["https://rebekahradice.com/blog/"]

    def parse(self, response):
        next_page = response.xpath(
            "//li[@class='pagination-next']/a/@href"
        ).extract_first()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)
        for post in response.xpath("//a[@class='entry-title-link']/@href").extract():
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
            "Author": response.xpath(
                "//span[@class='entry-author-name']/text()"
            ).extract_first(),
            "Title": response.xpath("//h1[@class='entry-title']/text()")
            .extract_first()
            .strip(),
            "Article body text": " ".join(
                response.xpath(
                    "//div[@class='entry-content' or @class='entry-wrap']/*[not(self::script) and not(contains(@class,'share-'))]/text()"
                ).extract()
            ),
        }
