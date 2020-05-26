# -*- coding: utf-8 -*-
import scrapy


class MarketoSpider(scrapy.Spider):
    name = "marketo"
    start_urls = ["https://blog.marketo.com/"]

    def parse(self, response):
        for page in response.xpath("//link[@rel='next']/@href").extract():
            yield scrapy.Request(url=response.urljoin(page), callback=self.parse)
        for post in response.xpath(
            "//a[@class='blog-post-preview' or @class='blog-main__featured-post']/@href"
        ).extract():
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
            "Author": " ".join(
                response.xpath("//a[@rel='author']//text()").extract()
            ).strip(),
            "Title": response.xpath("//h1//text()").extract_first(),
            "Article body text": " ".join(
                response.xpath(
                    "//div[@class='blog-post-page__content__text']//text()"
                ).extract()
            ),
        }
