# -*- coding: utf-8 -*-
import scrapy


class AskaaronleeSpider(scrapy.Spider):
    name = "askaaronlee"
    start_urls = ["https://askaaronlee.com/"]

    def parse(self, response):
        for page in response.xpath(
            "//div[contains(@class,'pagination-next')]/a/@href"
        ).extract():
            yield scrapy.Request(url=page, callback=self.parse)
        for post in response.xpath("//a[@class='entry-title-link']/@href").extract():
            yield scrapy.Request(url=post, callback=self.parse_post)

    def parse_post(self, response):
        yield {
            "Date": response.xpath("//time[@class='entry-time']/@datetime")
            .extract_first()
            .split("T")[0],
            "Site url": self.start_urls[0],
            "Article url": response.url,
            "Author": response.xpath(
                "//span[@class='entry-author-name']/text()"
            ).extract_first(),
            "Title": response.xpath("//h1/text()").extract_first(),
            "Article body text": " ".join(
                response.xpath("//div[@class='entry-content']//text()").extract()
            ),
        }
