# -*- coding: utf-8 -*-
import scrapy


class SocpublicSpider(scrapy.Spider):
    name = "socpublic"
    start_urls = ["http://socpublic.com/account/news.html"]
    custom_settings = {"ROBOTSTXT_OBEY": False}

    def parse(self, response):
        for page in response.xpath("//ul[@class='pagination']//a/@href").extract():
            yield scrapy.Request(url=response.urljoin(page), callback=self.parse)
        for post in response.xpath("//a[@class='title']/@href").extract():
            yield scrapy.Request(url=post, callback=self.parse_post)

    def parse_post(self, response):
        yield {
            "Date": response.xpath(
                "//i[contains(@class,'fa-calendar')]//following-sibling::text()"
            ).re_first("(\d+\.\d+\.\d+\.?)"),
            "Site url": "http://socpublic.com",
            "Article url": response.url,
            "Author": "",
            "Title": response.xpath("//h1//text()").extract_first(),
            "Article body text": " ".join(
                response.xpath("//h1//following-sibling::div[1]//text()").extract()
            ),
        }
