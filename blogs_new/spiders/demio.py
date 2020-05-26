# -*- coding: utf-8 -*-
import scrapy
import w3lib.html


class DemioSpider(scrapy.Spider):
    name = "demio"
    start_urls = ["https://learn.demio.com/blog/"]

    def parse(self, response):
        for page in response.xpath("//link[@rel='next']/@href").extract():
            yield scrapy.Request(url=page, callback=self.parse)
        for post in response.xpath("//article/a/@href").extract():
            yield scrapy.Request(url=post, callback=self.parse_post)

    def parse_post(self, response):
        yield {
            "Date": response.xpath("//script[contains(text(),'datePublished')]//text()")
            .re_first('"datePublished":"(.+?)"')
            .split("T")[0],
            "Site url": self.start_urls[0],
            "Article url": response.url,
            "Author": response.xpath(
                "//div[@class='blog-post-meta__author']//img/@alt"
            ).extract_first(),
            "Title": response.xpath(
                "//div[@class='post-title']/text()"
            ).extract_first(),
            "Article body text": w3lib.html.remove_tags(
                " ".join(
                    response.xpath(
                        "//div[contains(@class,'post-body')] | //div[contains(@class,'dss-notes')]"
                    ).extract()
                )
            ),
            # "Article body text": " ".join(
            #     response.xpath(
            #         "//div[contains(@class,'dss-head')]/*[not(contains(@class,'tve-leads-shortcode'))]//text()"
            #     ).extract()
            # ),
        }
