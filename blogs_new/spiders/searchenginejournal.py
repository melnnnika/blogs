# -*- coding: utf-8 -*-
import scrapy
import re


class SearchenginejournalSpider(scrapy.Spider):
    name = "searchenginejournal"

    def start_requests(self):
        for i in range(1, 21):
            yield scrapy.Request(
                url="https://www.searchenginejournal.com/post-sitemap%s.xml" % i,
                callback=self.parse_page,
            )

    def parse_page(self, response):
        for post in re.findall("<loc>(.+?)<\/loc>", response.text):
            yield scrapy.Request(url=post, callback=self.parse_post)

    def parse_post(self, response):
        yield {
            "Date": response.xpath(
                "//script[contains(text(),'datePublished')]/text()"
            )
            .re_first('"datePublished": "(.+?)",')
            .split("T")[0],
            "Site url": "https://www.searchenginejournal.com/",
            "Article url": response.url,
            "Author": response.xpath("//a[@class='post-author']/text()")
            .extract_first()
            .strip(),
            "Title": response.xpath(
                "//h1/text()"
            ).extract_first(),
            "Article body text": " ".join(
                response.xpath(
                    "//section[contains(@class,'sec-art')]//text()"
                ).extract()
            ),
        }
