x HEAD
# 🌟 وبسایت نارموون

وبسایت معرفی ربات تلگرامی نارموون - تحلیلگر هوش مصنوعی بازارهای مالی

## 🚀 ویژگی‌ها

- **FastAPI** - فریمورک سریع و مدرن Python
- **Jinja2 Templates** - قالب‌بندی قدرتمند
- **Bootstrap 5 RTL** - طراحی ریسپانسیو فارسی
- **SEO Optimized** - بهینه‌سازی کامل برای موتورهای جستجو
- **Mobile First** - طراحی اولویت موبایل
- **Fast Loading** - سرعت بارگذاری بالا

## 📁 ساختار پروژه

```
narmoon-website/
├── main.py                 # اپلیکیشن اصلی FastAPI
├── requirements.txt        # وابستگی‌های Python
├── Dockerfile             # کانتینر Docker
├── railway.json           # تنظیمات Railway
├── .env.example           # نمونه متغیرهای محیطی
├── templates/             # قالب‌های HTML
│   ├── base.html          # قالب پایه
│   ├── index.html         # صفحه اصلی
│   ├── videos.html        # ویدیوهای آموزشی
│   ├── articles.html      # لیست مقالات
│   └── article_detail.html # جزئیات مقاله
├── static/               # فایل‌های استاتیک
│   ├── css/
│   │   └── style.css     # استایل‌های سفارشی
│   ├── js/
│   │   └── main.js       # جاوااسکریپت اصلی
│   └── images/           # تصاویر
└── README.md            # راهنمای نصب
```

## 🛠️ نصب و راه‌اندازی

### پیش‌نیازها
- Python 3.8+
- pip package manager

### 1️⃣ کلون کردن پروژه
```bash
git clone <repository-url>
cd narmoon-website
```

### 2️⃣ ایجاد محیط مجازی
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# یا
venv\Scripts\activate     # Windows
```

### 3️⃣ نصب وابستگی‌ها
```bash
pip install -r requirements.txt
```

### 4️⃣ تنظیم متغیرهای محیطی
```bash
cp .env.example .env
# ویرایش فایل .env
```

### 5️⃣ اجرای برنامه
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

وبسایت در آدرس `http://localhost:8000` در دسترس خواهد بود.

## 🌐 استقرار روی Railway

### 1️⃣ ایجاد اکانت Railway
- به [railway.app](https://railway.app) بروید
- با GitHub اکانت خود وارد شوید

### 2️⃣ اتصال به مخزن
- "New Project" را کلیک کنید
- "Deploy from GitHub repo" را انتخاب کنید
- مخزن پروژه را انتخاب کنید

### 3️⃣ تنظیم متغیرهای محیطی
در بخش Variables این متغیرها را اضافه کنید:
```
PORT=8000
GOOGLE_ANALYTICS_ID=your_ga_id
DOMAIN_NAME=your-domain.com
```

### 4️⃣ استقرار خودکار
Railway به صورت خودکار پروژه را build و deploy می‌کند.

## 📄 اضافه کردن محتوا

### مقالات جدید
برای اضافه کردن مقاله جدید، در فایل `main.py` در لیست `SAMPLE_ARTICLES` یک آیتم جدید اضافه کنید:

```python
{
    "id": 3,
    "title": "عنوان مقاله",
    "summary": "خلاصه مقاله",
    "content": "محتوای کامل مقاله",
    "author": "نویسنده",
    "date": datetime(2024, 2, 1),
    "tags": ["تگ1", "تگ2"],
    "category": "دسته‌بندی"
}
```

### ویدیوهای جدید
برای اضافه کردن ویدیو جدید، در لیست `SAMPLE_VIDEOS` یک آیتم جدید اضافه کنید:

```python
{
    "id": 3,
    "title": "عنوان ویدیو",
    "description": "توضیحات ویدیو",
    "youtube_id": "VIDEO_ID_FROM_YOUTUBE",
    "duration": "مدت زمان",
    "category": "دسته‌بندی"
}
```

## 🎨 سفارشی‌سازی

### تغییر رنگ‌ها
رنگ‌های پایه در فایل `static/css/style.css` تعریف شده‌اند:

```css
:root {
    --primary-color: #20B2AA; /* فیروزه‌ای */
    --primary-dark: #1a9999;
    --primary-light: #4dd0c7;
    /* سایر رنگ‌ها... */
}
```

### اضافه کردن تصاویر
تصاویر را در پوشه `static/images/` قرار دهید:
- `logo.png` - لوگوی اصلی
- `logo-white.png` - لوگوی سفید برای footer
- `favicon.ico` - آیکون وبسایت
- `hero-dashboard.png` - تصویر اصلی
- `narmoon-og.jpg` - تصویر Open Graph

## 📱 SEO و بهینه‌سازی

### Google Analytics
1. اکانت Google Analytics ایجاد کنید
2. کد tracking را در متغیر `GOOGLE_ANALYTICS_ID` قرار دهید
3. در `templates/base.html` خط مربوطه را فعال کنید

### Search Console
1. وبسایت را به Google Search Console اضافه کنید
2. فایل sitemap در `/sitemap.xml` موجود است
3. فایل robots.txt در `/robots.txt` موجود است

### سرعت بارگذاری
- فشرده‌سازی GZIP فعال است
- تصاویر Lazy Loading دارند
- فایل‌های CSS/JS minify شده‌اند

## 🔧 مشکل‌یابی

### خطاهای رایج
1. **Port در دسترس نیست**: پورت 8000 را تغییر دهید
2. **فایل‌های static لود نمی‌شوند**: مسیر `static/` را بررسی کنید
3. **خطای Import**: وابستگی‌ها را مجدداً نصب کنید

### لاگ‌ها
```bash
# مشاهده لاگ‌های Railway
railway logs

# اجرای محلی با debug
uvicorn main:app --reload --log-level debug
```

## 📞 پشتیبانی

- مشکلات فنی: Issue در GitHub
- سوالات عمومی: تلگرام @NarmoonAI_BOT

## 📄 مجوز

این پروژه تحت مجوز MIT است. جزئیات در فایل LICENSE موجود است.

---

**ساخته شده با ❤️ برای نارموون**
# narmoonwebsite
website
origin/main
