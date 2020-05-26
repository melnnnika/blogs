# -*- coding: utf-8 -*-
import scrapy
import w3lib


class ProbloggerSpider(scrapy.Spider):
    name = "problogger"
    start_urls = ["https://problogger.com/blog/"]
    custom_settings = {"ROBOTSTXT_OBEY": False}

    def parse(self, response):
        for page in response.xpath("//link[@rel='next']/@href").extract():
            yield scrapy.Request(url=response.urljoin(page), callback=self.parse)
        for post in response.xpath("//h2/a/@href").extract():
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
                "//span[@class='author']/a/text()"
            ).extract_first(),
            "Title": response.xpath("//h1[@class='title']/text()").extract_first(),
            "Article body text": w3lib.html.remove_tags(
                " ".join(response.xpath("//div[@class='post-content']").extract())
            ),
        }
