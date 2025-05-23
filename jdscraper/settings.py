# تنظیمات اصلی Scrapy

BOT_NAME = 'jdscraper'

SPIDER_MODULES = ['jdscraper.spiders']
NEWSPIDER_MODULE = 'jdscraper.spiders'

# فعال کردن pipeline
ITEM_PIPELINES = {
    'jdscraper.pipelines.JdscraperPipeline': 300,
}

# رعایت ربات‌ها (اختیاری)
ROBOTSTXT_OBEY = True

# تنظیمات مربوط به User-Agent (اختیاری ولی پیشنهاد میشه)
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36'
