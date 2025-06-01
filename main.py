from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from datetime import datetime
from typing import List, Dict, Any
from fastapi.responses import RedirectResponse

# FastAPI app instance
app = FastAPI(
    title="نارموون - تحلیلگر هوش مصنوعی بازارهای مالی",
    description="اولین ربات تلگرامی فارسی برای تحلیل بازارهای مالی با هوش مصنوعی",
    version="1.0.0",
    docs_url=None,  # غیرفعال کردن docs در production
    redoc_url=None
)

# Middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files with HTTPS support
app.mount("/static", StaticFiles(directory="static"), name="static")

# Force HTTPS in production
@app.middleware("http")
async def force_https(request: Request, call_next):
    if request.headers.get("x-forwarded-proto") == "http":
        url = request.url.replace(scheme="https")
        return RedirectResponse(url=str(url), status_code=301)
    response = await call_next(request)
    return response

# Templates
templates = Jinja2Templates(directory="templates")

# Sample data - در آینده از دیتابیس خوانده می‌شود
SAMPLE_ARTICLES = [
    {
        "id": 1,
        "title": "مقدمه‌ای بر تحلیل تکنیکال با هوش مصنوعی",
        "summary": "در این مقاله با اصول تحلیل تکنیکال و نحوه استفاده از هوش مصنوعی در تریدینگ آشنا می‌شوید.",
        "content": "محتوای کامل مقاله...",
        "author": "تیم نارموون",
        "date": datetime(2024, 1, 15),
        "tags": ["تحلیل تکنیکال", "هوش مصنوعی", "تریدینگ"],
        "category": "آموزشی"
    },
    {
        "id": 2,
        "title": "راهنمای کامل تحلیل بازار رمزارزها",
        "summary": "نحوه تحلیل بازار کریپتو و استفاده از ابزارهای پیشرفته نارموون",
        "content": "محتوای کامل مقاله...",
        "author": "تیم نارموون", 
        "date": datetime(2024, 1, 20),
        "tags": ["رمزارز", "بیتکوین", "تحلیل بازار"],
        "category": "بازارهای مالی"
    }
]

SAMPLE_VIDEOS = [
    {
        "id": 1,
        "title": "آموزش کامل استفاده از ربات نارموون",
        "description": "در این ویدیو نحوه استفاده از تمام امکانات ربات نارموون را یاد می‌گیرید",
        "youtube_id": "dQw4w9WgXcQ",  # نمونه - باید تغییر کند
        "duration": "15:30",
        "category": "آموزش ربات"
    },
    {
        "id": 2,
        "title": "تحلیل تصویری چارت با هوش مصنوعی",
        "description": "روش ارسال تصاویر چارت و دریافت تحلیل دقیق",
        "youtube_id": "dQw4w9WgXcQ",  # نمونه - باید تغییر کند
        "duration": "12:45",
        "category": "تحلیل تکنیکال"
    }
]

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """صفحه اصلی"""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "title": "نارموون - تحلیلگر هوش مصنوعی بازارهای مالی",
        "meta_description": "اولین ربات تلگرامی فارسی برای تحلیل بازارهای مالی با هوش مصنوعی. تحلیل رمزارز، فارکس، طلا و سهام با دقت بالا.",
        "stats": {
            "active_users": "2,500+",
            "daily_analysis": "300+", 
            "success_analysis": "هزاران",
            "strategies": "150+"
        }
    })

@app.get("/videos", response_class=HTMLResponse)
async def videos(request: Request):
    """صفحه ویدیوهای آموزشی"""
    return templates.TemplateResponse("videos.html", {
        "request": request,
        "title": "ویدیوهای آموزشی نارموون",
        "meta_description": "مجموعه ویدیوهای آموزشی نارموون برای یادگیری تحلیل بازارهای مالی با هوش مصنوعی",
        "videos": SAMPLE_VIDEOS
    })

@app.get("/articles", response_class=HTMLResponse) 
async def articles(request: Request):
    """صفحه مقالات آموزشی"""
    return templates.TemplateResponse("articles.html", {
        "request": request,
        "title": "مقالات آموزشی نارموون",
        "meta_description": "مقالات تخصصی و آموزشی درباره تحلیل بازارهای مالی، رمزارز و استفاده از هوش مصنوعی در تریدینگ",
        "articles": SAMPLE_ARTICLES
    })

@app.get("/article/{article_id}", response_class=HTMLResponse)
async def article_detail(request: Request, article_id: int):
    """جزئیات مقاله"""
    article = next((a for a in SAMPLE_ARTICLES if a["id"] == article_id), None)
    if not article:
        raise HTTPException(status_code=404, detail="مقاله یافت نشد")
    
    return templates.TemplateResponse("article_detail.html", {
        "request": request,
        "title": f"{article['title']} - نارموون",
        "meta_description": article["summary"],
        "article": article,
        "related_articles": [a for a in SAMPLE_ARTICLES if a["id"] != article_id][:3]
    })

@app.get("/sitemap.xml")
async def sitemap():
    """نقشه سایت برای SEO"""
    from fastapi.responses import Response
    
    urls = [
        {"loc": "/", "priority": "1.0", "changefreq": "daily"},
        {"loc": "/videos", "priority": "0.8", "changefreq": "weekly"},
        {"loc": "/articles", "priority": "0.8", "changefreq": "daily"},
    ]
    
    # اضافه کردن URL های مقالات
    for article in SAMPLE_ARTICLES:
        urls.append({
            "loc": f"/article/{article['id']}",
            "priority": "0.6",
            "changefreq": "monthly"
        })
    
    sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap_xml += '<urlset xmlns="https://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for url in urls:
        sitemap_xml += f'''
        <url>
            <loc>https://yourdomain.com{url["loc"]}</loc>
            <priority>{url["priority"]}</priority>
            <changefreq>{url["changefreq"]}</changefreq>
        </url>'''
    
    sitemap_xml += '\n</urlset>'
    
    return Response(content=sitemap_xml, media_type="application/xml")

@app.get("/robots.txt")
async def robots():
    """فایل robots.txt برای SEO"""
    from fastapi.responses import PlainTextResponse
    
    robots_content = """User-agent: *
Allow: /
Disallow: /admin/
Sitemap: https://yourdomain.com/sitemap.xml"""
    
    return PlainTextResponse(robots_content)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000)),
        reload=True
    )
