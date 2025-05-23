import sqlite3
import subprocess
import requests
from fastapi import FastAPI, Request, BackgroundTasks
from apscheduler.schedulers.background import BackgroundScheduler

BOT_TOKEN = "8020973419:AAGtjkbfb4BJBIR3_lA5GMOUzRZdO0iTGDE"
MIN_DISCOUNT = 30
DB_PATH = "products.db"

app = FastAPI()

# ======== دیتابیس ========
def create_tables():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        priceWas REAL,
        priceIs REAL,
        difference REAL,
        discount REAL,
        link TEXT UNIQUE,
        image TEXT
    )''')
    conn.execute('''
    CREATE TABLE IF NOT EXISTS users (
        chat_id TEXT PRIMARY KEY
    )''')
    conn.commit()
    conn.close()

def add_user(chat_id: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (chat_id) VALUES (?)", (chat_id,))
    conn.commit()
    conn.close()

def get_all_users():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT chat_id FROM users")
    users = [row[0] for row in cursor.fetchall()]
    conn.close()
    return users

# ======== ارسال پیام تلگرام ========
def send_message(chat_id: str, text: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    try:
        r = requests.post(url, data=payload, timeout=10)
        r.raise_for_status()
    except Exception as e:
        print(f"Error sending message to {chat_id}: {e}")

# ======== اجرای اسکرایپ و ارسال تخفیف ========
def run_scraper_and_notify():
    print("شروع اجرای اسپایدر...")
    # اجرای اسپایدر (مطمئن شو scrapy و spider اسم درست دارن)
    subprocess.run(["scrapy", "crawl", "jd_spider"], check=True)
    
    print("خواندن محصولات با تخفیف بالای 30 درصد...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name, priceWas, priceIs, discount, link FROM products WHERE discount >= ?", (MIN_DISCOUNT,))
    products = cursor.fetchall()
    conn.close()

    if not products:
        print("تخفیف بالای 30 درصد یافت نشد.")
        return

    users = get_all_users()
    if not users:
        print("هیچ کاربری ثبت نشده است.")
        return

    print(f"ارسال پیام به {len(users)} کاربر...")
    for user_chat_id in users:
        for p in products:
            name, priceWas, priceIs, discount, link = p
            msg = (f"🔥 <b>{name}</b>\n"
                   f"قیمت قبلی: {priceWas} یورو\n"
                   f"قیمت جدید: {priceIs} یورو\n"
                   f"تخفیف: {discount}%\n"
                   f"<a href='{link}'>مشاهده محصول</a>")
            send_message(user_chat_id, msg)

# ======== وبهوک ========
@app.post("/webhook")
async def webhook_update(request: Request, background_tasks: BackgroundTasks):
    data = await request.json()
    if "message" in data:
        chat_id = str(data["message"]["chat"]["id"])
        add_user(chat_id)
        background_tasks.add_task(run_scraper_and_notify)
    return {"ok": True}

# ======== زمان‌بندی هر 3 دقیقه ========
scheduler = BackgroundScheduler()
scheduler.add_job(run_scraper_and_notify, 'interval', minutes=3)
scheduler.start()

# ======== اجرای اولیه ساخت جداول ========
create_tables()
