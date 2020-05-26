# -*- coding: utf-8 -*-
import scrapy


class SamcartSpider(scrapy.Spider):
    name = "samcart"
    start_urls = ["https://www.samcart.com/blog"]

    def parse(self, response):
        for page in response.xpath("//link[@rel='next']/@href").extract():
            yield scrapy.Request(url=page, callback=self.parse)
        for post in response.xpath("//article/a/@href").extract():
            yield scrapy.Request(url=post, callback=self.parse_post)

    def parse_post(self, response):
        yield {
            "Date": response.xpath("//meta[@property='article:published_time']/@content")
            .extract_first()
            .split("T")[0],
            "Site url": self.start_urls[0],
            "Article url": response.url,
            "Author": response.xpath("//script[contains(text(),'Person')]//text()")
            .re('"name":"(.+?)"')[-1]
            .strip(),
            "Title": response.xpath("//h1/text()").extract_first(),
            "Article body text": " ".join(
                response.xpath(
                    "//div[contains(@class,'article__body')]/*[not(contains(@class,'swp_social_panel')) and not(contains(@class,'post__tags'))]//text()"
                ).extract()
            ),
        }
