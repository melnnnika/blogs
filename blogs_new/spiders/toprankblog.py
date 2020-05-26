# -*- coding: utf-8 -*-
import scrapy


class ToprankblogSpider(scrapy.Spider):
    name = "toprankblog"
    start_urls = ["http://www.toprankblog.com/"]

    def parse(self, response):
        next_page = response.xpath(
            "//li[@class='pagination-next']/a/@href"
        ).extract_first()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)
        for post in response.xpath("//a[@class='entry-title-link']/@href").extract():
            yield scrapy.Request(url=post, callback=self.parse_post)

    def parse_post(self, response):
        author_date = response.xpath(
            "//div[@class='alt-meta']//small/text()"
        ).extract_first()
        yield {
            "Date": author_date.split(" on\n")[-1],
            "Site url": self.start_urls[0],
            "Article url": response.url,
            "Author": response.xpath(
                "//div[@id='author-info']//img/@alt"
            ).extract_first(),
            "Title": response.xpath(
                "//h1[@class='entry-title']/text()"
            ).extract_first(),
            "Article body text": " ".join(
                response.xpath("//div[@class='entry-content']//text()").extract()
            ),
        }
