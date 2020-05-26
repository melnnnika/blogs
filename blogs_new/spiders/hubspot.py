# -*- coding: utf-8 -*-
import scrapy
import re
from w3lib.html import remove_tags, remove_tags_with_content


class HubspotSpider(scrapy.Spider):
    name = "hubspot"

    start_urls = ["https://blog.hubspot.com/sitemap.xml"]

    def parse(self, response):
        for post in re.findall("<loc>(.+?)<\/loc>", response.text):
            if "/bid/" in post:
                yield scrapy.Request(url=post, callback=self.parse_post)

    def parse_post(self, response):
        body = ' '.join(response.xpath("//div[@class='hs-migrated-cms-post']").extract())
        date = response.xpath(
            "//p[@class='post-content__publish-date']/text()"
        ).re_first("Originally\s+published\s+(.+?)\s+\d+:\d+")
        if not date:
            date = (
                response.xpath("//p[@class='post-header__publish-date']/@data-postdate")
                .extract_first()
                .split(" ")[0]
            )
        author = response.xpath(
            "//div[@class='post-author-tag__text']//a/text()"
        ).extract_first()
        if not author:
            author = response.xpath(
                "//a[@class='hubspot-author__link']//text()"
            ).extract_first()
        yield {
            "Date": date,
            "Site url": "https://blog.hubspot.com",
            "Article url": response.url,
            "Author": author.strip(),
            "Title": response.xpath("//h1//text()").extract_first(),
            "Article body text": remove_tags(
                remove_tags_with_content(body, ("script",))
            )
        }
