# -*- coding: utf-8 -*-
import scrapy
import re


class LivechatSpider(scrapy.Spider):
    name = "livechat"
    start_urls = ["https://www.livechat.com/post-sitemap.xml"]
    custom_settings = {"ROBOTSTXT_OBEY": False}

    def parse(self, response):
        for post in re.findall("<loc>(.+?)<\/loc>", response.text):
            if '/blog/' in post:
                yield scrapy.Request(url=post, callback=self.parse_post)

    def parse_post(self, response):
        yield {
            "Date": response.xpath(
                "//img[contains(@src,'calendar')]/following-sibling::span/text()"
            )
            .extract_first()
            .split("T")[0],
            "Site url": self.start_urls[0],
            "Article url": response.url,
            "Author": response.xpath("//span[@class='u-text-p8']/text()")
            .extract_first()
            .strip(),
            "Title": response.xpath("//h1/text()").extract_first(),
            "Article body text": " ".join(
                response.xpath(
                    "//div[@class='post-header']//following-sibling::*//text()"
                ).extract()
            ),
        }
