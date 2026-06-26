#!/usr/bin/env python3
from pathlib import Path
import re, html
ROOT=Path('/Users/grant/IdeaProjects/myopencart')
BLOG=ROOT/'upload/blog'
for p in sorted(BLOG.glob('*/index.html')):
    if p.parent.name=='assets': continue
    slug=p.parent.name
    t=p.read_text(errors='ignore')
    # remove nested article marker if any
    t=re.sub(r'\s*<article class="blog-article"\s+data-content-marker="[^"]*">\s*','\n',t,flags=re.I)
    # Extract title for alt.
    m=re.search(r'<h1[^>]*>(.*?)</h1>',t,re.S|re.I)
    title=html.unescape(re.sub('<[^>]+>','',m.group(1))).strip() if m else slug.replace('-',' ').title()
    cover=f'/blog/assets/{slug}-cover.svg'
    hero=f'<img class="article-hero-img" src="{cover}" alt="{html.escape(title)} cover image" width="1600" height="900" fetchpriority="high">'
    # Normalize any existing article hero to unique slug cover.
    if 'article-hero-img' in t:
        t=re.sub(r'<img class="article-hero-img"[^>]*>', hero, t, count=1, flags=re.I)
    else:
        def add_hero(m):
            block=m.group(0)
            return block[:-9] + hero + '</header>'
        t=re.sub(r'<header class="article-head">.*?</header>', add_hero, t, count=1, flags=re.S|re.I)
    # Fix CSS escaped icon if previous script lost backslash in CSS content.
    t=t.replace('content:"002";font-family:"Font Awesome 6 Free"', 'content:"\\f002";font-family:"Font Awesome 6 Free"')
    t=t.replace('</article></article>','</article>')
    p.write_text(t,encoding='utf-8')
print('patched', len(list(BLOG.glob('*/index.html'))))
