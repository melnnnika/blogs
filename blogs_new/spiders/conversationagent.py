# -*- coding: utf-8 -*-
import scrapy
import re


class ConversationagentSpider(scrapy.Spider):
    name = "conversationagent"
    start_urls = ["https://www.conversationagent.com/"]

    def parse(self, response):
        next_page = response.xpath(
            "//span[@class='pager-right']/a/@href"
        ).extract_first()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)
        for post in response.xpath("//h3[@class='entry-header']/a/@href").extract():
            yield scrapy.Request(url=post, callback=self.parse_post)

    def parse_post(self, response):
        yield {
            "Date": re.findall("\d{4}\/\d{2}", response.url)[0],
            "Site url": self.start_urls[0],
            "Article url": response.url,
            "Author": response.xpath("//a[@rel='author']/text()").extract_first(),
            "Title": response.xpath(
                "//h3[@class='entry-header']//text()"
            ).extract_first(),
            "Article body text": " ".join(
                response.xpath("//div[@class='entry-content']//text()").extract()
            ),
        }
