# -*- coding: utf-8 -*-

# Scrapy settings for blogs_new project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "blogs_new"

SPIDER_MODULES = ["blogs_new.spiders"]
NEWSPIDER_MODULE = "blogs_new.spiders"
# DEFAULT_REQUEST_HEADERS = {
#     "authority": "www.jonloomer.com",
#     "cache-control": "max-age=0",
#     "upgrade-insecure-requests": "1",
#     "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36",
#     "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
#     "sec-fetch-site": "same-origin",
#     "sec-fetch-mode": "navigate",
#     "sec-fetch-user": "?1",
#     "sec-fetch-dest": "document",
#     "referer": "https://www.jonloomer.com/",
#     "accept-language": "uk-UA,uk;q=0.9,ru;q=0.8,en-US;q=0.7,en;q=0.6",
#     "cookie": "__cfduid=dd51887e21a6972663bd912d7bf411fd21589271650; _omappvp=mqnlLg6FFgB3YXNfRnSfkDxzvMAEcX6mDJ9cZCXDT7V34nhbypqSuRt6FxZZ2MIPJnS3Va6R7oAIQTRZZk3PkBNwVfk0xe5O; nabParticipation=true%2C100; nabAlternative=13; _ga=GA1.2.650525861.1589271655; __qca=P0-1874362452-1589271653992; nabExperimentsWithPageViews=%7B%2230438%22%3A1589271657172%7D; cf_clearance=6ac2a492823b7013c301836797eb4292c5b3b48e-1589801210-0-250; _gid=GA1.2.2303374.1589801214; _gat_UA-27497054-1=1",
# }

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'blogs_new (+http://www.yourdomain.com)'

# Obey robots.txt rules
# ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'blogs_new.middlewares.BlogsNewSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'blogs_new.middlewares.BlogsNewDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'blogs_new.pipelines.BlogsNewPipeline': 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
