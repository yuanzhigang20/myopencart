#!/usr/bin/env python3
from pathlib import Path
from html.parser import HTMLParser
import re, json, sys
ROOT=Path('/Users/grant/IdeaProjects/myopencart')
DATE='2026-07-04'
SLUGS=['adult-toy-cleaner-spray-guide','wand-massager-power-adapter-guide']
class Parser(HTMLParser):
    def __init__(self): super().__init__(); self.text=[]; self.title=''; self.meta=[]; self.h1=0; self.a=[]; self.img=[]; self.in_title=False
    def handle_starttag(self, tag, attrs):
        d=dict(attrs)
        if tag=='title': self.in_title=True
        if tag=='h1': self.h1+=1
        if tag=='meta': self.meta.append(d)
        if tag=='a': self.a.append(d.get('href',''))
        if tag=='img': self.img.append(d)
    def handle_endtag(self, tag):
        if tag=='title': self.in_title=False
    def handle_data(self, data):
        self.text.append(data)
        if self.in_title: self.title+=data

def parse(path):
    html=path.read_text(encoding='utf-8'); p=Parser(); p.feed(html); text=' '.join(p.text)
    return html,p,text
results={}; ok=True
for slug in SLUGS:
    path=ROOT/'upload/blog'/slug/'index.html'
    html,p,text=parse(path)
    desc=next((m.get('content','') for m in p.meta if m.get('name')=='description'),'')
    checks={
      'title_length':len(p.title),'meta_length':len(desc),'word_count':len(re.findall(r'[A-Za-z]+', text)),
      'one_h1':p.h1==1,'gtag_id_count':html.count('G-P2LJRXN3D1'),'gtag_ok':html.count('G-P2LJRXN3D1')==2,
      'quick_answer':'Quick Answer' in text,'red_flags':'Red Flags' in text,'faqpage_jsonld':'FAQPage' in html,
      'authority_refs':len(re.findall(r'https://(?:www\.)?(?:fda|cdc|consumer\.ftc|ftc|iec|cpsc)\.', html))>=2,
      'internal_blog_links':len([a for a in p.a if a.startswith('/blog/')])>=4,
      'product_support_links':len([a for a in p.a if 'route=product' in a or 'route=information/contact' in a])>=3,
      'image_seo_metadata':bool(p.img and p.img[0].get('alt') and p.img[0].get('title') and 'og:image' in html and 'twitter:image' in html and 'ImageObject' in html),
      'content_marker':f'daily-blog-{DATE}' in html,
      'banned_terms_clear':not re.search(r'\b(?:teen|minors?|cure|guaranteed orgasm|porn)\b', text, re.I)
    }
    score=sum(1 for k,v in checks.items() if isinstance(v,bool) and v)*100//sum(1 for v in checks.values() if isinstance(v,bool))
    checks['quality_score']=score
    checks['status']='pass' if all(v for k,v in checks.items() if isinstance(v,bool)) and score>=85 and checks['title_length']<60 and checks['meta_length']<155 and checks['word_count']>=1000 else 'fail'
    results[slug]=checks
    ok &= checks['status']=='pass'
idx=(ROOT/'upload/blog/index.html').read_text()
sm=(ROOT/'upload/sitemap.xml').read_text()
index_ok=all(f'/blog/{s}/' in idx for s in SLUGS) and '100 discreet' in idx and '"numberOfItems": 100' in idx
sitemap_ok=all(f'/blog/{s}/' in sm and f'{s}-opus-cover.png' in sm and '<lastmod>2026-07-04</lastmod>' in sm for s in SLUGS)
print(json.dumps({'status':'pass' if ok and index_ok and sitemap_ok else 'fail','articles':results,'index_ok':index_ok,'sitemap_ok':sitemap_ok}, indent=2))
sys.exit(0 if ok and index_ok and sitemap_ok else 1)
