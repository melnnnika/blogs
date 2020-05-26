# -*- coding: utf-8 -*-
import scrapy


class WebStrategistSpider(scrapy.Spider):
    name = "web-strategist"
    start_urls = ["http://web-strategist.com/blog/"]
    custom_settings = {"ROBOTSTXT_OBEY": False}

    def parse(self, response):
        for page in response.xpath("//div[@class='nav-previous']/a/@href").extract():
            yield scrapy.Request(url=response.urljoin(page), callback=self.parse)
        for post in response.xpath("//h2[@class='entry-title']/a/@href").extract():
            yield scrapy.Request(url=post, callback=self.parse_post)

    def parse_post(self, response):
        yield {
            "Date": response.xpath("//time[contains(@class,'entry-date')]/@datetime")
            .extract_first()
            .split("T")[0],
            "Site url": self.start_urls[0],
            "Article url": response.url,
            "Author": "Jeremiah Owyang",
            "Title": response.xpath(
                "//h1[@class='entry-title']/text()"
            ).extract_first(),
            "Article body text": " ".join(
                response.xpath(
                    "//div[@class='entry-content']/*[not(self::figure) and not(self::script)]//text()"
                ).extract()
            ),
        }
