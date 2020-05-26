# -*- coding: utf-8 -*-
import scrapy
from w3lib.html import remove_tags, remove_tags_with_content


class ZdnetSpider(scrapy.Spider):
    name = "zdnet"
    start_urls = ["https://www.zdnet.com/blog/feeds/?tag=mantle_skin;content"]
    # custom_settings = {"ROBOTSTXT_OBEY": False}

    def parse(self, response):
        for page in response.xpath("//a[@class='next']/@href").extract():
            yield scrapy.Request(url=response.urljoin(page), callback=self.parse)
        for post in response.xpath("//h3/a/@href").extract():
            yield scrapy.Request(url=response.urljoin(post), callback=self.parse_post)

    def parse_post(self, response):
        body = " ".join(response.xpath("//div[@class='storyBody']").extract())
        yield {
            "Date": response.xpath("//time/@datetime")
            .extract_first()
            .split(" ")[0],
            "Site url": self.start_urls[0],
            "Article url": response.url,
            "Author": response.xpath(
                "//a[@rel='author']/span/text()"
            ).extract_first(),
            "Title": response.xpath("//h1//text()").extract_first(),
            "Article body text": remove_tags(
                remove_tags_with_content(body, ("script", "div", "section"))
            ),
        }
