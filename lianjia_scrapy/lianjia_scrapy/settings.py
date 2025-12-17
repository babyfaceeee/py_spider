# Scrapy settings for lianjia_scrapy project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "lianjia_scrapy"

SPIDER_MODULES = ["lianjia_scrapy.spiders"]
NEWSPIDER_MODULE = "lianjia_scrapy.spiders"

ADDONS = {}


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "lianjia_scrapy (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Concurrency and throttling settings
#CONCURRENT_REQUESTS = 16
CONCURRENT_REQUESTS_PER_DOMAIN = 2
DOWNLOAD_DELAY = 0.25

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
    "Cookie":"select_city=110000; lianjia_uuid=4dcc0b93-2709-44c3-96ed-611e11ba354c; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2219aecf6bbaf215f-00581b4a4ebb72-1d525631-2073600-19aecf6bbb02d90%22%2C%22%24device_id%22%3A%2219aecf6bbaf215f-00581b4a4ebb72-1d525631-2073600-19aecf6bbb02d90%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; crosSdkDT2019DeviceId=-6q37bm-jl0xj6-lkfrfff7xgm6gjr-1x0jakhgv; login_ucid=2000000515593808; ftkrc_=f89b9de8-94de-4a09-b502-5ae239cdaef4; lfrc_=92132112-da63-42fe-b20c-454cd83a52d9; lianjia_token=2.00148caf354fd29489052186040512105c; lianjia_token_secure=2.00148caf354fd29489052186040512105c; security_ticket=r0PDjqIHZ6/JvHlYPDp2cYASDre+ZmpeUmI/ODWSsju1FobT4y1Ig7D+K1GDDQcN20SlNv8A/AxPY5lXhBOtTSnHE06gT0rMCH2kRlLcOlo93jw1KZzycg4LM0dbKC5KUEm9MEtmD6UqLi5atfsNSZMLIDKzv17bzpv2OBudRQ4=; lianjia_ssid=a53aa6ab-7989-44cc-8ee0-1d89515ba271; hip=0-OOmOg5e2-ULPkOoTy-AckdUBLw-bFOaOC5A50tcrxHdWQxcbxnpsnJgT43AX-o7z41VU8yAceXqnULB7Qr8l08ymOoLhpXmlde2lAkYkNyhWdNdHKqA8eDJdjLqbC9Mg8KFd1FwqRoRcu0x9F4TPUZCPjt4vZtrwIWICbybD9IzM1nDfuDYCZSxJ9XTHD1wQHncUe0ZCjQtd9oYbXLU15jHzU9CjMGNGJ-u2NqUgbtqR2EtQEFrz6mNVErQw5atE_Z-Wfa9eiXtInq_0-ZvKgihxBxfWHwGP8G",
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "lianjia_scrapy.middlewares.LianjiaScrapySpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    "lianjia_scrapy.middlewares.LianjiaScrapyDownloaderMiddleware": None,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "lianjia_scrapy.pipelines.LianjiaScrapyPipeline": 300,
    'lianjia_scrapy.exporters.CsvExportPipeline': 350,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
FEED_EXPORT_ENCODING = "utf-8-sig"

