import sys
sys.path.append('./blog_system')
from database import BlogPost, get_db
from sqlalchemy.orm import Session
from typing import List, Optional
import json
import re
from datetime import datetime
import uuid

def create_safe_slug(title: str):
    """ساخت slug امن و منحصربفرد"""
    # تبدیل به لاتین ساده
    slug = title.lower()
    slug = re.sub(r'[ای]', 'i', slug)
    slug = re.sub(r'[او]', 'a', slug) 
    slug = re.sub(r'[ه]', 'h', slug)
    slug = re.sub(r'[\u200c\s]+', '-', slug)  # نیم‌فاصله و فاصله
    slug = re.sub(r'[^\w\-]', '', slug)  # حذف کاراکترهای خاص
    slug = re.sub(r'\-+', '-', slug)  # تکرار خط تیره
    slug = slug.strip('-')
    
    # اگر خالی شد، uuid بساز
    if not slug:
        slug = f"post-{uuid.uuid4().hex[:8]}"
    
    return slug

def create_unique_slug(title: str):
    """ساخت slug منحصربفرد"""
    base_slug = create_safe_slug(title)
    slug = base_slug
    counter = 1
    
    db = next(get_db())
    
    # چک کردن تکراری بودن
    while db.query(BlogPost).filter(BlogPost.slug == slug).first():
        slug = f"{base_slug}-{counter}"
        counter += 1
    
    db.close()
    return slug

def create_blog_post(title: str, content: str, slug: str = None, excerpt: str = None, 
                    thumbnail: str = None, tags: List[str] = None):
    """ساخت مقاله جدید"""
    if not slug:
        slug = create_unique_slug(title)
    
    db = next(get_db())
    
    blog_post = BlogPost(
        title=title,
        slug=slug,
        content=content,
        excerpt=excerpt,
        thumbnail=thumbnail,
        tags=json.dumps(tags, ensure_ascii=False) if tags else None,
        is_published=True
    )
    
    try:
        db.add(blog_post)
        db.commit()
        db.refresh(blog_post)
        return blog_post
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def get_all_posts():
    """دریافت همه مقالات منتشر شده"""
    db = next(get_db())
    posts = db.query(BlogPost).filter(BlogPost.is_published == True).order_by(BlogPost.created_at.desc()).all()
    db.close()
    return posts

def get_post_by_slug(slug: str):
    """دریافت مقاله با slug"""
    db = next(get_db())
    post = db.query(BlogPost).filter(BlogPost.slug == slug, BlogPost.is_published == True).first()
    db.close()
    return post
