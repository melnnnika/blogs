# -*- coding: utf-8 -*-
import scrapy


class CuriouscatblogSpider(scrapy.Spider):
    name = "curiouscatblog"
    start_urls = [
        "http://management.curiouscatblog.net/category/popular/",
        "https://management.curiouscatblog.net/category/books/",
        "https://management.curiouscatblog.net/category/career/",
        "https://management.curiouscatblog.net/category/carnival/",
        "https://management.curiouscatblog.net/category/china/",
        "https://management.curiouscatblog.net/category/competition/",
        "https://management.curiouscatblog.net/category/creativity/",
        "https://management.curiouscatblog.net/category/curiouscatcom/",
        "https://management.curiouscatblog.net/category/customer-focus/",
        "https://management.curiouscatblog.net/category/data/",
        "https://management.curiouscatblog.net/category/deming/",
        "https://management.curiouscatblog.net/category/design-of-experiments/",
        "https://management.curiouscatblog.net/category/economics/",
        "https://management.curiouscatblog.net/category/education/",
        "https://management.curiouscatblog.net/category/fun/",
        "https://management.curiouscatblog.net/category/google/",
        "https://management.curiouscatblog.net/category/health-care/",
        "https://management.curiouscatblog.net/category/india/",
        "https://management.curiouscatblog.net/category/innovation/",
        "https://management.curiouscatblog.net/category/investing/",
        "https://management.curiouscatblog.net/category/it/",
        "https://management.curiouscatblog.net/category/lean-thinking/",
        "https://management.curiouscatblog.net/category/management-improvement/",
        "https://management.curiouscatblog.net/category/management-articles/",
        "https://management.curiouscatblog.net/category/manufacturing/",
        "https://management.curiouscatblog.net/category/performance-appraisal/",
        "https://management.curiouscatblog.net/category/popular/",
        "https://management.curiouscatblog.net/category/process-improvement/",
        "https://management.curiouscatblog.net/category/psychology/",
        "https://management.curiouscatblog.net/category/public-sector/",
        "https://management.curiouscatblog.net/category/quality-tools/",
        "https://management.curiouscatblog.net/category/quote/",
        "https://management.curiouscatblog.net/category/respect/",
        "https://management.curiouscatblog.net/category/science/",
        "https://management.curiouscatblog.net/category/six-sigma/",
        "https://management.curiouscatblog.net/category/software-development/",
        "https://management.curiouscatblog.net/category/statistics/",
        "https://management.curiouscatblog.net/category/systems-thinking/",
        "https://management.curiouscatblog.net/category/tags/",
        "https://management.curiouscatblog.net/category/theory-of-constraints/",
        "https://management.curiouscatblog.net/category/toyota-production-system-tps/",
        "https://management.curiouscatblog.net/category/travel-photos/",
        "https://management.curiouscatblog.net/category/uk/",
        "https://management.curiouscatblog.net/category/webcast/",
    ]

    def parse(self, response):
        for page in response.xpath("//div[@class='nav-previous']/a/@href").extract():
            yield scrapy.Request(url=response.urljoin(page), callback=self.parse)
        for post in response.xpath("//h1[@class='entry-title']/a/@href").extract():
            yield scrapy.Request(url=post, callback=self.parse_post)

    def parse_post(self, response):
        yield {
            "Date": response.xpath("//time/@datetime").extract_first().split("T")[0],
            "Site url": "http://management.curiouscatblog.net",
            "Article url": response.url,
            "Author": "John Hunter",
            "Title": response.xpath("//h1/text()").extract_first(),
            "Article body text": " ".join(
                response.xpath(
                    "//div[@class='entry-content']//*[not(self::script)]/text()"
                ).extract()
            ),
        }
