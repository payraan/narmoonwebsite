#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.path.append('./blog_system')
from blog_helpers import create_blog_post

def add_long_article():
    print("📝 افزودن مقاله طولانی")
    print("=" * 40)
    
    title = input("عنوان مقاله: ")
    excerpt = input("خلاصه مقاله: ")
    tags_input = input("تگ‌ها (با کاما): ")
    tags = [tag.strip() for tag in tags_input.split(',')] if tags_input else []
    
    print("\n📄 محتوای مقاله:")
    print("(برای پایان، خط خالی + 'END' تایپ کنید)")
    
    content_lines = []
    while True:
        line = input()
        if line.strip() == 'END':
            break
        content_lines.append(line)
    
    content = '\n'.join(content_lines)
    
    if title and content:
        post = create_blog_post(title, content, excerpt=excerpt, tags=tags)
        print(f"\n✅ مقاله '{post.title}' اضافه شد!")
        print(f"   Slug: {post.slug}")
    else:
        print("❌ عنوان و محتوا الزامی است!")

if __name__ == "__main__":
    add_long_article()
