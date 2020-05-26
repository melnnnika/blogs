# -*- coding: utf-8 -*-
import scrapy


class MozSpider(scrapy.Spider):
    name = "moz"
    start_urls = ["https://moz.com/blog/category/social-media"]
    custom_settings = {"ROBOTSTXT_OBEY": False}

    def parse(self, response):
        for page in response.xpath("//a[@class='pager-right']/@href").extract():
            yield scrapy.Request(url=response.urljoin(page), callback=self.parse)
        for post in response.xpath("//h2/a/@href").extract():
            yield scrapy.Request(url=post, callback=self.parse_post)

    def parse_post(self, response):
        yield {
            "Date": response.xpath("//div[@class='media-body']//time/@datetime")
            .extract_first()
            .split(" ")[0],
            "Site url": self.start_urls[0],
            "Article url": response.url,
            "Author": response.xpath(
                "//div[@class='media-body']//a/text()"
            ).extract_first(),
            "Title": response.xpath(
                "//h2[contains(@class,'h2')]/text()"
            ).extract_first(),
            "Article body text": " ".join(
                response.xpath(
                    "//div[@class='post-content']//text()"
                ).extract()
            ),
        }
