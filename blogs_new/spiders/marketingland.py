# -*- coding: utf-8 -*-
import scrapy


class MarketinglandSpider(scrapy.Spider):
    name = "marketingland"
    start_urls = ["http://marketingland.com/"]

    def parse(self, response):
        for page in response.xpath("//link[@rel='next']/@href").extract():
            yield scrapy.Request(url=response.urljoin(page), callback=self.parse)
        for post in response.xpath("//h2[@class='headline']/a/@href").extract():
            yield scrapy.Request(url=post, callback=self.parse_post)

    def parse_post(self, response):
        yield {
            "Date": "".join(
                response.xpath("//div[contains(@class,'dateline')]/text()").extract()
            )
            .split(" on ")[-1]
            .split(" at ")[0],
            "Site url": self.start_urls[0],
            "Article url": response.url,
            "Author": response.xpath("//a[contains(@href,'/author/')]/text()")
            .extract_first()
            .strip(),
            "Title": response.xpath("//h1/text()").extract_first(),
            "Article body text": " ".join(
                response.xpath("//div[@class='body-content']/p//text()").extract()
            ),
        }
