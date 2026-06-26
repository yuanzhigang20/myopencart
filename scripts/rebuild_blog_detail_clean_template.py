#!/usr/bin/env python3
from __future__ import annotations
import re, html, json
from pathlib import Path
ROOT=Path('/Users/grant/IdeaProjects/myopencart')
BLOG=ROOT/'upload/blog'
ASSETS=BLOG/'assets'
BASE='https://shoplovanest.com'
GTAG='''<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-P2LJRXN3D1"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-P2LJRXN3D1');
</script>'''
CSS=r'''
:root{--ink:#241812;--muted:#705f56;--rose:#b8796a;--cream:#fffaf5;--card:#fffdf9;--line:#eaded6;--soft:#f6ece4;--shadow:0 18px 38px rgba(52,31,22,.08)}*{box-sizing:border-box}html,body{margin:0;max-width:100%;overflow-x:hidden}body{background:var(--cream);color:var(--ink);font-family:"Avenir Next","Helvetica Neue",Arial,sans-serif;line-height:1.72}.container{max-width:1220px;margin:0 auto;padding:0 20px}a{color:#704437}.privacy-bar{background:#21120d;color:#fff7ef;font-size:12px;font-weight:700}.privacy-bar .container{min-height:38px;display:flex;gap:12px;align-items:center;justify-content:center;flex-wrap:wrap}.site-header{position:sticky;top:0;z-index:10;background:rgba(255,250,245,.97);border-bottom:1px solid var(--line);backdrop-filter:blur(14px)}.nav{min-height:84px;display:flex;align-items:center;gap:24px}.brand{text-decoration:none;color:var(--ink);min-width:190px}.brand b{font:700 28px Georgia,serif;display:block;letter-spacing:.02em}.brand span{font-size:9px;font-weight:900;letter-spacing:.34em;margin-left:10px}.nav-links{display:flex;gap:22px;align-items:center;flex:1;justify-content:center}.nav-links a{font-size:13px;font-weight:800;text-decoration:none;color:#30231e}.search{width:220px;border:1px solid var(--line);border-radius:999px;background:white;min-height:38px;padding:0 14px}.cart{font-weight:900;text-decoration:none}.menu-btn{display:none}.blog-shell{max-width:1040px;margin:0 auto;padding:34px 20px 70px}.breadcrumb{font-size:13px;color:var(--muted);margin-bottom:22px}.breadcrumb a{text-decoration:none;font-weight:800}.article-head{background:linear-gradient(135deg,#fffdf9,#f4e3d9);border:1px solid var(--line);border-radius:22px;padding:clamp(22px,4vw,42px);box-shadow:var(--shadow);margin-bottom:30px}.kicker{font-size:12px;text-transform:uppercase;letter-spacing:.13em;color:var(--rose);font-weight:900}.article-head h1{font:700 clamp(2.15rem,5.2vw,4.3rem)/.98 Georgia,serif;letter-spacing:-.045em;margin:10px 0 16px}.summary{max-width:820px;font-size:18px;color:var(--muted);margin:0}.meta{display:flex;gap:12px;flex-wrap:wrap;color:#8b7a70;font-size:13px;margin:16px 0 22px}.hero{width:100%;aspect-ratio:16/9;object-fit:cover;border-radius:18px;border:1px solid var(--line);box-shadow:var(--shadow);background:#f0ded4}.lede{font-size:18px;background:#fff;border:1px solid var(--line);border-radius:18px;padding:22px;margin:24px 0;color:#4d3d36}.content-card{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:clamp(18px,3vw,30px);box-shadow:0 10px 28px rgba(60,39,29,.045);margin:24px 0}.content-card h2{font:700 28px/1.15 Georgia,serif;margin:0 0 14px;color:var(--ink)}.content-card h3{font-size:19px;margin:22px 0 8px}.content-card p,.content-card li{color:#4f4039}.content-card p:last-child,.content-card ul:last-child{margin-bottom:0}.checklist{background:#fff8f4;border:1px solid var(--line);border-radius:16px;padding:18px}.checklist li{margin:8px 0}.figure{margin:28px 0}.figure img{width:100%;aspect-ratio:16/9;object-fit:cover;border-radius:18px;border:1px solid var(--line);box-shadow:var(--shadow);background:#f0ded4}.figure figcaption{font-size:13px;color:var(--muted);margin-top:8px}table{width:100%;border-collapse:separate;border-spacing:0;overflow:hidden;border:1px solid var(--line);border-radius:15px;background:white;display:block;overflow-x:auto}th,td{padding:13px 14px;border-bottom:1px solid var(--line);border-right:1px solid var(--line);vertical-align:top}th{background:#f3e9e2}.cta{background:linear-gradient(135deg,#2a1912,#805747);color:white;border-radius:20px;padding:26px;margin:30px 0}.cta h2{font:700 28px Georgia,serif;margin:0 0 8px}.cta p{color:#f7eee7}.btn-row{display:flex;gap:12px;flex-wrap:wrap;margin-top:16px}.btn{display:inline-flex;align-items:center;justify-content:center;min-height:42px;border-radius:999px;background:#fff;color:#2a1912!important;text-decoration:none;font-weight:900;padding:0 18px}.related-links,.related-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}.related-links a,.related-card{background:#fffaf7;border:1px solid var(--line);border-radius:14px;padding:15px;text-decoration:none;color:#3a281f}.footer{background:var(--soft);border-top:1px solid var(--line);padding:44px 0;color:#6f6159}.footer-grid{display:grid;grid-template-columns:2fr 1fr 1fr 1.6fr;gap:28px}.footer h5,.footer b{color:var(--ink)}.footer a{display:block;text-decoration:none;color:#6f6159;margin:6px 0;font-size:13px}@media(max-width:860px){.nav{min-height:auto;padding:16px 0;flex-wrap:wrap}.nav-links{order:3;width:100%;justify-content:flex-start;overflow-x:auto;padding-bottom:6px}.search{width:100%}.footer-grid,.related-links,.related-grid{grid-template-columns:1fr}.article-head h1{font-size:2.35rem}.privacy-bar .container{justify-content:flex-start}.blog-shell{padding:24px 16px 56px}.container{padding:0 16px}}
'''
HEADER='''<div class="privacy-bar"><div class="container"><span>18+ Only</span><span>·</span><span>Discreet Packaging</span><span>·</span><span>Private Billing</span><span>·</span><span>Secure PayPal Checkout</span></div></div><header class="site-header"><div class="container nav"><a class="brand" href="/"><b>LOVANEST</b><span>ADULT WELLNESS</span></a><nav class="nav-links"><a href="/">Home</a><a href="/index.php?route=product/search&language=en-gb&search=wellness">Shop</a><a href="/index.php?route=product/search&language=en-gb&search=Beginner%20Friendly">Categories</a><a href="/blog/">Blog</a><a href="/index.php?route=information/information&language=en-gb&information_id=4">About</a><a href="/index.php?route=information/contact">Contact</a></nav><form action="/index.php" method="get"><input type="hidden" name="route" value="product/search"><input type="hidden" name="language" value="en-gb"><input class="search" name="search" placeholder="Search products..."></form><a class="cart" href="/index.php?route=checkout/cart&language=en-gb">Cart</a></div></header>'''
FOOTER='''<footer class="footer"><div class="container footer-grid"><div><b>LOVANEST Adult Wellness</b><p>Private, body-aware intimate wellness shopping for adults 18+. Discreet packaging, calm education, and secure checkout.</p></div><div><h5>Shop</h5><a href="/index.php?route=product/search&language=en-gb&search=wellness">All Products</a><a href="/index.php?route=product/search&language=en-gb&search=Beginner%20Friendly">Beginner Friendly</a><a href="/index.php?route=product/search&language=en-gb&search=Care">Accessories & Care</a></div><div><h5>Learn</h5><a href="/blog/">Blog</a><a href="/index.php?route=information/contact">Contact</a><a href="/index.php?route=information/information&language=en-gb&information_id=4">About</a></div><div><h5>Policies & Payment</h5><a href="/index.php?route=information/information&language=en-gb&information_id=6">Shipping Policy</a><a href="/index.php?route=account/returns.add&language=en-gb">Return Policy</a><a href="/index.php?route=information/information&language=en-gb&information_id=3">Privacy Policy</a><a href="/index.php?route=information/information&language=en-gb&information_id=5">Terms of Service</a><p>PayPal secure checkout · © 2026 Lovanest</p></div></div></footer>'''

def text(x): return html.unescape(re.sub('<[^>]+>','',x or '')).strip()
def title_desc_cat(old, slug):
    m=re.search(r'<h1[^>]*>(.*?)</h1>',old,re.S|re.I); title=text(m.group(1)) if m else slug.replace('-',' ').title()
    m=re.search(r'<meta name="description" content="([^"]*)"',old,re.I); desc=html.unescape(m.group(1)) if m else ''
    if not desc:
        m=re.search(r'<p class="(?:article-summary|lede)">(.*?)</p>',old,re.S|re.I); desc=text(m.group(1)) if m else 'A private ShopLovaNest adult wellness guide.'
    m=re.search(r'<p class="article-category">(.*?)</p>',old,re.S|re.I); cat=text(m.group(1)) if m else 'Adult Wellness Guide'
    return title,desc,cat

def extract_content(old):
    # Prefer content from inner original article after first article-head if possible.
    m=re.search(r'</header>(.*?)(?:<aside class="end-cta"|<section><h2>Related Articles|</article>)',old,re.S|re.I)
    body=m.group(1) if m else old
    body=re.sub(r'<figure class="inline-figure">.*?</figure>','',body,flags=re.S|re.I)
    body=re.sub(r'<aside class="mid-cta">.*?</aside>','',body,flags=re.S|re.I)
    body=re.sub(r'<div class="lede-card">(.*?)</div>',r'<p class="lede">\1</p>',body,flags=re.S|re.I)
    return body

def normalize_sections(body):
    lede=''
    m=re.search(r'<p class="lede">(.*?)</p>|<div class="lede-card">(.*?)</div>',body,re.S|re.I)
    if m:
        lede=m.group(1) or m.group(2)
        body=body[:m.start()]+body[m.end():]
    sections=[]
    for m in re.finditer(r'<section[^>]*>(.*?)</section>',body,re.S|re.I):
        inner=m.group(1)
        if 'related-grid' in inner: continue
        sections.append(inner.strip())
    if not sections:
        # split by h2 fallback
        parts=re.split(r'(?=<h2)',body)
        sections=[p.strip() for p in parts if '<h2' in p]
    cleaned=[]
    for s in sections:
        s=re.sub(r'class="article-content-card"','',s)
        s=re.sub(r'<section[^>]*>|</section>','',s)
        s=s.strip()
        if s: cleaned.append(s)
    return lede, cleaned

def related(slug):
    allp=sorted([p.parent.name for p in BLOG.glob('*/index.html') if p.parent.name!='assets'])
    rel=[s for s in allp if s!=slug][:6]
    return ''.join(f'<a class="related-card" href="/blog/{r}/"><b>{html.escape(r.replace("-"," ").title())}</b></a>' for r in rel)

def render(slug,title,desc,cat,lede,sections):
    cover=f'/blog/assets/{slug}-cover.svg'
    guide=f'/blog/assets/{slug}-guide-1.svg'
    detail=f'/blog/assets/{slug}-detail-1.svg'
    cards=[]
    for i,s in enumerate(sections):
        cards.append(f'<section class="content-card">{s}</section>')
        if i==0: cards.append(f'<figure class="figure"><img loading="lazy" src="{guide}" alt="{html.escape(title)} guide visual" width="1600" height="900"><figcaption>Visual checklist matched to this guide topic.</figcaption></figure>')
        if i==3: cards.append(f'<figure class="figure"><img loading="lazy" src="{detail}" alt="{html.escape(title)} detail visual" width="1600" height="900"><figcaption>Product detail and privacy cues for this article.</figcaption></figure>')
        if i==1: cards.append('<aside class="cta"><h2>Shop privately with context</h2><p>Use this guide to compare products, privacy, materials, care, and checkout before buying.</p><div class="btn-row"><a class="btn" href="/index.php?route=product/search&language=en-gb&search=wellness">Shop Related Products</a><a class="btn" href="/blog/">Back to Blog</a></div></aside>')
    return f'''<!doctype html><html lang="en"><head>{GTAG}<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc)}"><meta name="rating" content="adult"><link rel="canonical" href="{BASE}/blog/{slug}/"><style>{CSS}</style></head><body>{HEADER}<main class="blog-shell"><article class="blog-article"><nav class="breadcrumb"><a href="/">Home</a> &gt; <a href="/blog/">Blog</a> &gt; <span>{html.escape(title)}</span></nav><header class="article-head"><div class="kicker">{html.escape(cat)}</div><h1>{html.escape(title)}</h1><p class="summary">{html.escape(desc)}</p><div class="meta"><span>2026-06-26</span><span>6 min read</span><span>ShopLovaNest Editorial Team</span></div><img class="hero" src="{cover}" alt="{html.escape(title)} cover image" width="1600" height="900" fetchpriority="high"></header>{f'<div class="lede">{lede}</div>' if lede else ''}{''.join(cards)}<aside class="cta"><h2>Continue shopping privately</h2><p>Explore customer favorites, compare options, or return to the education hub.</p><div class="btn-row"><a class="btn" href="/index.php?route=product/search&language=en-gb&search=wellness">View All Products</a><a class="btn" href="/blog/">Explore More Guides</a></div></aside><section class="content-card"><h2>Related Articles</h2><div class="related-grid">{related(slug)}</div></section></article></main>{FOOTER}</body></html>'''

for p in sorted(BLOG.glob('*/index.html')):
    if p.parent.name=='assets': continue
    slug=p.parent.name; old=p.read_text(errors='ignore')
    title,desc,cat=title_desc_cat(old,slug)
    lede,sections=normalize_sections(extract_content(old))
    if len(sections)<3:
        # preserve at least a readable shell
        sections=[f'<h2>Guide Overview</h2><p>{html.escape(desc)}</p>', '<h2>What to Check</h2><p>Compare product details, privacy, materials, care guidance, and support before checkout.</p>', '<h2>Bottom Line</h2><p>Choose transparent listings and simple routines that fit your privacy and comfort needs.</p>']
    p.write_text(render(slug,title,desc,cat,lede,sections),encoding='utf-8')
print('rebuilt', len(list(BLOG.glob('*/index.html'))))
