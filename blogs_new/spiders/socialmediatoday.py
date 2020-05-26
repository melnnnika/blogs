# -*- coding: utf-8 -*-
import scrapy


class SocialmediatodaySpider(scrapy.Spider):
    name = "socialmediatoday"
    start_urls = ["https://www.socialmediatoday.com/"]

    def parse(self, response):
        next_page = response.xpath(
            "//a[contains(text(),'Next') or contains(text(),'More stories')]/@href"
        ).extract_first()
        if next_page:
            yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse)
        for post in response.xpath(
            "//h3[contains(@class,'feed__title')]/a/@href"
        ).extract():
            yield scrapy.Request(url=response.urljoin(post), callback=self.parse_post)

    def parse_post(self, response):
        yield {
            "Date": " ".join(
                response.xpath("//div[@class='published-info']/text()").extract()
            ).strip(),
            "Site url": self.start_urls[0],
            "Article url": response.url,
            "Author": response.xpath("//a[@rel='author']/text()").extract_first(),
            "Title": response.xpath("//h1/text()").extract_first(),
            "Article body text": " ".join(
                response.xpath(
                    "//div[contains(@class,'article-body')]/p/text()"
                ).extract()
            ),
        }
