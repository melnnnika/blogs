# -*- coding: utf-8 -*-
import scrapy


class MobilemarketingwatchSpider(scrapy.Spider):
    name = "mobilemarketingwatch"
    start_urls = [
        "https://mobilemarketingwatch.com/category/mobile-marketing",
        "https://mobilemarketingwatch.com/category/mobile-advertising",
        "https://mobilemarketingwatch.com/category/casino-mobile-marketing",
        "https://mobilemarketingwatch.com/category/mobile-health-mhealth",
        "https://mobilemarketingwatch.com/category/opinion-2",
        "https://mobilemarketingwatch.com/category/mobile-marketing/platformsoss",
        "https://mobilemarketingwatch.com/category/mobile-marketing/mobile-resources",
        "https://mobilemarketingwatch.com/category/mobile-retail-mobile-topics",
        "https://mobilemarketingwatch.com/category/mobile-marketing/social-media",
    ]
    # custom_settings = {"ROBOTSTXT_OBEY": False}

    def parse(self, response):
        for page in response.xpath("//a[contains(@class,'next')]/@href").extract():
            yield scrapy.Request(url=response.urljoin(page), callback=self.parse)
        for post in response.xpath("//h3/a/@href").extract():
            yield scrapy.Request(url=post, callback=self.parse_post)

    def parse_post(self, response):
        yield {
            "Date": response.xpath(
                "//meta[@property='article:published_time']/@content"
            )
            .extract_first()
            .split("T")[0],
            "Site url": "https://mobilemarketingwatch.com",
            "Article url": response.url,
            "Author": response.xpath("//span[@itemprop='author']//span/text()")
            .extract_first()
            .strip(),
            "Title": response.xpath("//h1/text()").extract_first(),
            "Article body text": " ".join(
                response.xpath("//div[@itemprop='articleBody']//text()").extract()
            ),
        }
