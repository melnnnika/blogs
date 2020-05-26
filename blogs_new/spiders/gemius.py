# -*- coding: utf-8 -*-
import scrapy


class GemiusSpider(scrapy.Spider):
    name = "gemius"
    start_urls = [
        "https://www.gemius.com/all.html?keywords=&more=1&FORM_SUBMIT=hiddenField&REQUEST_TOKEN=8eeae4de85a087e79a2cca47560cf55e",
        "https://www.gemius.com/all.html?keywords=&more=2&FORM_SUBMIT=hiddenField&REQUEST_TOKEN=8eeae4de85a087e79a2cca47560cf55e",
    ]

    def start_requests(self):
        # for page in response.xpath("//a[@class='page-numbers']/@href").extract():
        #     yield scrapy.Request(url=page, callback=self.parse)
        # for post in response.xpath(
        #     "//div[contains(@class,'mod_newslist')]//a/@href"
        # ).extract():
        #     yield scrapy.Request(url=response.urljoin(post), callback=self.parse_page)
        for page in self.start_urls:
            yield scrapy.Request(url=page, callback=self.parse_page, dont_filter=True)

    def parse_page(self, response):
        print(response.text)
        # for post in response.xpath(
        #     "//div[contains(@class,'mod_newslist')]//a/@href"
        # ).extract():
        #     print(post)
            # yield scrapy.Request(url=response.urljoin(post), callback=self.parse_post)

    def parse_post(self, response):
        yield {
            "Date": response.xpath(
                "//div[contains(@class,'sectionTitle')]//span[@class='tag']/text()"
            )
            .extract_first()
            .split(" ")[0],
            "Site url": self.start_urls[0],
            "Article url": response.url,
            "Author": "",
            "Title": response.xpath("//article//h1/text()").extract_first(),
            "Article body text": " ".join(
                response.xpath(
                    "//div[contains(@class,'artWrapper') or @class='infoBox']//text()"
                ).extract()
            ),
        }
