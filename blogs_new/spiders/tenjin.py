# -*- coding: utf-8 -*-
import scrapy


class TenjinSpider(scrapy.Spider):
    name = "tenjin"
    start_urls = ["https://blog.tenjin.com/"]
    custom_settings = {"ROBOTSTXT_OBEY": False}

    def parse(self, response):
        for post in response.xpath("//h2[@class='post-title']/a/@href").extract():
            yield scrapy.Request(url=response.urljoin(post), callback=self.parse_post)

    def parse_post(self, response):
        yield {
            "Date": response.xpath(
                "//meta[@property='article:published_time']/@content"
            )
            .extract_first()
            .split("T")[0],
            "Site url": "https://blog.tenjin.com/",
            "Article url": response.url,
            "Author": response.xpath("//div[@class='author']//a/text()")
            .extract_first()
            .strip(),
            "Title": response.xpath("//h1//text()").extract_first(),
            "Article body text": " ".join(
                response.xpath("//section[@class='post-content']//text()").extract()
            ),
        }
