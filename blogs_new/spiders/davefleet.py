# -*- coding: utf-8 -*-
import scrapy


class AskaaronleeSpider(scrapy.Spider):
    name = "davefleet"
    start_urls = ["https://davefleet.com/"]

    def parse(self, response):
        for page in response.xpath("//a[@class='page-numbers']/@href").extract():
            yield scrapy.Request(url=page, callback=self.parse)
        for post in response.xpath("//h2[@class='postitle']/a/@href").extract():
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
            "Author": response.xpath("//a[contains(@class,'post-author')]//text()")
            .extract_first()
            .strip(),
            "Title": response.xpath("//h1/text()").extract_first(),
            "Article body text": " ".join(
                response.xpath(
                    "//div[@class='thn_post_wrap']/*[not(contains(@class,'sharedaddy'))]//text()"
                ).extract()
            ),
        }
