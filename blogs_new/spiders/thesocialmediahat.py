# -*- coding: utf-8 -*-
import scrapy


class ThesocialmediahatSpider(scrapy.Spider):
    name = "thesocialmediahat"
    start_urls = [
        "https://www.thesocialmediahat.com/blog/category/social-media/",
        "https://www.thesocialmediahat.com/blog/category/social-media-tools/",
        "https://www.thesocialmediahat.com/blog/category/digital-marketing/",
    ]
    custom_settings = {"ROBOTSTXT_OBEY": False}

    def parse(self, response):
        for page in response.xpath("//li[@class='pagination-next']/a/@href").extract():
            yield scrapy.Request(url=response.urljoin(page), callback=self.parse)
        for post in response.xpath("//a[@class='entry-title-link']/@href").extract():
            yield scrapy.Request(url=post, callback=self.parse_post)

    def parse_post(self, response):
        yield {
            "Date": response.xpath(
                "//meta[@property='article:published_time']/@content"
            )
            .extract_first()
            .split("T")[0],
            "Site url": "https://www.thesocialmediahat.com",
            "Article url": response.url,
            "Author": response.xpath(
                "//span[@class='entry-author-name']/text()"
            ).extract_first(),
            "Title": response.xpath("//h1//text()").extract_first(),
            "Article body text": " ".join(
                response.xpath(
                    "//div[@class='entry-content']/*[not(contains(@class,'swp_social_panel')) and not(self::figure)]//text()"
                ).extract()
            ),
        }
