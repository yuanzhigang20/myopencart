#!/usr/bin/env python3
from __future__ import annotations
import html, json, re, hashlib
from pathlib import Path

ROOT=Path('/Users/grant/IdeaProjects/myopencart')
BLOG=ROOT/'upload/blog'
ASSETS=BLOG/'assets'
OUT=ROOT/'output'
ASSETS.mkdir(exist_ok=True)
TODAY='2026-06-26'
GTAG_ID='G-P2LJRXN3D1'

# Richer, more article-specific visual language. SVG keeps it fast and safe, but no two covers are the same.
PALETTES=[('#fff6ee','#edcfc4','#9a5a4c','#2b1812'),('#fffaf5','#e7c7b5','#7f4639','#21130e'),('#f9f1eb','#d8b9aa','#b8796a','#2a1912'),('#fff4f7','#eec6d0','#8d4d61','#2b1620'),('#f6f3ef','#d8d0c5','#766050','#201713')]
THEMES=[
 ('lube|lubricant|condom','lubricant bottle, sealed condom packets, water drop texture, compatibility card','lube-condom'),
 ('clean|dry|cleaner|mistake','cleaning spray, soft towel, water droplets, drying rack','cleaning-care'),
 ('storage|lockable|privacy|billing|shipping|delivery|travel|tsa','plain parcel, lockable box, suitcase tag, privacy card','privacy-storage'),
 ('lingerie|lace|fabric|size','silk fabric folds, lace edge, measuring tape, soft hanger','lingerie'),
 ('kegel|pelvic','wellness spheres, soft pouch, routine card','pelvic-wellness'),
 ('couple|date-night|gift','gift box, two cups, warm candle, consent card','couples'),
 ('male|masturbator|cock-ring','premium product box, care pouch, water rinse cue','male-wellness'),
 ('vibrator|wand|rabbit|bullet|egg|suction|wearable|remote|rechargeable|waterproof|usb|g-spot|mini|palm','sleek intimate wellness device silhouette, charging cable, storage pouch','vibrator'),
 ('glass|steel|silicone|abs|jelly|material|porous|hypoallergenic|body-safe','material swatches, glass shine, silicone matte sample, safety checklist','materials'),
 ('anal|plug','beginner-safe tapered product silhouette, lube bottle, size guide card','anal-safety'),
]

def meta(p:Path):
    t=p.read_text(errors='ignore')
    slug=p.parent.name
    m=re.search(r'<h1[^>]*>(.*?)</h1>',t,re.S|re.I)
    title=html.unescape(re.sub('<[^>]+>','',m.group(1))).strip() if m else slug.replace('-',' ').title()
    m=re.search(r'<meta name="description" content="([^"]*)"',t,re.I)
    desc=html.unescape(m.group(1)).strip() if m else ''
    if not desc:
        m=re.search(r'<p class="(?:lede|article-summary)">(.*?)</p>',t,re.S|re.I)
        desc=html.unescape(re.sub('<[^>]+>','',m.group(1))).strip() if m else 'Private adult wellness shopping guide.'
    return slug,title,desc,t

def theme_for(slug,title):
    s=(slug+' '+title).lower()
    for pat,scene,key in THEMES:
        if re.search(pat,s): return scene,key
    return 'premium product flat-lay, plain packaging, shopping checklist, soft candle','buying-guide'

def cover_svg(slug,title,desc):
    scene,key=theme_for(slug,title)
    digest=int(hashlib.sha1(slug.encode()).hexdigest()[:8],16)
    bg,mid,accent,ink=PALETTES[digest%len(PALETTES)]
    w,h=1600,900
    # positions vary by slug
    shift=(digest%120)-60
    title_lines=[]; line=''
    for word in title.split():
        if len((line+' '+word).strip())>28 and line:
            title_lines.append(line); line=word
        else: line=(line+' '+word).strip()
    if line: title_lines.append(line)
    title_lines=title_lines[:3]
    scene_label=scene.split(',')[0].title()
    safe_title=html.escape(title)
    # Safe sensual ecommerce illustration: product silhouettes and scene props, not anatomy/acts.
    device='''<g opacity=".96" filter="url(#shadow)"><rect x="1035" y="250" width="168" height="390" rx="84" fill="#fffdf9" stroke="{mid}" stroke-width="5"/><ellipse cx="1119" cy="255" rx="70" ry="34" fill="{accent}" opacity=".22"/><path d="M1072 548 C1108 500 1165 501 1192 548" fill="none" stroke="{accent}" stroke-width="13" stroke-linecap="round" opacity=".5"/></g>'''.format(mid=mid,accent=accent)
    lube='''<g filter="url(#shadow)"><rect x="935" y="238" width="150" height="410" rx="42" fill="#fffdf9" stroke="{mid}" stroke-width="5"/><rect x="964" y="285" width="92" height="164" rx="22" fill="{accent}" opacity=".18"/><rect x="974" y="204" width="72" height="56" rx="18" fill="{ink}" opacity=".9"/><path d="M1195 420 C1248 464 1196 534 1153 492 C1127 466 1166 430 1195 420Z" fill="{accent}" opacity=".5"/><rect x="1130" y="602" width="240" height="72" rx="20" fill="#fff" stroke="{mid}" stroke-width="4"/><circle cx="1170" cy="638" r="18" fill="{accent}" opacity=".5"/><circle cx="1230" cy="638" r="18" fill="{accent}" opacity=".28"/></g>'''.format(mid=mid,accent=accent,ink=ink)
    parcel='''<g filter="url(#shadow)"><rect x="920" y="340" width="430" height="250" rx="34" fill="#fffdf9" stroke="{mid}" stroke-width="5"/><path d="M920 410 H1350" stroke="{mid}" stroke-width="5"/><path d="M1040 340 V590" stroke="{mid}" stroke-width="5"/><rect x="1135" y="455" width="150" height="64" rx="18" fill="{accent}" opacity=".25"/><circle cx="1005" cy="482" r="46" fill="{accent}" opacity=".18"/></g>'''.format(mid=mid,accent=accent)
    fabric='''<g filter="url(#shadow)"><path d="M890 610 C1010 360 1180 300 1395 390 C1310 520 1220 642 1030 706 C970 700 925 668 890 610Z" fill="#fffdf9" stroke="{mid}" stroke-width="5"/><path d="M970 610 C1080 520 1210 485 1340 500" fill="none" stroke="{accent}" stroke-width="10" opacity=".35"/><circle cx="1085" cy="455" r="48" fill="{accent}" opacity=".18"/></g>'''.format(mid=mid,accent=accent)
    checklist='''<g filter="url(#shadow)"><rect x="930" y="240" width="355" height="420" rx="35" fill="#fffdf9" stroke="{mid}" stroke-width="5"/><circle cx="990" cy="330" r="18" fill="{accent}" opacity=".65"/><rect x="1030" y="315" width="170" height="18" rx="9" fill="{ink}" opacity=".16"/><circle cx="990" cy="410" r="18" fill="{accent}" opacity=".45"/><rect x="1030" y="395" width="205" height="18" rx="9" fill="{ink}" opacity=".13"/><circle cx="990" cy="490" r="18" fill="{accent}" opacity=".32"/><rect x="1030" y="475" width="145" height="18" rx="9" fill="{ink}" opacity=".11"/><path d="M1235 620 C1305 550 1385 582 1372 660" stroke="{accent}" stroke-width="14" stroke-linecap="round" fill="none" opacity=".5"/></g>'''.format(mid=mid,accent=accent,ink=ink)
    if key=='lube-condom': art=lube
    elif key in ('privacy-storage',): art=parcel
    elif key=='lingerie': art=fabric
    elif key in ('cleaning-care','materials'): art=checklist
    else: art=device if digest%2 else checklist
    title_svg=''.join(f'<text x="126" y="{300+i*72}" font-family="Georgia,serif" font-size="60" font-weight="700" fill="{ink}">{html.escape(ln)}</text>' for i,ln in enumerate(title_lines))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900" role="img" aria-label="{safe_title}">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{bg}"/><stop offset=".58" stop-color="{mid}"/><stop offset="1" stop-color="#d5a99a"/></linearGradient><radialGradient id="glow" cx="74%" cy="28%" r="58%"><stop offset="0" stop-color="#fff" stop-opacity=".78"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient><filter id="shadow"><feDropShadow dx="0" dy="22" stdDeviation="22" flood-color="{ink}" flood-opacity=".17"/></filter></defs>
<rect width="1600" height="900" fill="url(#g)"/><rect width="1600" height="900" fill="url(#glow)"/><circle cx="{1340+shift}" cy="{180-shift//3}" r="165" fill="#fff" opacity=".38"/><circle cx="{1160-shift}" cy="720" r="235" fill="{accent}" opacity=".14"/>
<rect x="82" y="132" width="690" height="604" rx="46" fill="#fffdf9" opacity=".83" filter="url(#shadow)"/>
<text x="126" y="214" font-family="Arial,sans-serif" font-size="25" font-weight="800" letter-spacing="6" fill="{accent}">SHOPLOVANEST GUIDE</text>
{title_svg}
<text x="126" y="590" font-family="Arial,sans-serif" font-size="28" font-weight="700" fill="{ink}" opacity=".68">{html.escape(scene_label)}</text>
<text x="126" y="640" font-family="Arial,sans-serif" font-size="25" fill="{ink}" opacity=".58">Discreet · Body-safe · 18+ wellness</text>
{art}
</svg>'''

def inline_svg(slug,title,kind):
    scene,key=theme_for(slug,title)
    digest=int(hashlib.sha1((slug+kind).encode()).hexdigest()[:8],16)
    bg,mid,accent,ink=PALETTES[(digest+2)%len(PALETTES)]
    label='Compatibility checklist' if kind=='guide' else 'Product detail and care scene'
    motif='sealed packet + lubricant bottle' if key=='lube-condom' else scene.split(',')[0]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900" role="img" aria-label="{html.escape(title+' '+label)}"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{bg}"/><stop offset="1" stop-color="{mid}"/></linearGradient><filter id="s"><feDropShadow dx="0" dy="18" stdDeviation="20" flood-color="{ink}" flood-opacity=".13"/></filter></defs><rect width="1600" height="900" fill="url(#g)"/><circle cx="1210" cy="220" r="210" fill="#fff" opacity=".45"/><rect x="140" y="145" width="560" height="610" rx="44" fill="#fffdf9" filter="url(#s)"/><text x="200" y="260" font-family="Georgia,serif" font-size="66" font-weight="700" fill="{ink}">{html.escape(label)}</text><text x="200" y="335" font-family="Arial,sans-serif" font-size="30" fill="{ink}" opacity=".62">{html.escape(motif.title())}</text><circle cx="245" cy="455" r="23" fill="{accent}" opacity=".65"/><rect x="295" y="438" width="300" height="26" rx="13" fill="{ink}" opacity=".14"/><circle cx="245" cy="535" r="23" fill="{accent}" opacity=".45"/><rect x="295" y="518" width="340" height="26" rx="13" fill="{ink}" opacity=".12"/><circle cx="245" cy="615" r="23" fill="{accent}" opacity=".32"/><rect x="295" y="598" width="260" height="26" rx="13" fill="{ink}" opacity=".1"/><g filter="url(#s)"><rect x="965" y="260" width="170" height="420" rx="50" fill="#fffdf9" stroke="{mid}" stroke-width="5"/><rect x="995" y="325" width="110" height="145" rx="22" fill="{accent}" opacity=".2"/><rect x="1210" y="510" width="230" height="82" rx="24" fill="#fff" stroke="{mid}" stroke-width="5"/><circle cx="1258" cy="551" r="22" fill="{accent}" opacity=".45"/><path d="M1155 655 C1220 590 1325 612 1362 680" fill="none" stroke="{accent}" stroke-width="16" stroke-linecap="round" opacity=".46"/></g></svg>'''

def ensure_css(t):
    extra=r'''
.blog-article{font-size:16px}.article-content-card{background:#fffdf9;border:1px solid var(--lv-line);border-radius:18px;padding:clamp(18px,3vw,30px);box-shadow:0 10px 28px rgba(60,39,29,.05);margin:26px 0}.article-content-card h2{border-top:0!important;padding-top:0!important;margin-bottom:14px!important}.article-content-card p:last-child,.article-content-card ul:last-child{margin-bottom:0}.lede-card{background:linear-gradient(135deg,#fffdf9,#f5e4da);border:1px solid var(--lv-line);border-radius:18px;padding:24px;margin:24px 0;color:#4f4039;font-size:18px}.checklist{background:#fff8f4;border:1px solid var(--lv-line);border-radius:16px;padding:18px}.checklist li{margin:.45rem 0}.blog-article ul{padding-left:1.25rem}.blog-article a:not(.cta-button){font-weight:800;color:#704437;text-decoration-thickness:.08em;text-underline-offset:.18em}.related{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;margin-top:12px}.related a{background:#fffaf7;border:1px solid var(--lv-line);border-radius:14px;padding:14px;text-decoration:none}.article-visual-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}.article-visual-grid .inline-figure{margin:0}@media(max-width:680px){.article-content-card{padding:18px}.lede-card{font-size:16px}.related,.article-visual-grid{grid-template-columns:1fr}.blog-article h2{font-size:24px}}
'''
    # append once inside final style block
    if 'article-content-card' not in t:
        idx=t.rfind('</style>')
        if idx!=-1: t=t[:idx]+extra+t[idx:]
    return t

def clean_article(t,slug,title,desc):
    t=ensure_css(t)
    # Fix nested article opening from previous run.
    t=re.sub(r'\s*<article class="blog-article"\s+data-content-marker="[^"]*">\s*', '\n', t, flags=re.I)
    t=re.sub(r'(<header class="article-head">.*?</header>)\s*<article class="blog-article"[^>]*>\s*', r'\1\n', t, count=1, flags=re.S|re.I)
    # Remove old eyebrow inside article head leftovers.
    t=re.sub(r'<p class="eyebrow">18\+ sexual wellness education · [^<]*</p>\s*','',t,flags=re.I)
    # Ensure hero image for every article.
    cover=f'/blog/assets/{slug}-cover.svg'
    if 'article-hero-img' not in t:
        hero=f'<img class="article-hero-img" src="{cover}" alt="{html.escape(title)} cover image" width="1600" height="900" fetchpriority="high">'
        t=re.sub(r'</header>', hero+'</header>', t, count=1, flags=re.I)
    else:
        t=re.sub(r'<img class="article-hero-img" src="[^"]+" alt="[^"]*"', f'<img class="article-hero-img" src="{cover}" alt="{html.escape(title)} cover image"', t, count=1)
    # Convert leading lede to card.
    t=re.sub(r'<p class="lede">(.*?)</p>', r'<div class="lede-card">\1</div>', t, count=1, flags=re.S|re.I)
    # Wrap ordinary sections in content cards except related already grid section ok still card.
    def repl(m):
        body=m.group(1)
        if 'article-content-card' in body or 'related-grid' in body: return m.group(0)
        return '<section class="article-content-card">'+body+'</section>'
    t=re.sub(r'<section>(.*?)</section>', repl, t, flags=re.S|re.I)
    # Better old related block
    t=t.replace('<div class="related">','<div class="related">')
    # Remove old/generated inline figures, then insert exactly two content-specific images.
    t=re.sub(r'\s*<figure class="inline-figure">.*?</figure>\s*','\n',t,flags=re.S|re.I)
    # Add content-specific inline images for all guide pages after first/third content card.
    fig1=f'<figure class="inline-figure"><img loading="lazy" src="/blog/assets/{slug}-guide-1.svg" alt="{html.escape(title)} compatibility and buying checklist image" width="1600" height="900"><figcaption>{html.escape(title)} — visual checklist for safer private shopping.</figcaption></figure>'
    cards=list(re.finditer(r'</section>',t,flags=re.I))
    if cards:
        pos=cards[0].end(); t=t[:pos]+fig1+t[pos:]
    fig2=f'<figure class="inline-figure"><img loading="lazy" src="/blog/assets/{slug}-detail-1.svg" alt="{html.escape(title)} product detail and care image" width="1600" height="900"><figcaption>Product detail, privacy, and care cues matched to this guide.</figcaption></figure>'
    cards=list(re.finditer(r'</section>',t,flags=re.I))
    if len(cards)>=4:
        pos=cards[3].end(); t=t[:pos]+fig2+t[pos:]
    # Fix double article close if any.
    t=t.replace('</article></article>','</article>')
    return t

items=[]
for p in sorted(BLOG.glob('*/index.html')):
    if p.parent.name=='assets': continue
    slug,title,desc,t=meta(p)
    # Generate unique cover + inline thematic SVGs for every article.
    (ASSETS/f'{slug}-cover.svg').write_text(cover_svg(slug,title,desc),encoding='utf-8')
    (ASSETS/f'{slug}-guide-1.svg').write_text(inline_svg(slug,title,'guide'),encoding='utf-8')
    (ASSETS/f'{slug}-detail-1.svg').write_text(inline_svg(slug,title,'detail'),encoding='utf-8')
    p.write_text(clean_article(t,slug,title,desc),encoding='utf-8')
    scene,key=theme_for(slug,title)
    items.append({'slug':slug,'title':title,'theme':key,'cover_image':{'position':'article hero','ratio':'16:9','filename':f'{slug}-cover.svg','alt':f'{title} cover image','prompt':f'Premium, tasteful, policy-safe adult wellness ecommerce image for "{title}" featuring {scene}. Warm ivory/cocoa/blush palette, discreet but bolder sensual product styling, no nudity, no genitals, no sex act.'},'inline_images':[{'position':'after first content section','ratio':'16:9','filename':f'{slug}-guide-1.svg','alt':f'{title} checklist image','prompt':f'Article-specific checklist scene for {title}: {scene}; premium DTC adult wellness editorial image, safe/non-explicit.'},{'position':'middle of article','ratio':'16:9','filename':f'{slug}-detail-1.svg','alt':f'{title} product detail image','prompt':f'Article-specific product detail/care/privacy scene for {title}: {scene}; tasteful, bolder, safe/non-explicit.'}]})

(OUT/f'blog_full_article_image_plan_{TODAY}.json').write_text(json.dumps(items,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'articles':len(items),'assets':len(list(ASSETS.glob('*-cover.svg'))),'plan':str(OUT/f'blog_full_article_image_plan_{TODAY}.json')},indent=2))
