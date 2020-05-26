# -*- coding: utf-8 -*-
import scrapy


class MarismithSpider(scrapy.Spider):
    name = "marismith"
    start_urls = ["https://www.marismith.com/mari-smith-blog/"]

    def parse(self, response):
        next_page = response.xpath("//a[contains(@class,'next')]/@href").extract_first()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)
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
            "Author": response.xpath(
                "//span[@class='fl-post-author']//span/text()"
            ).extract_first(),
            "Title": response.xpath("//h1/text()").extract_first().strip(),
            "Article body text": " ".join(
                response.xpath(
                    "//div[contains(@class,'fl-post-content')]/*[not(self::figure) and not(self::pre) and not(@class='wp-about-author-containter-around')]//text()"
                ).extract()
            ),
        }
