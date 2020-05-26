# -*- coding: utf-8 -*-
import scrapy


class RdstationSpider(scrapy.Spider):
    name = "rdstation"
    start_urls = ["https://blog.rdstation.com.br/"]

    def parse(self, response):
        for page in response.xpath("//a[@class='nextpostslink']/@href").extract():
            yield scrapy.Request(url=page, callback=self.parse)
        for post in response.xpath("//ul[@class='post-list']//li/a/@href").extract():
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
                "//div[@itemprop='author']//span[@itemprop='name']//text()"
            ).extract_first(),
            "Title": response.xpath(
                "//h1[@itemprop='headline']/text()"
            ).extract_first(),
            "Article body text": " ".join(
                response.xpath(
                    "//main[@itemprop='articleBody']/*[not(@class='post-categories') and not (@class='categories-list')]//text()"
                ).extract()
            ),
        }
