# -*- coding: utf-8 -*-
import scrapy


class SocialmediaexaminerSpider(scrapy.Spider):
    name = "socialmediaexaminer"
    start_urls = ["https://www.socialmediaexaminer.com/"]

    def parse(self, response):
        for page in response.xpath("//li[@class='pagination-next']/a/@href").extract():
            yield scrapy.Request(url=page, callback=self.parse)
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
            "Author": response.xpath("//span[@class='entry-author-name']/text()")
            .extract_first()
            .strip(),
            "Title": response.xpath("//h1/text()").extract_first(),
            "Article body text": " ".join(
                response.xpath(
                    "//div[@class='entry-content']/*[not(self::twitter-widget) and not(self::div)]//text()"
                ).extract()
            ),
        }
