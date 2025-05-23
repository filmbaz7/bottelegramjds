
import scrapy
from jdscraper.items import JdscraperItem

class JDSpider(scrapy.Spider):
    name = "jd"
    allowed_domains = ["jdsports.it"]
    start_urls = ["https://www.jdsports.it/saldi/"]

    def parse(self, response):
        for product in response.css("div.ProductListItem"):
            item = JdscraperItem()
            item["name"] = product.css("a.ProductTitle::text").get()
            item["priceWas"] = self.extract_price(product.css("span.ProductPrice-original span::text").get())
            item["priceIs"] = self.extract_price(product.css("span.ProductPrice-current span::text").get())
            item["link"] = response.urljoin(product.css("a.ProductTitle::attr(href)").get())
            item["image"] = product.css("img::attr(src)").get()
            if item["priceWas"] and item["priceIs"]:
                item["difference"] = round(item["priceWas"] - item["priceIs"], 2)
                item["discount"] = round((item["difference"] / item["priceWas"]) * 100, 1)
            yield item

        next_page = response.css("a.Pagination-link[rel='next']::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def extract_price(self, price_str):
        if price_str:
            return float(price_str.replace("€", "").replace(",", ".").strip())
        return None
