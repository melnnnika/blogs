# -*- coding: utf-8 -*-
import scrapy


class SmallbiztrendsSpider(scrapy.Spider):
    name = "smallbiztrends"
    start_urls = ["https://smallbiztrends.com/category/social-media"]

    def parse(self, response):
        next_page = response.xpath("//a[contains(@class,'next')]/@href").extract_first()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)
        for post in response.xpath(
            "//p[@class='elementor-post__title']/a/@href"
        ).extract():
            yield scrapy.Request(url=post, callback=self.parse_post)

    def parse_post(self, response):
        yield {
            "Date": response.xpath(
                "//span[contains(text(),'Published:')]/span/@datetime"
            )
            .extract_first()
            .split("T")[0],
            "Site url": self.start_urls[0],
            "Article url": response.url,
            "Author": response.xpath(
                "//span[@class='article-author']//span[@class='nickname']//text()"
            ).extract_first(),
            "Title": response.xpath("//h1/text()").extract_first().strip(),
            "Article body text": " ".join(
                response.xpath(
                    "//div[@class='entry-wrap']/*[not(contains(@class,'quads-location')) and not(contains(@class,'content-ad-wrap'))]//text()"
                ).extract()
            ),
        }
