# -*- coding: utf-8 -*-
import scrapy


class RazorsocialSpider(scrapy.Spider):
    name = "razorsocial"
    start_urls = ["https://www.razorsocial.com/blog/"]
    custom_settings = {"ROBOTSTXT_OBEY": False}

    def parse(self, response):
        for page in response.xpath("//a[@class='nextpostslink']/@href").extract():
            yield scrapy.Request(url=response.urljoin(page), callback=self.parse)
        for post in response.xpath("//h2[@class='bc-custom-header']/a/@href").extract():
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
            "Author": "",
            "Title": response.xpath("//h1[@class='post-title']/text()").extract_first(),
            "Article body text": " ".join(
                response.xpath(
                    "//div[@class='post-content']/*[not(self::iframe) and not(self::div) and not(self::figure) and not(self::noscript) and not(self::img)]//text()"
                ).extract()
            ),
        }
