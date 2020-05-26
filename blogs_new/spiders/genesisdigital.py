# -*- coding: utf-8 -*-
import scrapy


class JvzooSpider(scrapy.Spider):
    name = "genesisdigital"
    start_urls = ["https://www.genesisdigital.co/blog/articles/"]
    custom_settings = {"ROBOTSTXT_OBEY": False}

    def parse(self, response):
        for page in response.xpath(
            "//div[contains(@class,'pagination-next')]/a/@href"
        ).extract():
            yield scrapy.Request(url=response.urljoin(page), callback=self.parse)
        for post in response.xpath("//a[@class='entry-title-link']/@href").extract():
            yield scrapy.Request(url=post, callback=self.parse_post)

    def parse_post(self, response):
        yield {
            "Date": response.xpath(
                "//meta[@property='article:published_time']/@content"
            )
            .extract_first()
            .split("T")[0],
            "Site url": "http://genndi.com",
            "Article url": response.url,
            "Author": "",
            "Title": response.xpath("//h1//text()").extract_first(),
            "Article body text": " ".join(
                response.xpath(
                    "//div[@class='entry-content']/*[not(self::figure) and not(self::div)]//text()"
                ).extract()
            ),
        }
