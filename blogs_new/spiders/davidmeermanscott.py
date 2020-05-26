# -*- coding: utf-8 -*-
import scrapy


class DavidmeermanscottSpider(scrapy.Spider):
    name = "davidmeermanscott"
    start_urls = ["https://www.davidmeermanscott.com/blog"]

    def parse(self, response):
        next_page = response.xpath(
            "//a[@class='next-posts-link']/@href"
        ).extract_first()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)
        for post in response.xpath(
            "//div[contains(@class,'blog--title')]//a/@href"
        ).extract():
            yield scrapy.Request(url=post, callback=self.parse_post)

    def parse_post(self, response):
        yield {
            "Date": response.xpath("//script[contains(text(),'datePublished')]/text()")
            .re_first('"datePublished" : "(.+?)",')
            .split(" ")[0],
            "Site url": self.start_urls[0],
            "Article url": response.url,
            "Author": response.xpath(
                "//a[@class='blog--custom--single-author-link']/text()"
            ).extract_first(),
            "Title": response.xpath("//h1/span/text()").extract_first().strip(),
            "Article body text": " ".join(
                response.xpath(
                    "//span[@id='hs_cos_wrapper_post_body']//*[not(self::script)]/text()"
                ).extract()
            ),
        }
