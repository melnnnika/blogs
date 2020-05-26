# -*- coding: utf-8 -*-
import scrapy


class ConvinceandconvertSpider(scrapy.Spider):
    name = "convinceandconvert"
    start_urls = ["https://www.convinceandconvert.com/category/social-media-marketing/"]

    def parse(self, response):
        for page in response.xpath("//a[@class='nextpostslink']/@href").extract():
            yield scrapy.Request(url=page, callback=self.parse)
        for post in response.xpath("//h4[@class='heading']/a/@href").extract():
            yield scrapy.Request(url=post, callback=self.parse_post)

    def parse_post(self, response):
        yield {
            "Date": response.xpath("//script[contains(text(),'datePublished')]/text()")
            .re_first('"datePublished":"(.+?)"')
            .split("T")[0],
            "Site url": self.start_urls[0],
            "Article url": response.url,
            "Author": response.xpath("//a[@class='toggleprofile']/text()")
            .extract_first()
            .strip(),
            "Title": response.xpath("//h1//text()").extract_first(),
            "Article body text": " ".join(
                response.xpath(
                    "//div[@class='entry-content']/*[not(self::iframe) and not(self::noscript) and not(self::div)]//text()"
                ).extract()
            ),
        }
