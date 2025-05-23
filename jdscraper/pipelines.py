from .db import get_connection

class JdscraperPipeline:
    def open_spider(self, spider):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()
        self.cursor.execute('DELETE FROM products')  # حذف داده‌های قبلی قبل از شروع اسکرپ
        self.conn.commit()

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        self.save_product(item)
        return item

    def save_product(self, item):
        self.cursor.execute('''
            INSERT INTO products (name, priceWas, priceIs, difference, discount, link, image) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(link) DO UPDATE SET
                name=excluded.name,
                priceWas=excluded.priceWas,
                priceIs=excluded.priceIs,
                difference=excluded.difference,
                discount=excluded.discount,
                image=excluded.image
        ''', (
            item.get('name'),
            item.get('priceWas'),
            item.get('priceIs'),
            item.get('difference'),
            item.get('discount'),
            item.get('link'),
            item.get('image')
        ))
        self.conn.commit()
