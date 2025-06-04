#!/usr/bin/env python3
import sys
sys.path.append('./blog_system')
from blog_helpers import create_blog_post, get_all_posts, get_post_by_slug

def add_post():
    print("\n📝 افزودن مقاله جدید")
    title = input("عنوان مقاله: ")
    content = input("محتوای مقاله: ")
    excerpt = input("خلاصه مقاله (اختیاری): ") or None
    tags_input = input("تگ‌ها (با کاما جدا کنید): ")
    tags = [tag.strip() for tag in tags_input.split(',')] if tags_input else None
    
    post = create_blog_post(title, content, excerpt=excerpt, tags=tags)
    print(f"✅ مقاله '{post.title}' با موفقیت اضافه شد!")
    print(f"   Slug: {post.slug}")

def list_posts():
    print("\n📋 لیست مقالات")
    posts = get_all_posts()
    if not posts:
        print("هیچ مقاله‌ای موجود نیست.")
        return
    
    for i, post in enumerate(posts, 1):
        tags = eval(post.tags) if post.tags else []
        print(f"{i}. {post.title}")
        print(f"   Slug: {post.slug}")
        print(f"   تگ‌ها: {', '.join(tags)}")
        print(f"   تاریخ: {post.created_at.strftime('%Y-%m-%d %H:%M')}")
        print()

def main():
    while True:
        print("\n🎯 مدیریت Blog نارمون")
        print("1. افزودن مقاله")
        print("2. نمایش مقالات")
        print("3. خروج")
        
        choice = input("\nانتخاب کنید (1-3): ")
        
        if choice == '1':
            add_post()
        elif choice == '2':
            list_posts()
        elif choice == '3':
            print("👋 خداحافظ!")
            break
        else:
            print("❌ انتخاب نامعتبر!")

if __name__ == "__main__":
    main()
