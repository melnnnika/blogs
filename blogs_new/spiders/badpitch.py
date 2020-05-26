# -*- coding: utf-8 -*-
import json
import scrapy
import re


class BadpitchSpider(scrapy.Spider):
    name = "badpitch"
    start_urls = [
        "https://badpitch.blogspot.com/sitemap.xml?page=1",
        "https://badpitch.blogspot.com/sitemap.xml?page=2",
        "https://badpitch.blogspot.com/sitemap.xml?page=3",
        "https://badpitch.blogspot.com/sitemap.xml?page=4",
    ]
    custom_settings = {"ROBOTSTXT_OBEY": False}

    def parse(self, response):
        for post in re.findall("<loc>(.+?)<\/loc>", response.text):
            yield scrapy.Request(url=post, callback=self.parse_post)

    def parse_post(self, response):
        post_id = response.xpath("//script[contains(text(),'postId')]/text()").re_first(
            "'postId': '(.+?)'"
        )
        yield scrapy.Request(
            url="https://badpitch.blogspot.com//feeds/posts/default/%s?alt=json&v=2&dynamicviews=1&rewriteforssl=true"
            % post_id,
            callback=self.parse_api,
            meta={"url": response.url},
        )

    def parse_api(self, response):
        article_data = json.loads(response.text)
        yield {
            "Date": article_data.get("entry", {})
            .get("published", {})
            .get("$t")
            .split("T")[0],
            "Site url": "https://badpitch.blogspot.com/",
            "Article url": response.meta["url"],
            "Author": article_data.get("entry", {})
            .get("author", [])[0]
            .get("name")
            .get("$t"),
            "Title": article_data.get("entry", {}).get("title", {}).get("$t"),
            "Article body text": article_data.get("entry", {})
            .get("content", {})
            .get("$t"),
        }
