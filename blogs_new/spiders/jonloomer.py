# -*- coding: utf-8 -*-
import scrapy


class JonloomerSpider(scrapy.Spider):
    name = "jonloomer"
    start_urls = ["https://www.jonloomer.com/blog/"]
    # custom_settings = {"ROBOTSTXT_OBEY": False}

    def parse(self, response):
        for page in response.xpath("//a[contains(@class,'next')]/@href").extract():
            yield scrapy.Request(url=response.urljoin(page), callback=self.parse)
        for post in response.xpath("//h1/a/@href").extract():
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
            "Author": response.xpath("//span[@itemprop='author']//text()").extract_first(),
            "Title": response.xpath("//h1//text()").extract_first(),
            "Article body text": " ".join(
                response.xpath(
                    "//section[@itemprop='articleBody']/*[not(self::aside) and not(self::iframe)]//text()"
                ).extract()
            ),
        }
