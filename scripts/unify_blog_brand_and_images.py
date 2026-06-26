#!/usr/bin/env python3
from __future__ import annotations
import json, re, html, math
from pathlib import Path
from datetime import date

ROOT = Path('/Users/grant/IdeaProjects/myopencart')
BLOG = ROOT / 'upload' / 'blog'
ASSETS = BLOG / 'assets'
OUT = ROOT / 'output'
BASE = 'https://shoplovanest.com'
TODAY = '2026-06-26'
ASSETS.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)

GTAG_ID = 'G-P2LJRXN3D1'
GTAG = '''<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-P2LJRXN3D1"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-P2LJRXN3D1');
</script>'''

HEADER = '''<div class="privacy-bar" aria-label="Store privacy and safety promises"><div class="container"><span>18+ Only</span><span>·</span><span>Discreet Packaging</span><span>·</span><span>Private Billing</span><span>·</span><span>Secure PayPal Checkout</span></div></div>
<header class="site-header">
  <nav class="navbar navbar-expand-lg" aria-label="Main navigation">
    <div class="container">
      <a class="navbar-brand" href="/" aria-label="Lovanest home"><span class="brand-word">LOVANEST</span><span class="brand-sub">ADULT WELLNESS</span></a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#mainNav" aria-controls="mainNav" aria-expanded="false" aria-label="Toggle navigation"><span class="navbar-toggler-icon"></span></button>
      <div class="collapse navbar-collapse" id="mainNav">
        <ul class="navbar-nav mx-auto mb-2 mb-lg-0">
          <li class="nav-item"><a class="nav-link" href="/">Home</a></li>
          <li class="nav-item"><a class="nav-link" href="/index.php?route=product/search&language=en-gb&search=wellness">Shop</a></li>
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">Categories</a>
            <ul class="dropdown-menu">
              <li><a class="dropdown-item fw-semibold" href="/index.php?route=product/search&language=en-gb&search=Beginner%20Friendly">Beginner Friendly</a></li>
              <li><a class="dropdown-item fw-semibold" href="/index.php?route=product/search&language=en-gb&search=Quiet%20Discreet">Quiet &amp; Discreet</a></li>
              <li><a class="dropdown-item fw-semibold" href="/index.php?route=product/search&language=en-gb&search=Lingerie%20Sleepwear">Lingerie &amp; Sleepwear</a></li>
              <li><a class="dropdown-item fw-semibold" href="/index.php?route=product/search&language=en-gb&search=Couples">Couples Essentials</a></li>
              <li><a class="dropdown-item fw-semibold" href="/index.php?route=product/search&language=en-gb&search=App%20Controlled">App-Controlled Toys</a></li>
              <li><a class="dropdown-item fw-semibold" href="/index.php?route=product/search&language=en-gb&search=Care">Accessories &amp; Care</a></li>
            </ul>
          </li>
          <li class="nav-item"><a class="nav-link" href="/blog/">Blog</a></li>
          <li class="nav-item"><a class="nav-link" href="/index.php?route=information/information&language=en-gb&information_id=4">About</a></li>
          <li class="nav-item"><a class="nav-link" href="/index.php?route=information/contact">Contact</a></li>
        </ul>
        <form class="header-search" action="/index.php" method="get" role="search">
          <input type="hidden" name="route" value="product/search"><input type="hidden" name="language" value="en-gb">
          <input class="form-control" name="search" placeholder="Search products..." aria-label="Search private wellness products">
        </form>
        <div class="d-flex gap-2 header-actions ms-lg-3">
          <a class="header-icon-link" href="/index.php?route=account/login&language=en-gb"><i class="fa-regular fa-user"></i> Login</a>
          <a class="cart-link" href="/index.php?route=checkout/cart&language=en-gb" aria-label="Cart"><i class="fa-solid fa-cart-shopping"></i><span class="cart-dot">0</span></a>
        </div>
      </div>
    </div>
  </nav>
</header>'''

FOOTER = '''<footer class="footer mt-auto">
  <div class="container">
    <div class="row g-4">
      <div class="col-lg-3"><div class="brand-footer-title">About Lovanest</div><p class="responsible-note mb-0">Lovanest Adult Wellness curates intimate essentials with privacy-first service, discreet packaging, and calm educational guidance for adults 18+.</p><div class="footer-social" aria-label="Social links"><a href="#" aria-label="Facebook"><i class="fa-brands fa-facebook-f"></i></a><a href="#" aria-label="Instagram"><i class="fa-brands fa-instagram"></i></a><a href="#" aria-label="Pinterest"><i class="fa-brands fa-pinterest-p"></i></a></div></div>
      <div class="col-6 col-lg-2 offset-lg-1"><h5>Shop</h5><ul class="list-unstyled mb-0"><li><a href="/index.php?route=product/search&language=en-gb&search=wellness">All Products</a></li><li><a href="/index.php?route=product/search&language=en-gb&search=Beginner%20Friendly">Beginner Friendly</a></li><li><a href="/index.php?route=product/search&language=en-gb&search=Quiet%20Discreet">Quiet &amp; Discreet</a></li><li><a href="/index.php?route=product/search&language=en-gb&search=Care">Accessories &amp; Care</a></li></ul></div>
      <div class="col-6 col-lg-2"><h5>Customer Service</h5><ul class="list-unstyled mb-0"><li><a href="/blog/">Blog</a></li><li><a href="/index.php?route=information/contact">Contact</a></li><li><a href="/index.php?route=information/information&language=en-gb&information_id=6">Shipping Policy</a></li><li><a href="/index.php?route=account/returns.add&language=en-gb">Return Policy</a></li><li><a href="/index.php?route=information/information&language=en-gb&information_id=3">Privacy Policy</a></li><li><a href="/index.php?route=information/information&language=en-gb&information_id=5">Terms of Service</a></li></ul></div>
      <div class="col-lg-3 offset-lg-1"><h5>Secure Payment</h5><p class="responsible-note mb-2"><i class="fa-brands fa-paypal"></i> PayPal-friendly secure checkout · encrypted storefront pages · discreet order handling.</p><p class="responsible-note mb-0">© 2026 Lovanest Adult Wellness.<br>All rights reserved. 18+ only.</p></div>
    </div>
  </div>
</footer>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" defer></script>'''

SITE_CSS = r'''
:root{--lv-ink:#231813;--lv-bark:#2a1912;--lv-cocoa:#3a281f;--lv-rose:#b8796a;--lv-blush:#f2ddd5;--lv-ivory:#fffaf5;--lv-cream:#f7eee7;--lv-card:#fffdf9;--lv-muted:#75655e;--lv-line:#eaded6;--lv-shadow:0 12px 30px rgba(60,38,28,.075)}*{box-sizing:border-box}html{scroll-behavior:smooth;max-width:100%;overflow-x:hidden}body{margin:0;max-width:100%;overflow-x:hidden;background:var(--lv-ivory);color:var(--lv-ink);font-family:"Avenir Next","Helvetica Neue",Helvetica,Arial,sans-serif;font-size:14px;letter-spacing:.005em;line-height:1.72}.container{max-width:1280px}a{color:var(--lv-cocoa)}img{max-width:100%;height:auto}.privacy-bar{background:#21120d;color:#fff7ef;font-size:12px;font-weight:600;letter-spacing:.02em}.privacy-bar .container{min-height:38px;display:flex;align-items:center;justify-content:center;gap:14px;flex-wrap:wrap}.privacy-bar span:nth-child(even){opacity:.55}.site-header{background:rgba(255,250,245,.96);border-bottom:1px solid var(--lv-line);position:sticky;top:0;z-index:1030;backdrop-filter:blur(14px)}.site-header .navbar{min-height:86px;padding:0;background:transparent!important}.navbar-brand{display:flex;flex-direction:column;align-items:flex-start;line-height:1;text-decoration:none;color:var(--lv-ink)!important;min-width:188px}.brand-word{font-family:Georgia,"Times New Roman",serif;font-size:28px;font-weight:700;letter-spacing:.02em}.brand-sub{font-size:9px;font-weight:800;letter-spacing:.34em;margin-left:11px;margin-top:5px;color:#5b453b}.navbar-nav{gap:20px}.nav-link{color:#30231e!important;font-size:13px;font-weight:700;padding:.5rem .1rem!important}.nav-link:hover,.nav-link:focus{color:var(--lv-rose)!important}.dropdown-menu{border-color:var(--lv-line);border-radius:14px;box-shadow:var(--lv-shadow);padding:.65rem}.dropdown-item{border-radius:10px;font-size:13px}.header-search{width:min(245px,22vw);position:relative;background:#fff;border:1px solid var(--lv-line);border-radius:999px}.header-search:before{content:"\f002";font-family:"Font Awesome 6 Free";font-weight:900;position:absolute;left:13px;top:50%;transform:translateY(-50%);font-size:12px;color:#a6978f}.header-search .form-control{border:0;background:transparent;border-radius:999px;min-height:38px;padding-left:34px;font-size:12px;color:var(--lv-ink)}.header-search .form-control::placeholder{color:#b5a9a1}.header-icon-link{color:var(--lv-cocoa);font-size:13px;font-weight:700;text-decoration:none;display:inline-flex;align-items:center;gap:6px;min-height:38px}.cart-link{position:relative;width:38px;height:38px;border-radius:999px;color:var(--lv-cocoa);display:inline-flex;align-items:center;justify-content:center;text-decoration:none}.cart-link .cart-dot{position:absolute;right:5px;top:4px;width:17px;height:17px;border-radius:999px;background:#8c5a47;color:white;font-size:9px;display:inline-flex;align-items:center;justify-content:center;font-weight:900}.btn,.cta-button{border-radius:999px;font-weight:800;min-height:42px;display:inline-flex;align-items:center;justify-content:center;gap:.45rem;white-space:nowrap;font-size:13px;text-decoration:none}.btn-primary,.cta-button.primary{background:#2a1912;color:#fff!important;border:1px solid #2a1912;padding:0 20px}.btn-light,.cta-button.secondary{background:#fffaf7;border:1px solid var(--lv-line);color:var(--lv-cocoa)!important;padding:0 18px}.blog-shell{max-width:1180px;margin:0 auto;padding:34px 20px 68px}.blog-hero{border:1px solid var(--lv-line);border-radius:18px;background:linear-gradient(135deg,#fffdf9 0%,#f5e7de 58%,#ead4c8 100%);padding:clamp(28px,5vw,64px);box-shadow:var(--lv-shadow);overflow:hidden}.blog-hero h1,.blog-article h1{font-family:Georgia,"Times New Roman",serif;font-size:clamp(2.35rem,6vw,4.6rem);line-height:.98;letter-spacing:-.045em;color:#241914;margin:10px 0 18px}.eyebrow,.card-kicker,.article-category{display:inline-flex;align-items:center;gap:.45rem;text-transform:uppercase;letter-spacing:.12em;font-size:12px;color:var(--lv-rose);font-weight:900}.lede,.article-summary{max-width:820px;color:var(--lv-muted);font-size:clamp(1.02rem,2vw,1.18rem);line-height:1.7}.hero-actions,.cta-row{display:flex;gap:12px;flex-wrap:wrap;margin-top:22px}.trust-strip{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin-top:18px}.trust-strip span,.category-pill{background:#fffaf7;border:1px solid var(--lv-line);border-radius:999px;padding:9px 12px;font-size:12px;font-weight:800;color:var(--lv-cocoa);display:inline-flex;align-items:center;gap:7px}.section{margin-top:48px}.section-head{display:flex;align-items:end;justify-content:space-between;gap:18px;margin-bottom:18px}.section h2,.section-title{font-family:Georgia,"Times New Roman",serif;font-size:28px;font-weight:700;letter-spacing:-.03em;color:#241914;margin:0}.section-intro{max-width:760px;margin:8px 0 0;color:var(--lv-muted)}.category-filter{display:flex;flex-wrap:wrap;gap:9px}.featured-grid,.latest-grid,.related-grid,.product-category-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}.featured-grid .article-card:first-child{grid-column:span 2}.article-card,.cluster-card,.shop-cta,.newsletter-box,.tip-card,.link-card,.related-card{background:var(--lv-card);border:1px solid var(--lv-line);border-radius:14px;box-shadow:0 8px 24px rgba(60,39,29,.045);overflow:hidden}.article-card{display:flex;flex-direction:column;transition:transform .18s ease,box-shadow .18s ease}.article-card:hover{transform:translateY(-3px);box-shadow:0 15px 28px rgba(60,39,29,.09)}.article-card img{width:100%;aspect-ratio:16/9;object-fit:cover;background:#f6e9e1}.article-card-body{padding:17px;display:flex;flex-direction:column;gap:9px;flex:1}.article-card h3{font-size:18px;line-height:1.25;margin:0;color:#2a1912}.article-card p{margin:0;color:var(--lv-muted)}.article-meta{display:flex;gap:10px;flex-wrap:wrap;font-size:12px;color:#8b7a70}.read-more{margin-top:auto;color:#5b352a;font-weight:900;text-decoration:none}.product-category-grid{grid-template-columns:repeat(4,minmax(0,1fr))}.shop-cta,.newsletter-box{padding:24px;background:linear-gradient(135deg,#fffdf9,#f6ece4)}.blog-article{max-width:930px;margin:0 auto}.breadcrumb{font-size:13px;color:var(--lv-muted);margin:0 0 24px}.breadcrumb a{text-decoration:none;color:var(--lv-cocoa);font-weight:800}.article-head{margin-bottom:26px}.article-head .article-meta{margin:10px 0 20px}.article-hero-img,.inline-figure img{width:100%;border-radius:18px;border:1px solid var(--lv-line);box-shadow:var(--lv-shadow);object-fit:cover;background:#f6e9e1}.article-hero-img{aspect-ratio:16/9}.inline-figure{margin:30px 0}.inline-figure img{aspect-ratio:16/9}.inline-figure figcaption{font-size:12px;color:var(--lv-muted);margin-top:8px}.blog-article section{margin-top:34px}.blog-article h2{font-family:Georgia,"Times New Roman",serif;font-size:28px;line-height:1.15;margin:0 0 14px;padding-top:24px;border-top:1px solid var(--lv-line)}.blog-article h3{font-size:18px;line-height:1.25;margin:22px 0 8px;color:#2a1912}.blog-article p,.blog-article li{color:#4f4039}.blog-article table{width:100%;border-collapse:collapse;background:#fff;border:1px solid var(--lv-line);border-radius:14px;overflow:hidden;display:block;overflow-x:auto}.blog-article th,.blog-article td{border:1px solid var(--lv-line);padding:.75rem;text-align:left;vertical-align:top}.blog-article th{background:#f3ece7}.tip-card{padding:18px;border-left:4px solid var(--lv-rose);background:#fffaf7}.mid-cta,.end-cta{padding:24px;border-radius:18px;background:linear-gradient(135deg,#2a1912,#7a5548);color:#fff;margin:34px 0}.mid-cta p,.end-cta p{color:#f7eee7}.mid-cta .cta-button,.end-cta .cta-button{background:#fff;color:#2a1912!important}.link-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}.link-card{padding:14px}.footer{background:#f6ece4;color:#44342d;border-top:1px solid var(--lv-line);padding:46px 0!important}.footer h5{color:#241914;font-size:13px;font-weight:900;margin-bottom:14px}.footer p,.footer li,.footer a,.responsible-note{color:#6f6159;font-size:12px;line-height:1.65}.footer a{text-decoration:none}.footer a:hover{color:#241914;text-decoration:underline}.footer-social{display:flex;gap:17px;margin-top:16px}.footer-social a{width:22px;height:22px;display:inline-flex;align-items:center;justify-content:center;color:#241914}.brand-footer-title{font-family:Georgia,"Times New Roman",serif;color:#241914;font-size:18px;font-weight:700;margin-bottom:12px}@media(max-width:991.98px){.site-header .navbar{min-height:auto;padding:18px 0}.navbar-nav{gap:4px;margin-top:16px}.header-search{width:100%;margin:12px 0}.header-actions{width:100%;justify-content:space-between}.trust-strip{grid-template-columns:1fr 1fr}.featured-grid,.latest-grid,.related-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.featured-grid .article-card:first-child{grid-column:1/-1}.product-category-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.brand-word{font-size:24px}.container{--bs-gutter-x:1.1rem}}@media(max-width:680px){.blog-shell{padding:24px 16px 54px}.blog-hero{border-radius:18px}.blog-hero h1,.blog-article h1{font-size:2.45rem}.trust-strip,.featured-grid,.latest-grid,.related-grid,.product-category-grid,.link-grid{grid-template-columns:1fr}.section-head{align-items:flex-start;flex-direction:column}.article-card img{aspect-ratio:16/10}.mid-cta,.end-cta{padding:20px}.privacy-bar .container{justify-content:flex-start}}
'''

FOCUS = [
 ('sex-toys-for-beginners','sex toys for beginners'),('best-adult-toys-for-beginners','best adult toys for beginners'),('body-safe-sex-toys','body safe sex toys'),('discreet-shipping-adult-toys','discreet shipping adult toys'),('vibrators-for-beginners','vibrators for beginners'),('quiet-vibrator-guide','quiet vibrator'),('water-based-lube-guide','water based lube'),('how-to-clean-silicone-sex-toys','how to clean silicone sex toys'),('adult-toy-buying-guide','adult toy buying guide'),('rabbit-vibrator-guide','rabbit vibrator'),('male-masturbator-guide','male masturbator'),('adult-toys-for-couples','adult toys for couples')
]
FOCUS_SLUGS = {s for s,k in FOCUS}

CATEGORY_RULES = [
 ('lube','Lubricants'),('lubricant','Lubricants'),('clean','Cleaning & Care'),('storage','Storage & Privacy'),('shipping','Privacy & Delivery'),('delivery','Privacy & Delivery'),('billing','Privacy & Delivery'),('travel','Travel Privacy'),('lingerie','Lingerie'),('kegel','Pelvic Wellness'),('couples','Couples'),('vibrator','Vibrators'),('wand','Vibrators'),('rabbit','Vibrators'),('male','Male Wellness'),('material','Materials'),('body-safe','Materials'),('silicone','Materials')
]
def category_for(slug,title=''):
    s=(slug+' '+title).lower()
    for key,val in CATEGORY_RULES:
        if key in s: return val
    return 'Buying Guides'

def strip_tags(s):
    return re.sub(r'<[^>]+>','',s or '').strip()

def get_title(txt, slug):
    m=re.search(r'<h1[^>]*>(.*?)</h1>', txt, re.S|re.I)
    if m: return html.unescape(strip_tags(m.group(1)))
    m=re.search(r'<title[^>]*>(.*?)</title>', txt, re.S|re.I)
    if m: return html.unescape(strip_tags(m.group(1))).split('|')[0].strip()
    return slug.replace('-',' ').title()

def get_desc(txt):
    m=re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']*)', txt, re.I)
    if m: return html.unescape(m.group(1))
    m=re.search(r'<p class=["\'](?:lede|article-summary)["\'][^>]*>(.*?)</p>', txt, re.S|re.I)
    return html.unescape(strip_tags(m.group(1)))[:180] if m else 'A discreet ShopLovaNest adult wellness guide focused on privacy, materials, care, and confident shopping.'

def slug_words(slug): return ' '.join(slug.split('-'))

# Generate lightweight premium SVG illustrations and matching .webp copies when Pillow is available.
def make_svg(path: Path, title: str, subtitle: str, ratio='16:9'):
    w,h=(1600,900) if ratio=='16:9' else (1200,900)
    safe_title=html.escape(title[:52])
    safe_sub=html.escape(subtitle[:72])
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{safe_title}">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fffaf5"/><stop offset="0.55" stop-color="#f1ded4"/><stop offset="1" stop-color="#d8b9aa"/></linearGradient><radialGradient id="r" cx="68%" cy="35%" r="55%"><stop offset="0" stop-color="#ffffff" stop-opacity=".82"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></radialGradient><filter id="shadow"><feDropShadow dx="0" dy="18" stdDeviation="24" flood-color="#3c261c" flood-opacity=".18"/></filter></defs>
<rect width="100%" height="100%" fill="url(#g)"/><rect width="100%" height="100%" fill="url(#r)"/>
<circle cx="{int(w*.78)}" cy="{int(h*.25)}" r="{int(h*.2)}" fill="#fffdf9" opacity=".52"/>
<circle cx="{int(w*.62)}" cy="{int(h*.68)}" r="{int(h*.28)}" fill="#b8796a" opacity=".18"/>
<rect x="{int(w*.56)}" y="{int(h*.2)}" width="{int(w*.26)}" height="{int(h*.48)}" rx="46" fill="#fffdf9" opacity=".88" filter="url(#shadow)"/>
<path d="M {int(w*.60)} {int(h*.58)} C {int(w*.66)} {int(h*.48)}, {int(w*.74)} {int(h*.48)}, {int(w*.79)} {int(h*.58)}" fill="none" stroke="#b8796a" stroke-width="12" stroke-linecap="round" opacity=".52"/>
<rect x="{int(w*.12)}" y="{int(h*.18)}" width="{int(w*.38)}" height="{int(h*.54)}" rx="36" fill="#fffdf9" opacity=".82" filter="url(#shadow)"/>
<text x="{int(w*.16)}" y="{int(h*.31)}" font-family="Georgia, serif" font-size="{int(h*.07)}" font-weight="700" fill="#241914">Lovanest</text>
<text x="{int(w*.16)}" y="{int(h*.40)}" font-family="Arial, sans-serif" font-size="{int(h*.035)}" font-weight="700" letter-spacing="3" fill="#7a5548">ADULT WELLNESS GUIDE</text>
<foreignObject x="{int(w*.16)}" y="{int(h*.47)}" width="{int(w*.31)}" height="{int(h*.18)}"><div xmlns="http://www.w3.org/1999/xhtml" style="font-family:Georgia,serif;font-size:{int(h*.052)}px;line-height:1.08;color:#2a1912;font-weight:700">{safe_title}</div></foreignObject>
<text x="{int(w*.16)}" y="{int(h*.70)}" font-family="Arial, sans-serif" font-size="{int(h*.032)}" fill="#75655e">{safe_sub}</text>
</svg>'''
    path.write_text(svg, encoding='utf-8')
    webp=path.with_suffix('.webp')
    try:
        from PIL import Image, ImageDraw, ImageFont
        im=Image.new('RGB',(w,h),'#f1ded4')
        draw=ImageDraw.Draw(im)
        for y in range(h):
            r=int(255-(y/h)*38); g=int(250-(y/h)*48); b=int(245-(y/h)*65)
            draw.line([(0,y),(w,y)],fill=(r,g,b))
        draw.ellipse((int(w*.58),int(h*.08),int(w*.98),int(h*.58)),fill=(255,253,249))
        draw.ellipse((int(w*.54),int(h*.47),int(w*.92),int(h*.95)),fill=(216,185,170))
        draw.rounded_rectangle((int(w*.10),int(h*.16),int(w*.52),int(h*.76)),radius=40,fill=(255,253,249),outline=(234,222,214),width=3)
        draw.rounded_rectangle((int(w*.58),int(h*.22),int(w*.83),int(h*.70)),radius=48,fill=(255,250,245),outline=(234,222,214),width=3)
        try:
            font_big=ImageFont.truetype('/System/Library/Fonts/Supplemental/Georgia.ttf', int(h*.075))
            font_mid=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', int(h*.034))
            font_title=ImageFont.truetype('/System/Library/Fonts/Supplemental/Georgia.ttf', int(h*.052))
            font_small=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', int(h*.032))
        except Exception:
            font_big=font_mid=font_title=font_small=None
        draw.text((int(w*.14),int(h*.24)),'Lovanest',fill=(36,25,20),font=font_big)
        draw.text((int(w*.14),int(h*.36)),'ADULT WELLNESS GUIDE',fill=(122,85,72),font=font_mid)
        words=title.split(); lines=[]; line=''
        for word in words:
            test=(line+' '+word).strip()
            if len(test)>24 and line:
                lines.append(line); line=word
            else: line=test
        if line: lines.append(line)
        y=int(h*.45)
        for ln in lines[:3]:
            draw.text((int(w*.14),y),ln,fill=(42,25,18),font=font_title); y+=int(h*.065)
        draw.text((int(w*.14),int(h*.70)),subtitle[:68],fill=(117,101,94),font=font_small)
        im.save(webp, 'WEBP', quality=82, method=6)
    except Exception:
        # Keep SVG as fallback; HTML still references SVG if WEBP was not created.
        pass
    return webp if webp.exists() else path

image_plan=[]
for slug, kw in FOCUS:
    title = slug.replace('-',' ').title()
    p = BLOG/slug/'index.html'
    if p.exists(): title=get_title(p.read_text(errors='ignore'),slug)
    items=[
        ('cover','article hero','16:9',f'{slug}-cover',f'{title} cover image with discreet Lovanest adult wellness styling',f'Premium ecommerce editorial hero image for ShopLovaNest adult wellness article "{title}". Warm ivory, cocoa, blush palette, discreet abstract product silhouettes, plain packaging, clean DTC brand style, no explicit anatomy, no vulgar content, high-end female-friendly intimate wellness aesthetic.'),
        ('guide-1','after first H2','16:9',f'{slug}-guide-1',f'Discreet shopping checklist for {kw}',f'Editorial flat-lay illustration for {kw}: checklist card, neutral packaging, soft blush and ivory background, calm private shopping mood, ecommerce blog image, no explicit content.'),
        ('detail-1','middle of article','16:9',f'{slug}-detail-1',f'Care and product detail illustration for {kw}',f'Clean product-care detail image for {kw}: soft cloth, storage pouch, care card, subtle wellness accessory silhouette, warm premium DTC lighting, discreet and non-explicit.')
    ]
    inline=[]
    for role,pos,ratio,stem,alt,prompt in items:
        out=make_svg(ASSETS/(stem+'.svg'), title if role=='cover' else kw.title(), 'Private · Body-safe · Discreet', ratio)
        rel='/blog/assets/'+out.name
        if role=='cover':
            cover={'position':pos,'ratio':ratio,'filename':out.name,'alt':alt,'prompt':prompt,'src':rel}
        else:
            inline.append({'position':pos,'ratio':ratio,'filename':out.name,'alt':alt,'prompt':prompt,'src':rel})
    image_plan.append({'slug':slug,'title':title,'main_keyword':kw,'cover_image':cover,'inline_images':inline})

PLAN_PATH = OUT / f'blog_image_plan_{TODAY}.json'
PLAN_PATH.write_text(json.dumps(image_plan, ensure_ascii=False, indent=2), encoding='utf-8')
plan_by_slug={x['slug']:x for x in image_plan}

# collect all articles metadata before rewriting
articles=[]
for p in sorted(BLOG.glob('*/index.html')):
    if p.parent.name=='assets': continue
    txt=p.read_text(encoding='utf-8', errors='ignore')
    slug=p.parent.name
    title=get_title(txt,slug)
    desc=get_desc(txt)
    cat=category_for(slug,title)
    articles.append({'slug':slug,'title':title,'desc':desc,'cat':cat,'date':'2026-06-26' if slug in ['body-safe-sex-toys','how-to-dry-adult-toys','anal-toys-for-beginners','tsa-adult-toys-travel-guide','adult-toy-privacy-guide','app-controlled-adult-toys','sex-toys-for-beginners'] else '2026-06-25'})

# order focus first for featured
focus_order=[s for s,k in FOCUS]
articles_sorted=sorted(articles, key=lambda a: (focus_order.index(a['slug']) if a['slug'] in focus_order else 999, a['title']))

def bootstrap_head(txt):
    # Normalize gtag to one instance immediately after <head>.
    txt=re.sub(r'<!-- Google tag \(gtag\.js\) -->\s*<script async src="https://www\.googletagmanager\.com/gtag/js\?id=G-P2LJRXN3D1"></script>\s*<script>.*?gtag\(\'config\', \'G-P2LJRXN3D1\'\);\s*</script>','',txt,flags=re.S)
    txt=re.sub(r'<head>\s*', '<head>\n'+GTAG+'\n', txt, count=1, flags=re.I)
    # remove old inline style blocks to avoid conflicting old blog header/footer styles
    txt=re.sub(r'\s*<style>.*?</style>','',txt,flags=re.S|re.I)
    libs='''
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css" rel="stylesheet">
  <style>'''+SITE_CSS+'</style>\n'
    txt=re.sub(r'</head>', libs+'</head>', txt, count=1, flags=re.I)
    return txt

def replace_header_footer(txt):
    # body header replacement: from <body...> to first <main or <article
    txt=re.sub(r'<body[^>]*>\s*<header.*?</header>\s*', '<body class="d-flex flex-column min-vh-100">\n'+HEADER+'\n', txt, count=1, flags=re.S|re.I)
    if '<body' in txt and 'privacy-bar' not in txt:
        txt=re.sub(r'<body[^>]*>', '<body class="d-flex flex-column min-vh-100">\n'+HEADER, txt, count=1, flags=re.I)
    txt=re.sub(r'\s*<footer.*?</footer>\s*(?=</body>)', '\n'+FOOTER+'\n', txt, count=1, flags=re.S|re.I)
    if '<footer' not in txt:
        txt=txt.replace('</body>', FOOTER+'\n</body>')
    return txt

def article_related(slug):
    cur=next((a for a in articles_sorted if a['slug']==slug), None)
    same=[a for a in articles_sorted if a['slug']!=slug and cur and a['cat']==cur['cat']]
    rest=[a for a in articles_sorted if a['slug']!=slug and a not in same]
    return (same+rest)[:6]

def img_for_card(a):
    if a['slug'] in plan_by_slug: return plan_by_slug[a['slug']]['cover_image']['src']
    # deterministic fallback to existing hub image or generated focus cover
    return '/blog/assets/sexual-wellness-education-hub.jpg'

def build_index():
    cats=[]
    for a in articles_sorted:
        if a['cat'] not in cats: cats.append(a['cat'])
    featured=articles_sorted[:6]
    latest=articles_sorted[6:]
    def card(a, featured=False):
        return f'''<article class="article-card"><a href="/blog/{a['slug']}/"><img loading="lazy" src="{img_for_card(a)}" alt="{html.escape(a['title'])} cover image"></a><div class="article-card-body"><p class="card-kicker">{html.escape(a['cat'])}</p><h3><a href="/blog/{a['slug']}/">{html.escape(a['title'])}</a></h3><p>{html.escape(a['desc'][:165])}</p><div class="article-meta"><span>{a['date']}</span><span>6 min read</span></div><a class="read-more" href="/blog/{a['slug']}/">Read More →</a></div></article>'''
    cat_html=''.join(f'<a class="category-pill" href="#cat-{re.sub(r"[^a-z0-9]+","-",c.lower()).strip("-")}">{html.escape(c)}</a>' for c in cats)
    featured_html=''.join(card(a, True) for a in featured)
    latest_html=''.join(card(a) for a in latest)
    shop_html=''.join(f'''<a class="link-card" href="{u}"><strong>{t}</strong><br><span>{d}</span></a>''' for t,u,d in [
        ('Beginner Friendly','/index.php?route=product/search&language=en-gb&search=Beginner%20Friendly','Simple first picks and calm buying guidance.'),
        ('Quiet & Discreet','/index.php?route=product/search&language=en-gb&search=Quiet%20Discreet','Privacy-minded essentials for shared homes.'),
        ('Lingerie & Sleepwear','/index.php?route=product/search&language=en-gb&search=Lingerie%20Sleepwear','Soft, confidence-first intimate styling.'),
        ('Accessories & Care','/index.php?route=product/search&language=en-gb&search=Care','Cleaning, storage, lubricant, and aftercare support.'),
    ])
    ld={"@context":"https://schema.org","@type":"ItemList","name":"ShopLovaNest Sexual Wellness Guides","url":BASE+'/blog/',"numberOfItems":len(articles_sorted),"itemListElement":[{"@type":"ListItem","position":i+1,"url":f"{BASE}/blog/{a['slug']}/","name":a['title']} for i,a in enumerate(articles_sorted)]}
    return f'''<!doctype html>
<html lang="en"><head>
{GTAG}
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sexual Wellness Guides | ShopLovaNest Blog</title><meta name="description" content="{len(articles_sorted)} discreet, adult-only sexual wellness guides with shopping links, privacy tips, materials, cleaning, storage, lubricant, and product advice.">
<meta name="rating" content="adult"><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{BASE}/blog/">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet"><link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css" rel="stylesheet"><style>{SITE_CSS}</style></head>
<body class="d-flex flex-column min-vh-100">
{HEADER}
<main class="blog-shell">
<section class="blog-hero"><p class="eyebrow">18+ EDUCATION HUB</p><h1>Sexual Wellness Guides</h1><p class="lede">Private, mature, product-aware guides for intimate wellness shopping. Learn about body-safe materials, discreet delivery, cleaning, storage, lubricant compatibility, and beginner-friendly product choices — all inside the same Lovanest shopping experience.</p><div class="hero-actions"><a class="cta-button primary" href="/index.php?route=product/search&language=en-gb&search=wellness">Explore Best Sellers</a><a class="cta-button secondary" href="/index.php?route=product/search&language=en-gb&search=New%20Arrivals">Shop New Arrivals</a><a class="cta-button secondary" href="/">View All Products</a></div><div class="trust-strip"><span><i class="fa-solid fa-box"></i> Discreet packaging</span><span><i class="fa-brands fa-paypal"></i> Secure PayPal checkout</span><span><i class="fa-solid fa-user-shield"></i> 18+ private shopping</span><span><i class="fa-solid fa-heart"></i> Female-friendly guidance</span></div></section>
<section class="section"><div class="section-head"><div><h2>Browse by Topic</h2><p class="section-intro">Filter by intent, then continue naturally to relevant products or support pages.</p></div></div><div class="category-filter">{cat_html}</div></section>
<section class="section"><div class="section-head"><div><h2>Featured Articles</h2><p class="section-intro">High-conversion, high-intent education pages for beginner decisions, privacy questions, and material safety.</p></div></div><div class="featured-grid">{featured_html}</div></section>
<section class="section"><div class="section-head"><div><h2>Recommended Shopping Paths</h2><p class="section-intro">Article readers can immediately return to the store without feeling they left the ecommerce site.</p></div></div><div class="product-category-grid">{shop_html}</div></section>
<section class="section"><div class="section-head"><div><h2>All Guides</h2><p class="section-intro">Each card includes title, category, date, reading time, summary, and a clear read-more action.</p></div></div><div class="latest-grid">{latest_html}</div></section>
<section class="section"><div class="newsletter-box"><h2>Private shopping notes, not noisy marketing</h2><p>Join the newsletter from your account area for discreet product guidance, care tips, and privacy-first shopping updates.</p><div class="cta-row"><a class="cta-button primary" href="/index.php?route=account/newsletter&language=en-gb">Newsletter Settings</a><a class="cta-button secondary" href="/index.php?route=information/contact">Ask a Private Question</a></div></div></section>
</main>
{FOOTER}
</body></html>'''

(BLOG/'index.html').write_text(build_index(), encoding='utf-8')

# Rewrite all articles header/footer/style; enhance focus pages with images/CTA/related.
for a in articles_sorted:
    p=BLOG/a['slug']/'index.html'
    txt=p.read_text(encoding='utf-8', errors='ignore')
    title=a['title']; desc=a['desc']; cat=a['cat']
    txt=bootstrap_head(txt)
    txt=replace_header_footer(txt)
    txt=re.sub(r'<main[^>]*>', '<main class="blog-shell">', txt, count=1, flags=re.I)
    # add article structural classes if missing
    txt=re.sub(r'<article class="blog-article">', '<article class="blog-article">', txt, count=1)
    if '<article class="blog-article">' not in txt:
        txt=txt.replace('<main class="blog-shell">','<main class="blog-shell">\n<article class="blog-article">',1).replace('</main>','</article>\n</main>',1)
    # Replace old simple article preamble: insert breadcrumb/article head before first h1 if no article-head.
    if 'class="article-head"' not in txt:
        plan=plan_by_slug.get(a['slug'])
        cover_html=''
        if plan:
            c=plan['cover_image']; cover_html=f'<img class="article-hero-img" src="{c["src"]}" alt="{html.escape(c["alt"])}" width="1600" height="900" fetchpriority="high">'
        head=f'''<nav class="breadcrumb" aria-label="Breadcrumb"><a href="/">Home</a> &gt; <a href="/blog/">Blog</a> &gt; <span>{html.escape(title)}</span></nav>
<header class="article-head"><p class="article-category">{html.escape(cat)}</p>'''
        # Move h1 into header by replacing first h1 start area
        txt=re.sub(r'<article class="blog-article">\s*', '<article class="blog-article">\n'+head+'\n', txt, count=1)
        # after first h1 add summary/meta/cover and close header, remove duplicate leading eyebrow if immediately after header possible
        meta=f'''<p class="article-summary">{html.escape(desc)}</p><div class="article-meta"><span>{a['date']}</span><span>6 min read</span><span>ShopLovaNest Editorial Team</span></div>{cover_html}</header>'''
        txt=re.sub(r'(</h1>)', r'\1\n'+meta, txt, count=1, flags=re.I)
        # remove old top eyebrow if left before h1 in header
        txt=re.sub(r'(<header class="article-head"><p class="article-category">.*?</p>)\s*<p class="eyebrow">.*?</p>\s*', r'\1\n', txt, count=1, flags=re.S)
    # Add CTA after second section if not present
    if 'class="mid-cta"' not in txt:
        mid=f'''<aside class="mid-cta"><h2>Ready to shop with privacy in mind?</h2><p>Explore Lovanest product paths that match this guide, with discreet packaging and secure PayPal-friendly checkout.</p><div class="cta-row"><a class="cta-button" href="/index.php?route=product/search&language=en-gb&search={html.escape(cat)}">Shop Related Products</a><a class="cta-button" href="/index.php?route=product/search&language=en-gb&search=Beginner%20Friendly">Browse Customer Favorites</a></div></aside>'''
        matches=list(re.finditer(r'</section>', txt, flags=re.I))
        if len(matches)>=2:
            pos=matches[1].end(); txt=txt[:pos]+mid+txt[pos:]
    # Focus inline images
    if a['slug'] in plan_by_slug and 'class="inline-figure"' not in txt:
        imgs=plan_by_slug[a['slug']]['inline_images']
        fig1=f'''<figure class="inline-figure"><img loading="lazy" src="{imgs[0]['src']}" alt="{html.escape(imgs[0]['alt'])}" width="1600" height="900"><figcaption>{html.escape(imgs[0]['alt'])}</figcaption></figure>'''
        fig2=f'''<figure class="inline-figure"><img loading="lazy" src="{imgs[1]['src']}" alt="{html.escape(imgs[1]['alt'])}" width="1600" height="900"><figcaption>{html.escape(imgs[1]['alt'])}</figcaption></figure>'''
        matches=list(re.finditer(r'</section>', txt, flags=re.I))
        if len(matches)>=1:
            pos=matches[0].end(); txt=txt[:pos]+fig1+txt[pos:]
        matches=list(re.finditer(r'</section>', txt, flags=re.I))
        if len(matches)>=5:
            pos=matches[4].end(); txt=txt[:pos]+fig2+txt[pos:]
    # Related articles/end CTA before article close
    if 'class="related-grid"' not in txt:
        rels=article_related(a['slug'])[:6]
        rel_html=''.join(f'''<a class="related-card" href="/blog/{r['slug']}/"><div class="article-card-body"><p class="card-kicker">{html.escape(r['cat'])}</p><h3>{html.escape(r['title'])}</h3><p>{html.escape(r['desc'][:120])}</p></div></a>''' for r in rels)
        end=f'''<aside class="end-cta"><h2>Continue shopping privately</h2><p>Use the guide as a starting point, then compare products, care needs, delivery privacy, and checkout options.</p><div class="cta-row"><a class="cta-button" href="/index.php?route=product/search&language=en-gb&search=wellness">View All Products</a><a class="cta-button" href="/blog/">Back to Blog</a></div></aside><section><h2>Related Articles</h2><div class="related-grid">{rel_html}</div></section>'''
        txt=txt.replace('</article>', end+'</article>',1)
    # Ensure body has classes and only one gtag script load
    # remove duplicate gtag blocks accidentally left
    parts=re.split(r'(<!-- Google tag \(gtag\.js\) -->\s*<script async src="https://www\.googletagmanager\.com/gtag/js\?id=G-P2LJRXN3D1"></script>\s*<script>.*?</script>)', txt, flags=re.S)
    if len(parts)>3:
        first=''.join(parts[:3])
        rest=''.join(parts[3:])
        rest=re.sub(r'<!-- Google tag \(gtag\.js\) -->\s*<script async src="https://www\.googletagmanager\.com/gtag/js\?id=G-P2LJRXN3D1"></script>\s*<script>.*?</script>','',rest,flags=re.S)
        txt=first+rest
    p.write_text(txt, encoding='utf-8')

# report
report = OUT / f'blog_brand_unification_report_{TODAY}.md'
report.write_text(f'''# ShopLovaNest Blog Brand Unification Report - {TODAY}

## Scope
- Scanned OpenCart storefront templates: `upload/catalog/view/template/common/header.twig`, `common/footer.twig`, `common/home.twig`, product templates, information templates, and all static `upload/blog/*/index.html` pages.
- Updated static blog list and {len(articles_sorted)} blog detail pages to mirror the storefront Header/Navbar/Logo/Footer style.
- Added a reusable static blog shell pattern matching homepage variables, spacing, cards, CTA buttons, trust signals, payment cue, mobile hamburger, and footer links.

## Image plan
- JSON: `{PLAN_PATH.relative_to(ROOT)}`
- Focus articles: {len(image_plan)}
- Generated local optimized illustration assets under `upload/blog/assets/` with 16:9 cover/inline compositions.

## Key focus articles
{chr(10).join('- `/blog/'+x['slug']+'/` — '+x['main_keyword'] for x in image_plan)}

## Validation targets
- Google tag remains exactly once per blog page, immediately after `<head>`.
- Blog header includes Logo, Home, Shop, Categories, Blog, About, Contact, search, Login, Cart, mobile hamburger.
- Blog footer includes brand intro, categories, Blog, Contact, Shipping Policy, Return Policy, Privacy Policy, Terms, PayPal cue, social placeholders, copyright.
''', encoding='utf-8')
print(json.dumps({'articles':len(articles_sorted),'focus_images':len(image_plan),'plan':str(PLAN_PATH),'report':str(report)}, indent=2))
