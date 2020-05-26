# -*- coding: utf-8 -*-
import scrapy
from w3lib.html import remove_tags, remove_tags_with_content


class StarClicksSpider(scrapy.Spider):
    name = "star-clicks"
    start_urls = ["https://blog.star-clicks.com/"]
    custom_settings = {"ROBOTSTXT_OBEY": False}

    def parse(self, response):
        for post in response.xpath("//h2[@class='entry-title']//a/@href").extract():
            yield scrapy.Request(url=post, callback=self.parse_post)

    def parse_post(self, response):
        body = " ".join(response.xpath("//div[@class='entry-content']").extract())
        yield {
            "Date": response.xpath(
                "//meta[@property='article:published_time']/@content"
            )
            .extract_first()
            .split("T")[0],
            "Site url": self.start_urls[0],
            "Article url": response.url,
            "Author": response.xpath(
                "//span[contains(@class,'author')]/a/text()"
            ).extract_first(),
            "Title": response.xpath("//h1//text()").extract_first(),
            "Article body text": remove_tags(
                remove_tags_with_content(body, ("script", "figure"))
            ),
        }
