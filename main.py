from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, Response, RedirectResponse, PlainTextResponse
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
import uvicorn
import os
from datetime import datetime
from typing import List, Dict, Any

# HTTPS Scheme Middleware - باید قبل از همه چیز باشه
class HTTPSSchemeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.headers.get("x-forwarded-proto") == "https":
            request.scope['scheme'] = 'https'
        response = await call_next(request)
        return response

# Security Headers Middleware
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Security Headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        
        # Content Security Policy
        # Content Security Policy
        csp_policy = (
            "default-src 'self' https:; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' 'wasm-unsafe-eval' "
            "https://cdn.jsdelivr.net https://cdnjs.cloudflare.com "
            "https://www.googletagmanager.com https://www.google-analytics.com "
            "https://googleads.g.doubleclick.net https://*.railway.app https://narmoon.io https://www.narmoon.io; "
            "style-src 'self' 'unsafe-inline' "
            "https://cdn.jsdelivr.net https://cdnjs.cloudflare.com "
            "https://fonts.googleapis.com https://*.railway.app https://narmoon.io https://www.narmoon.io; "
            "font-src 'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com; "
            "img-src 'self' data: https: http: https://*.railway.app https://narmoon.io https://www.narmoon.io; "
            "connect-src 'self' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com https://fonts.googleapis.com https://www.google-analytics.com https://analytics.google.com https://www.google.com https://*.railway.app https://narmoon.io https://www.narmoon.io; "
            "frame-src https://www.youtube.com https://youtube.com https://www.googletagmanager.com https://td.doubleclick.net; "
            "object-src 'none'; "
            "base-uri 'self'; "
            "form-action 'self';" 
        )

        response.headers["Content-Security-Policy"] = csp_policy

        response.headers["Content-Security-Policy"] = csp_policy
        
        # HTTPS Strict Transport Security (only in production)
        if request.headers.get("x-forwarded-proto") == "https":
            request.scope['scheme'] = 'https'
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
        
        return response

# FastAPI app instance
app = FastAPI(
    title="نارموون - تحلیلگر هوش مصنوعی بازارهای مالی",
    description="اولین ربات تلگرامی فارسی برای تحلیل بازارهای مالی با هوش مصنوعی",
    version="2.0.0",
    docs_url=None,  # غیرفعال کردن docs در production
    redoc_url=None
)

# Middleware - ترتیب مهم است
app.add_middleware(HTTPSSchemeMiddleware)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://narmoon.io", "https://www.narmoon.io", "https://localhost:8000"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Static files with cache headers
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

# Force HTTPS in production
@app.middleware("http")
async def force_https(request: Request, call_next):
    # Force HTTPS redirect only in production
    if (request.headers.get("x-forwarded-proto") == "http" and 
        ("narmoon.io" in request.headers.get("host", "") or "railway.app" in request.headers.get("host", ""))):
        url = request.url.replace(scheme="https")
        return RedirectResponse(url=str(url), status_code=301)
    
    response = await call_next(request)
    
    # Cache static files
    if request.url.path.startswith("/static/"):
        response.headers["Cache-Control"] = "public, max-age=31536000"
        response.headers["Expires"] = "Thu, 31 Dec 2025 23:59:59 GMT"
    
    return response

# Templates
templates = Jinja2Templates(directory="templates")

# Add current year to template context
def add_template_globals():
    templates.env.globals['current_year'] = datetime.now().year

add_template_globals()

# Enhanced sample data
SAMPLE_ARTICLES = [
    {
        "id": 1,
        "title": "مقدمه‌ای بر تحلیل تکنیکال با هوش مصنوعی",
        "summary": "در این مقاله با اصول تحلیل تکنیکال و نحوه استفاده از هوش مصنوعی در تریدینگ آشنا می‌شوید.",
        "content": """
        <h3>مقدمه</h3>
        <p>در دنیای امروز، بازارهای مالی پیچیده‌تر از همیشه شده‌اند و تحلیل آن‌ها نیازمند ابزارهای پیشرفته است.</p>
        
        <h3>نقش هوش مصنوعی</h3>
        <p>هوش مصنوعی می‌تواند الگوهای پیچیده‌ای را در نمودارهای قیمت شناسایی کند که برای چشم انسان قابل تشخیص نیست.</p>
        
        <h3>مزایای نارموون</h3>
        <ul>
            <li>تحلیل تصویری نمودار در چند ثانیه</li>
            <li>سیگنال‌های خرید و فروش دقیق</li>
            <li>مدیریت ریسک هوشمند</li>
        </ul>
        """,
        "author": "تیم نارموون",
        "date": datetime(2025, 1, 15),
        "tags": ["تحلیل تکنیکال", "هوش مصنوعی", "تریدینگ"],
        "category": "آموزشی",
        "reading_time": "۵ دقیقه"
    },
    {
        "id": 2,
        "title": "راهنمای کامل تحلیل بازار رمزارزها",
        "summary": "نحوه تحلیل بازار کریپتو و استفاده از ابزارهای پیشرفته نارموون",
        "content": """
        <h3>بازار رمزارزها</h3>
        <p>بازار رمزارزها یکی از پرنوسان‌ترین بازارهای مالی است که نیاز به تحلیل دقیق دارد.</p>
        
        <h3>ابزارهای تحلیل</h3>
        <p>نارموون با استفاده از هوش مصنوعی، تحلیل‌های دقیقی از بازار رمزارزها ارائه می‌دهد.</p>
        """,
        "author": "تیم نارموون", 
        "date": datetime(2025, 1, 20),
        "tags": ["رمزارز", "بیتکوین", "تحلیل بازار"],
        "category": "بازارهای مالی",
        "reading_time": "۸ دقیقه"
    }
]

SAMPLE_VIDEOS = [
    {
        "id": 1,
        "title": "آموزش کامل استفاده از ربات نارموون",
        "description": "در این ویدیو نحوه استفاده از تمام امکانات ربات نارموون را یاد می‌گیرید",
        "youtube_id": "WjQzb7rBboM",
        "duration": "15:30",   
        "category": "آموزش ربات",
        "views": "۱,۲۳۴",
        "published_date": datetime(2025, 1, 10)
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
            "active_users": "۲,۵۰۰+",
            "daily_analysis": "۳۰۰+", 
            "success_analysis": "هزاران",
            "strategies": "۱۵۰+"
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

# SEO Routes
@app.get("/sitemap.xml", response_class=Response)
async def sitemap(request: Request):
    """نقشه سایت برای SEO"""
    base_url = str(request.base_url).rstrip('/')
    
    urls = [
        {"loc": "/", "priority": "1.0", "changefreq": "daily", "lastmod": "2025-06-01"},
        {"loc": "/videos", "priority": "0.8", "changefreq": "weekly", "lastmod": "2025-06-01"},
        {"loc": "/articles", "priority": "0.8", "changefreq": "daily", "lastmod": "2025-06-01"},
    ]
    
    # اضافه کردن URL های مقالات
    for article in SAMPLE_ARTICLES:
        urls.append({
            "loc": f"/article/{article['id']}",
            "priority": "0.6",
            "changefreq": "monthly",
            "lastmod": article['date'].strftime('%Y-%m-%d')
        })
    
    sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap_xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for url in urls:
        sitemap_xml += f'''  <url>
    <loc>{base_url}{url["loc"]}</loc>
    <lastmod>{url["lastmod"]}</lastmod>
    <changefreq>{url["changefreq"]}</changefreq>
    <priority>{url["priority"]}</priority>
  </url>\n'''
    
    sitemap_xml += '</urlset>'
    
    return Response(content=sitemap_xml, media_type="application/xml")

@app.get("/robots.txt", response_class=PlainTextResponse)
async def robots(request: Request):
    """فایل robots.txt برای SEO"""
    base_url = str(request.base_url).rstrip('/')
    
    robots_content = f"""User-agent: *
Allow: /
Disallow: /admin/
Disallow: /api/
Disallow: /_next/
Disallow: /static/

# Sitemap
Sitemap: {base_url}/sitemap.xml

# Crawl delay
Crawl-delay: 1"""
    
    return PlainTextResponse(robots_content)

@app.get("/manifest.json", response_class=Response)
async def manifest():
    """Web App Manifest برای PWA"""
    import json
    
    manifest_json = {
        "name": "نارموون - تحلیلگر هوش مصنوعی بازارهای مالی",
        "short_name": "نارموون",
        "description": "اولین ربات تلگرامی فارسی برای تحلیل بازارهای مالی با هوش مصنوعی",
        "start_url": "/",
        "scope": "/",
        "display": "standalone",
        "background_color": "#ffffff",
        "theme_color": "#3b82f6",
        "orientation": "portrait-primary",
        "categories": ["finance", "productivity", "business"],
        "lang": "fa",
        "dir": "rtl",
        "icons": [
            {
                "src": "/static/images/logo-192.png",
                "sizes": "192x192",
                "type": "image/png",
                "purpose": "any maskable"
            },
            {
                "src": "/static/images/logo-512.png", 
                "sizes": "512x512",
                "type": "image/png",
                "purpose": "any maskable"
            },
            {
                "src": "/static/images/favicon.ico",
                "sizes": "48x48",
                "type": "image/x-icon"
            }
        ],
        "screenshots": [
            {
                "src": "/static/images/hero-dashboard.png",
                "sizes": "1280x720",
                "type": "image/png",
                "form_factor": "wide",
                "label": "Dashboard نارموون"
            }
        ]
    }
    
    return Response(
        content=json.dumps(manifest_json, ensure_ascii=False, indent=2),
        media_type="application/json"
    )

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check برای monitoring"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0",
        "service": "narmoon-website"
    }

# API Routes for future use
@app.get("/api/stats")
async def get_stats():
    """API endpoint برای آمار وبسایت"""
    return {
        "active_users": 2500,
        "daily_analysis": 300,
        "total_analysis": 50000,
        "success_rate": 85.5,
        "uptime": "99.9%"
    }

@app.get("/api/articles")
async def get_articles_api():
    """API endpoint برای دریافت مقالات"""
    return {
        "articles": SAMPLE_ARTICLES,
        "total": len(SAMPLE_ARTICLES),
        "status": "success"
    }

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    """صفحه 404 سفارشی"""
    return templates.TemplateResponse("404.html", {
        "request": request,
        "title": "صفحه یافت نشد - نارموون",
        "meta_description": "صفحه مورد نظر یافت نشد."
    }, status_code=404)

@app.exception_handler(500)
async def server_error_handler(request: Request, exc: Exception):
    """صفحه 500 سفارشی"""
    return templates.TemplateResponse("500.html", {
        "request": request,
        "title": "خطای سرور - نارموون",
        "meta_description": "خطای داخلی سرور رخ داده است."
    }, status_code=500)

# Redirect old URLs (if any)
@app.get("/home")
async def redirect_home():
    return RedirectResponse(url="/", status_code=301)

# Analytics endpoint (for internal use)
@app.post("/api/analytics")
async def track_analytics(request: Request):
    """Track user analytics"""
    try:
        data = await request.json()
        # در آینده می‌توان آمار را در دیتابیس ذخیره کرد
        print(f"Analytics: {data}")
        return {"status": "tracked"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    # تنظیمات مختلف برای development و production
    is_development = os.environ.get("DEBUG", "False").lower() == "true"
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000)),
        reload=is_development,
        log_level="info" if not is_development else "debug",
        access_log=True,
        forwarded_allow_ips="*",
    )

@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    """صفحه درباره نارموون"""
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/blog", response_class=HTMLResponse)
async def blog(request: Request):
    import sys
    sys.path.append("./blog_system")
    try:
        from blog_helpers import get_all_posts
        posts = get_all_posts()
        
        html = f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>وبلاگ نارمون</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.rtl.min.css" rel="stylesheet">
    <link rel="stylesheet" href="/css/style.min.css">
</head>
<body>
    <div class="container py-5">
        <h1 class="text-center mb-5">🎯 وبلاگ نارمون</h1>
        <div class="alert alert-success text-center mb-4">
            <strong>{len(posts)} مقاله منتشر شده</strong>
        </div>
        <div class="row">"""  
        
        for post in posts:
            html += f"""<div class="col-md-6 col-lg-4 mb-4">
                <div class="card h-100 shadow-sm">
                    <div class="card-body">
                        <h5 class="card-title">{post.title}</h5>
                        <p class="text-muted">{post.excerpt[:100] if post.excerpt else ""}...</p>
                        <small class="text-muted">{post.created_at.strftime("%Y/%m/%d")}</small>
                    </div>
                </div>
            </div>"""
        
        html += """</div></div></body></html>"""
        return HTMLResponse(html)
    except Exception as e:
        return HTMLResponse(f"<h1>خطا: {str(e)}</h1>")

@app.get("/blog/{slug}", response_class=HTMLResponse)
async def blog_post(request: Request, slug: str):
    """صفحه مقاله منفرد - آماده برای آینده"""
    # فعلاً redirect به صفحه اصلی blog
    return RedirectResponse(url="/blog", status_code=302)

@app.get("/blog/tag/{tag}", response_class=HTMLResponse)
async def blog_tag(request: Request, tag: str):
    """صفحه برچسب مقالات - آماده برای آینده"""
    # فعلاً redirect به صفحه اصلی blog  
    return RedirectResponse(url="/blog", status_code=302)

@app.get("/blog/archive/{year}/{month}", response_class=HTMLResponse)
async def blog_archive(request: Request, year: int, month: int):
    """صفحه آرشیو مقالات - آماده برای آینده"""
    # فعلاً redirect به صفحه اصلی blog
    return RedirectResponse(url="/blog", status_code=302)

@app.post("/newsletter")
async def newsletter_subscribe(request: Request):
    """عضویت در خبرنامه"""
    form = await request.form()
    email = form.get("email")
    
    if email:
        # اینجا می‌تونی email رو در database ذخیره کنی
        # فعلاً فقط success response برمی‌گردونیم
        return {"status": "success", "message": "عضویت با موفقیت انجام شد"}
    else:
        return {"status": "error", "message": "ایمیل معتبر وارد کنید"}

# === BLOG API ===
@app.get('/api/blog')
async def blog_api():
    import sys
    sys.path.append('./blog_system')
    try:
        from blog_helpers import get_all_posts
        posts = get_all_posts()
        return {
            'success': True,
            'count': len(posts),
            'posts': [
                {
                    'title': post.title,
                    'excerpt': post.excerpt,
                    'created_at': post.created_at.strftime('%Y/%m/%d'),
                    'word_count': len(post.content.split())
                }
                for post in posts
            ]
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}


@app.get("/blog-real", response_class=HTMLResponse)
async def blog_real():
    import sys
    sys.path.append('./blog_system')
    try:
        from blog_helpers import get_all_posts
        posts = get_all_posts()
        
        html = f'''
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>وبلاگ نارمون</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.rtl.min.css" rel="stylesheet">
    <link rel="stylesheet" href="/css/style.min.css">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm">
        <div class="container">
            <a class="navbar-brand" href="/">
                <img src="/images/logo.png" alt="نارمون" height="50">
            </a>
            <div class="navbar-nav">
                <a class="nav-link" href="/">خانه</a>
                <a class="nav-link active" href="/blog-real">وبلاگ</a>
                <a class="nav-link" href="/about">درباره ما</a>
            </div>
        </div>
    </nav>
    
    <div class="container py-5">
        <h1 class="text-center mb-5">🎯 وبلاگ نارمون</h1>
        <div class="alert alert-success text-center">
            <strong>{len(posts)} مقاله</strong> منتشر شده
        </div>
        
        <div class="row">'''
        
        for post in posts:
            html += f'''
            <div class="col-md-6 col-lg-4 mb-4">
                <div class="card h-100 shadow-sm">
                    <div class="card-body">
                        <h5 class="card-title">{post.title}</h5>
                        <p class="card-text text-muted">{post.excerpt[:100] if post.excerpt else ""}...</p>
                        <div class="d-flex justify-content-between align-items-center">
                            <small class="text-muted">{post.created_at.strftime('%Y/%m/%d')}</small>
                            <span class="badge bg-primary">{len(post.content.split())} کلمه</span>
                        </div>
                    </div>
                </div>
            </div>'''
        
        html += '''
        </div>
        <div class="text-center mt-5">
            <a href="/api/blog" class="btn btn-outline-primary">مشاهده API</a>
        </div>
    </div>
</body>
</html>'''
        return HTMLResponse(html)
    except Exception as e:
        return HTMLResponse(f'<h1>خطا: {str(e)}</h1><p><a href="/">بازگشت به خانه</a></p>')
