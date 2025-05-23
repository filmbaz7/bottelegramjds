
import scrapy

class JdscraperItem(scrapy.Item):
    name = scrapy.Field()
    priceWas = scrapy.Field()
    priceIs = scrapy.Field()
    difference = scrapy.Field()
    discount = scrapy.Field()
    link = scrapy.Field()
    image = scrapy.Field()
