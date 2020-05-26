# -*- coding: utf-8 -*-
import scrapy


class SmartbriefSpider(scrapy.Spider):
    name = "smartbrief"
    start_urls = [
        "https://www.smartbrief.com/industry/marketing-advertising/marketing#.VFfVbYvF-d4"
    ]

    def parse(self, response):
        for page in response.xpath("//li[@class='pager-next']/a/@href").extract():
            yield scrapy.Request(url=response.urljoin(page), callback=self.parse)
        for post in response.xpath(
            "//div[@class='multi-summary-title']//a/@href"
        ).extract():
            yield scrapy.Request(url=post, callback=self.parse_post)

    def parse_post(self, response):
        yield {
            "Date": response.xpath(
                "//meta[@property='article:published_time']/@content"
            )
            .extract_first()
            .split("T")[0],
            "Site url": self.start_urls[0],
            "Article url": response.url,
            "Author": response.xpath("//a[contains(@href,'author')]//text()")
            .extract_first()
            .strip(),
            "Title": response.xpath("//h1/text()").extract_first(),
            "Article body text": " ".join(
                response.xpath(
                    "//div[@class='content_wrapper']//p//text()"
                ).extract()
            ),
        }
