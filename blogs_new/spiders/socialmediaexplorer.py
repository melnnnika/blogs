# -*- coding: utf-8 -*-
import scrapy
import re


class SocialmediaexplorerSpider(scrapy.Spider):
    name = "socialmediaexplorer"
    start_urls = [
        "https://socialmediaexplorer.com/post-sitemap1.xml",
        "https://socialmediaexplorer.com/post-sitemap2.xml",
        "https://socialmediaexplorer.com/post-sitemap3.xml",
        "https://socialmediaexplorer.com/post-sitemap4.xml",
        "https://socialmediaexplorer.com/post-sitemap5.xml",
    ]
    # custom_settings = {"ROBOTSTXT_OBEY": False}

    def parse(self, response):
        # print(response.xpath("//loc/text()").extract())
        for post in re.findall("<loc>(.+?)<\/loc>", response.text):
            yield scrapy.Request(url=post, callback=self.parse_post)

    def parse_post(self, response):
        yield {
            "Date": response.xpath(
                "//meta[@property='article:published_time']/@content"
            )
            .extract_first()
            .split("T")[0],
            "Site url": "https://socialmediaexplorer.com",
            "Article url": response.url,
            "Author": response.xpath("//a[@rel='author']//text()")
            .extract_first()
            .strip(),
            "Title": response.xpath(
                "//div[@class='post-thumb-title']//text()"
            ).extract_first(),
            "Article body text": " ".join(
                response.xpath(
                    "//div[@class='credits']/following-sibling::*[not(@class='sfsi_Sicons') and not(contains(@class,'quads-location'))]//text()"
                ).extract()
            ),
        }
