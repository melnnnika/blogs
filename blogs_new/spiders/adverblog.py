# -*- coding: utf-8 -*-
import scrapy


class AdverblogSpider(scrapy.Spider):
    name = "adverblog"
    pages = 556

    def start_requests(self):
        yield scrapy.Request(url="http://www.adverblog.com/", callback=self.parse_page)
        for page in range(1, self.pages + 1):
            yield scrapy.Request(
                url="http://www.adverblog.com/page/%s/" % page, callback=self.parse_page
            )

    def parse_page(self, response):
        for post in response.xpath("//div[@class='article']//h2/a/@href").extract():
            yield scrapy.Request(url=response.urljoin(post), callback=self.parse_post)

    def parse_post(self, response):
        date_string = response.xpath("//div[@class='sub-meta']/text()").extract_first()
        yield {
            "Date": date_string.split(" at ")[0],
            "Site url": "http://www.adverblog.com/",
            "Article url": response.url,
            "Author": response.xpath(
                "//a[contains(@href,'/author/')]/text()"
            ).extract_first(),
            "Title": response.xpath("//h1/text()").extract_first(),
            "Article body text": " ".join(
                response.xpath("//div[contains(@class,'article')]//p/text()").extract()
            ),
        }
