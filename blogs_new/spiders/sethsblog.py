# -*- coding: utf-8 -*-
import scrapy


class SethsblogSpider(scrapy.Spider):
    name = "sethsblog"
    start_urls = ["https://seths.blog/"]

    def parse(self, response):
        posts = response.xpath("//h2/a/@href").extract()
        if posts:
            if "/page/" not in response.url:
                next_page = "https://seths.blog/page/2/"
            else:
                prev_page = response.url.split("/page/")[-1]
                next_page = "https://seths.blog/page/%s" % (
                    int(prev_page.strip("/")) + 1
                )
            yield scrapy.Request(url=next_page, callback=self.parse)
        for post in posts:
            yield scrapy.Request(url=post, callback=self.parse_post)

    def parse_post(self, response):
        yield {
            "Date": response.xpath(
                "//div[contains(@class,'post')]//span[@class='date']/text()"
            ).extract_first(),
            "Site url": self.start_urls[0],
            "Article url": response.url,
            "Author": "Seth Godin",
            "Title": response.xpath("//h2/a//text()").extract_first(),
            "Article body text": " ".join(
                response.xpath(
                    "//div[contains(@class,'post')]//div[@class='has-content-area']//text()"
                ).extract()
            ),
        }
