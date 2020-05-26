# -*- coding: utf-8 -*-
import scrapy


class MarketingovercoffeeSpider(scrapy.Spider):
    name = "marketingovercoffee"
    start_urls = ["https://www.marketingovercoffee.com/"]

    def parse(self, response):
        for page in response.xpath("//div[@class='alignleft']/a/@href").extract():
            yield scrapy.Request(url=response.urljoin(page), callback=self.parse)
        for post in response.xpath("//h2[@class='entry-title']/a/@href").extract():
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
            "Author": response.xpath("//a[@rel='author']/text()")
            .extract_first()
            .strip(),
            "Title": response.xpath("//h1/text()").extract_first(),
            "Article body text": " ".join(
                response.xpath(
                    "//div[@class='entry-content']//*[not(self::script)]/text()"
                ).extract()
            ),
        }
