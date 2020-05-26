# -*- coding: utf-8 -*-
import scrapy
import re
from w3lib.html import remove_tags, remove_tags_with_content


class SocialmediaSpider(scrapy.Spider):
    name = "socialmedia"

    start_urls = ["https://www.socialmedia.biz/post-sitemap.xml"]

    def parse(self, response):
        for post in re.findall("<loc>(.+?)<\/loc>", response.text):
            yield scrapy.Request(url=post, callback=self.parse_post)

    def parse_post(self, response):
        yield {
            "Date": response.xpath(
                "//meta[@property='article:published_time']/@content"
            )
            .extract_first()
            .split("T")[0],
            "Site url": "https://www.socialmedia.biz",
            "Article url": response.url,
            "Author": response.xpath(
                "//span[contains(@class,'author')]//text()"
            ).extract_first(),
            "Title": response.xpath("//h1//text()").extract_first(),
            "Article body text": " ".join(
                response.xpath(
                    "//div[@class='entry-content']/*[not(contains(@class,'swp_social_panel')) and not(self::figure)]//text()"
                ).extract()
            ),
        }
