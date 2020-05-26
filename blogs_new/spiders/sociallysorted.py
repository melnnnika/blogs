# -*- coding: utf-8 -*-
import scrapy


class SociallysortedSpider(scrapy.Spider):
    name = "sociallysorted"
    start_urls = ["https://sociallysorted.com.au/blog/"]
    custom_settings = {"ROBOTSTXT_OBEY": False}

    def parse(self, response):
        for page in response.xpath("//a[@class='nextpostslink']/@href").extract():
            yield scrapy.Request(url=response.urljoin(page), callback=self.parse)
        for post in response.xpath("//h4[@class='entry-title']/a/@href").extract():
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
                "//div[@class='ts-fab-header']//h4/a/text()"
            ).extract_first(),
            "Title": response.xpath(
                "//div[@class='et_pb_text_inner']/h1//text()"
            ).extract_first(),
            "Article body text": " ".join(
                response.xpath(
                    "//div[contains(@class,'post_content')]/*[not(self::iframe) and not(self::div) and not(self::figure) and not(self::noscript) and not(self::img)]//text()"
                ).extract()
            ),
        }
