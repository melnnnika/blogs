# -*- coding: utf-8 -*-
import scrapy
import re


class BrandchannelSpider(scrapy.Spider):
    name = "brandchannel"

    def start_requests(self):
        for i in range(1, 23):
            yield scrapy.Request(
                url="https://www.brandchannel.com/post-sitemap%s.xml" % i,
                callback=self.parse_page,
            )

    def parse_page(self, response):
        for post in re.findall("<loc>(.+?)<\/loc>", response.text):
            yield scrapy.Request(url=post, callback=self.parse_post)

    def parse_post(self, response):
        yield {
            "Date": response.xpath(
                "//meta[@property='article:published_time']/@content"
            )
            .extract_first()
            .split("T")[0],
            "Site url": "https://www.brandchannel.com",
            "Article url": response.url,
            "Author": response.xpath("//span[contains(@class,'author')]/a/text()")
            .extract_first()
            .strip(),
            "Title": response.xpath(
                "//h1[@class='entry-title']/text()"
            ).extract_first(),
            "Article body text": " ".join(
                response.xpath(
                    "//div[@class='entry-content']/*[not(contains(@class,'addtoany_share_save_container'))]//text()"
                ).extract()
            ),
        }
