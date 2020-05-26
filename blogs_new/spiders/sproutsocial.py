# -*- coding: utf-8 -*-
import scrapy


class SproutsocialSpider(scrapy.Spider):
    name = "sproutsocial"
    start_urls = ["https://sproutsocial.com/insights/"]
    custom_settings = {"ROBOTSTXT_OBEY": False}

    def parse(self, response):
        for page in response.xpath("//a[@rel='next']/@href").extract():
            yield scrapy.Request(url=response.urljoin(page), callback=self.parse)
        for post in response.xpath("//h2/a/@href").extract():
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
            "Author": " ".join(
                response.xpath(
                    "//a[@class='AuthorAttribution-name']/span/text()"
                ).extract()
            ).strip(),
            "Title": response.xpath("//h1/text()").extract_first(),
            "Article body text": " ".join(
                response.xpath("//div[@class='Post-content']//text()").extract()
            ),
        }
