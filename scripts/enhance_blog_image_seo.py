#!/usr/bin/env python3
"""Enhance ShopLovaNest blog image SEO metadata.

Updates static blog article HTML and sitemap image metadata:
- img alt/title for hero images
- figcaption after hero image when absent
- og:image / twitter:image / image alt metadata
- JSON-LD BlogPosting with ImageObject
- sitemap lastmod + image:image tags for blog URLs
"""
from __future__ import annotations

from datetime import date
from html import escape
from pathlib import Path
import json
import re
import sys
import xml.etree.ElementTree as ET

SITE = "https://shoplovanest.com"
BLOG_ROOT = Path("upload/blog")
SITEMAP = Path("upload/sitemap.xml")
TODAY = date.today().isoformat()


def clean_text(s: str) -> str:
    s = re.sub(r"<[^>]+>", " ", s or "")
    s = re.sub(r"\s+", " ", s).strip()
    return s


def attr(tag: str, name: str) -> str | None:
    m = re.search(rf'\b{name}\s*=\s*(["\'])(.*?)\1', tag, re.I | re.S)
    return m.group(2) if m else None


def set_attr(tag: str, name: str, value: str) -> str:
    value = escape(value, quote=True)
    if re.search(rf'\b{name}\s*=', tag, re.I):
        return re.sub(rf'\b{name}\s*=\s*(["\']).*?\1', f'{name}="{value}"', tag, flags=re.I | re.S)
    return tag[:-1].rstrip() + f' {name}="{value}">'


def upsert_meta(head: str, prop_or_name: str, key: str, content: str) -> str:
    esc_content = escape(content, quote=True)
    pattern = rf'<meta\s+{prop_or_name}=["\']{re.escape(key)}["\']\s+content=["\'][^"\']*["\']\s*/?>'
    repl = f'<meta {prop_or_name}="{key}" content="{esc_content}">'
    if re.search(pattern, head, re.I):
        return re.sub(pattern, repl, head, flags=re.I)
    # Insert near other social tags if present, otherwise before </head>
    return head.rstrip() + "\n" + repl + "\n"


def remove_existing_generated_jsonld(head: str) -> str:
    return re.sub(
        r'\n?\s*<script type="application/ld\+json" data-shoplovanest-image-seo="true">.*?</script>\s*',
        "\n",
        head,
        flags=re.I | re.S,
    )


def article_body_excerpt(text: str, limit: int = 180) -> str:
    body = re.search(r"<body[^>]*>(.*?)</body>", text, re.I | re.S)
    source = body.group(1) if body else text
    # Drop scripts/styles/nav-ish chunks roughly by tags, then text.
    source = re.sub(r"<script\b.*?</script>|<style\b.*?</style>", " ", source, flags=re.I | re.S)
    words = clean_text(source)
    if len(words) > limit:
        words = words[:limit].rsplit(" ", 1)[0] + "…"
    return words


def enhance_article(path: Path) -> dict | None:
    slug = path.parent.name
    text = path.read_text(encoding="utf-8", errors="ignore")
    original = text
    title = clean_text((re.search(r"<h1[^>]*>(.*?)</h1>", text, re.I | re.S) or re.search(r"<title>(.*?)</title>", text, re.I | re.S) or [None, slug.replace('-', ' ').title()]).group(1) if hasattr((re.search(r"<h1[^>]*>(.*?)</h1>", text, re.I | re.S) or re.search(r"<title>(.*?)</title>", text, re.I | re.S) or [None, slug.replace('-', ' ').title()]), 'group') else slug.replace('-', ' ').title())
    # Safer title extraction after the one-liner above.
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", text, re.I | re.S)
    ttl = re.search(r"<title>(.*?)</title>", text, re.I | re.S)
    title = clean_text(h1.group(1) if h1 else (ttl.group(1) if ttl else slug.replace('-', ' ').title()))
    meta_desc_m = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']\s*/?>', text, re.I | re.S)
    description = clean_text(meta_desc_m.group(1)) if meta_desc_m else article_body_excerpt(text)

    img_m = re.search(r'<img\b(?=[^>]*\bclass=["\'][^"\']*\bhero\b)[^>]*>', text, re.I | re.S)
    if not img_m:
        img_m = re.search(r'<img\b[^>]*>', text, re.I | re.S)
    if not img_m:
        return None
    img_tag = img_m.group(0)
    src = attr(img_tag, "src")
    if not src:
        return None
    image_url = src if src.startswith("http") else SITE + (src if src.startswith("/") else "/" + src)
    alt = f"{title} — ShopLovaNest article image"
    caption = f"Visual guide for {title}, created for ShopLovaNest readers comparing intimate wellness products with privacy and care in mind."
    img_title = f"{title} | ShopLovaNest"

    new_img = set_attr(img_tag, "alt", alt)
    new_img = set_attr(new_img, "title", img_title)
    text = text[:img_m.start()] + new_img + text[img_m.end():]

    # Wrap/append figcaption immediately after hero image if no nearby/generated caption.
    after_start = img_m.start() + len(new_img)
    nearby = text[after_start:after_start + 500]
    if "data-shoplovanest-image-caption" not in nearby and not re.match(r"\s*<figcaption\b", nearby, re.I):
        fig = f'\n<figcaption class="image-caption" data-shoplovanest-image-caption="true">{escape(caption)}</figcaption>'
        text = text[:after_start] + fig + text[after_start:]

    head_m = re.search(r"<head>(.*?)</head>", text, re.I | re.S)
    if head_m:
        head = head_m.group(1)
        head = upsert_meta(head, "property", "og:image", image_url)
        head = upsert_meta(head, "property", "og:image:alt", alt)
        head = upsert_meta(head, "name", "twitter:image", image_url)
        head = upsert_meta(head, "name", "twitter:image:alt", alt)
        head = remove_existing_generated_jsonld(head)
        data = {
            "@context": "https://schema.org",
            "@type": "BlogPosting",
            "mainEntityOfPage": {"@type": "WebPage", "@id": f"{SITE}/blog/{slug}/"},
            "headline": title,
            "description": description,
            "image": {
                "@type": "ImageObject",
                "url": image_url,
                "caption": caption,
                "name": img_title,
                "description": alt,
                "width": int(attr(new_img, "width") or 1600),
                "height": int(attr(new_img, "height") or 900),
            },
            "publisher": {"@type": "Organization", "name": "ShopLovaNest", "url": SITE},
            "dateModified": TODAY,
        }
        jsonld = '<script type="application/ld+json" data-shoplovanest-image-seo="true">\n' + json.dumps(data, ensure_ascii=False, indent=2) + '\n</script>\n'
        head = head.rstrip() + "\n" + jsonld
        text = text[:head_m.start(1)] + head + text[head_m.end(1):]

    if text != original:
        path.write_text(text, encoding="utf-8")
        return {"slug": slug, "url": f"{SITE}/blog/{slug}/", "image": image_url, "title": title, "caption": caption}
    return None


def update_sitemap(entries: list[dict]) -> int:
    if not SITEMAP.exists():
        return 0
    ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    ET.register_namespace('image', 'http://www.google.com/schemas/sitemap-image/1.1')
    ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9', 'image': 'http://www.google.com/schemas/sitemap-image/1.1'}
    tree = ET.parse(SITEMAP)
    root = tree.getroot()
    by_url = {e['url']: e for e in entries}
    changed = 0
    for url_el in root.findall('sm:url', ns):
        loc_el = url_el.find('sm:loc', ns)
        if loc_el is None or loc_el.text not in by_url:
            continue
        entry = by_url[loc_el.text]
        lastmod = url_el.find('sm:lastmod', ns)
        if lastmod is None:
            lastmod = ET.SubElement(url_el, '{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod')
        if lastmod.text != TODAY:
            lastmod.text = TODAY
            changed += 1
        # Remove prior image children to avoid stale duplicate metadata.
        for child in list(url_el):
            if child.tag == '{http://www.google.com/schemas/sitemap-image/1.1}image':
                url_el.remove(child)
        img = ET.SubElement(url_el, '{http://www.google.com/schemas/sitemap-image/1.1}image')
        loc = ET.SubElement(img, '{http://www.google.com/schemas/sitemap-image/1.1}loc')
        loc.text = entry['image']
        title = ET.SubElement(img, '{http://www.google.com/schemas/sitemap-image/1.1}title')
        title.text = entry['title']
        cap = ET.SubElement(img, '{http://www.google.com/schemas/sitemap-image/1.1}caption')
        cap.text = entry['caption']
        changed += 1
    tree.write(SITEMAP, encoding='utf-8', xml_declaration=True)
    return changed


def main() -> int:
    entries=[]
    for path in sorted(BLOG_ROOT.glob('*/index.html')):
        item=enhance_article(path)
        if item:
            entries.append(item)
    changed_sitemap=update_sitemap(entries)
    print(f"Enhanced {len(entries)} article files; sitemap updates: {changed_sitemap}")
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
