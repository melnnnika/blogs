# -*- coding: utf-8 -*-
import scrapy


class AlexaSpider(scrapy.Spider):
    name = "alexa"
    start_urls = ["https://blog.alexa.com/all-posts/"]
    custom_settings = {"ROBOTSTXT_OBEY": False}

    def parse(self, response):
        for page in response.xpath("//a[@class='pagination-next']//@href").extract():
            yield scrapy.Request(url=response.urljoin(page), callback=self.parse)
        for post in response.xpath("//h2/a/@href").extract():
            yield scrapy.Request(url=response.urljoin(post), callback=self.parse_post)

    def parse_post(self, response):
        yield {
            "Date": response.xpath(
                "//meta[@property='article:published_time']/@content"
            )
            .extract_first()
            .split("T")[0],
            "Site url": "https://blog.alexa.com",
            "Article url": response.url,
            "Author": response.xpath(
                "//script[contains(text(),'pagePostAuthor')]/text()"
            ).re_first('pagePostAuthor":"(.+?)"'),
            "Title": response.xpath("//h1[@class='fusion-post-title']/text()")
            .extract_first()
            .strip(),
            "Article body text": " ".join(
                response.xpath("//div[contains(@class,'post-content')]/*[not(@class='rt-reading-time') and not(@class='awac-wrapper')]//text()").extract()
            ),
        }
