# -*- coding: utf-8 -*-
import scrapy


class AffiliatetipSpider(scrapy.Spider):
    name = "affiliatetip"
    start_urls = ["https://affiliatetip.com/"]

    def parse(self, response):
        next_page = response.xpath(
            "//div[contains(@class,'pagination-next')]/a/@href"
        ).extract_first()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)
        for post in response.xpath("//h2[@class='entry-title']/a/@href").extract():
            yield scrapy.Request(url=post, callback=self.parse_post)

    def parse_post(self, response):
        yield {
            "Date": response.xpath(
                "//time[@class='entry-time']/text()"
            ).extract_first(),
            "Site url": self.start_urls[0],
            "Article url": response.url,
            "Author": response.xpath(
                "//span[@class='entry-author-name']/text()"
            ).extract_first(),
            "Title": response.xpath(
                "//h1[@class='entry-title']/text()"
            ).extract_first(),
            "Article body text": " ".join(
                response.xpath(
                    "//div[@class='entry-content']//*[not(contains(@class, 'sharedaddy')) and not (contains(@class, 'jp-relatedposts'))]//text()"
                ).extract()
            ),
        }
