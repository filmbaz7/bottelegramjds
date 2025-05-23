
from fastapi import FastAPI
import sqlite3
import os

app = FastAPI()
DB_PATH = os.path.join(os.path.dirname(__file__), "jdscraper", "products.db")

@app.get("/")
def read_root():
    return {"message": "JD Sports Discount API is live!"}

@app.get("/products")
def get_products():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name, priceWas, priceIs, difference, discount, link, image FROM products")
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            "name": row[0],
            "priceWas": row[1],
            "priceIs": row[2],
            "difference": row[3],
            "discount": row[4],
            "link": row[5],
            "image": row[6],
        }
        for row in rows
    ]
