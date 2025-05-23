
BOT_NAME = "jdscraper"
SPIDER_MODULES = ["jdscraper.spiders"]
NEWSPIDER_MODULE = "jdscraper.spiders"

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    "jdscraper.pipelines.JdscraperPipeline": 300,
}
