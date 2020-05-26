# -*- coding: utf-8 -*-
import scrapy


class DucttapemarketingSpider(scrapy.Spider):
    name = "ducttapemarketing"
    start_urls = ["https://ducttapemarketing.com/blog/"]

    def parse(self, response):
        next_page = response.xpath("//a[@class='nxt-btn']/@href").extract_first()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)
        for post in response.xpath(
            "//span[contains(@class,'tve-post-grid-title')]/a/@href"
        ).extract():
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
            "Author": response.xpath("//p[@class='author']/text()")
            .extract_first()
            .replace("By", "")
            .strip(),
            "Title": response.xpath("//h1/text()").extract_first().strip(),
            "Article body text": " ".join(
                response.xpath(
                    "//div[@id='content']//p/text() | //div[@id='content']//h2/text() | //div[@id='content']//h3/text()"
                ).extract()
            ),
        }
