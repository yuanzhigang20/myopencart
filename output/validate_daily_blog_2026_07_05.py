#!/usr/bin/env python3
from pathlib import Path
from html.parser import HTMLParser
import re,json,sys,xml.etree.ElementTree as ET
ROOT=Path('/Users/grant/IdeaProjects/myopencart'); BLOG=ROOT/'upload/blog'; DATE='2026-07-05'
SLUGS=['remote-control-cock-ring-guide','silicone-lube-spray-guide']; GTAG='G-P2LJRXN3D1'
class P(HTMLParser):
 def __init__(self): super().__init__(); self.tags=[]; self.h1=0; self.title=''; self.meta=''; self.img=[]; self.links=[]; self.h2=[]; self.h3=[]; self.in_title=False; self.in_h2=False; self.in_h3=False; self.text=[]
 def handle_starttag(self,tag,attrs):
  d=dict(attrs); self.tags.append((tag,d))
  if tag=='h1': self.h1+=1
  if tag=='title': self.in_title=True
  if tag=='h2': self.in_h2=True
  if tag=='h3': self.in_h3=True
  if tag=='meta' and d.get('name')=='description': self.meta=d.get('content','')
  if tag=='img': self.img.append(d)
  if tag=='a' and d.get('href'): self.links.append(d['href'])
 def handle_endtag(self,tag):
  if tag=='title': self.in_title=False
  if tag=='h2': self.in_h2=False
  if tag=='h3': self.in_h3=False
 def handle_data(self,data):
  if self.in_title: self.title+=data
  if self.in_h2: self.h2.append(data.strip())
  if self.in_h3: self.h3.append(data.strip())
  self.text.append(data)
def validate(slug):
 html=(BLOG/slug/'index.html').read_text(); p=P(); p.feed(html); text=' '.join(p.text); words=re.findall(r"[A-Za-z][A-Za-z'-]+", text)
 internal=[x for x in p.links if x.startswith('/blog/') and x != f'/blog/{slug}/']; product=[x for x in p.links if 'route=product/search' in x or 'route=information/contact' in x]
 auth=[x for x in p.links if x.startswith('https://www.fda.gov') or x.startswith('https://www.cdc.gov') or x.startswith('https://consumer.ftc.gov') or x.startswith('https://www.plannedparenthood.org') or x.startswith('https://www.cpsc.gov') or x.startswith('https://www.tsa.gov')]
 checks={
  'title_length':len(p.title),'meta_length':len(p.meta),'word_count':len(words),'one_h1':p.h1==1,
  'gtag_id_count':html.count(GTAG),'gtag_ok':html.count(GTAG)==2 and html.startswith('<!doctype html><html lang="en"><head><!-- Google tag'),
  'quick_answer': 'Quick Answer' in text,'red_flags':'Red Flags / when to slow down before checkout' in text,
  'faqpage_jsonld':'FAQPage' in html and len(p.h3)>=4,'authority_refs':len(auth)>=3,
  'internal_blog_links':len(set(internal))>=2,'product_support_links':len(set(product))>=1,
  'image_seo_metadata':bool(p.img and p.img[0].get('alt') and p.img[0].get('title') and 'og:image' in html and 'twitter:image' in html and 'ImageObject' in html),
  'content_marker':f'daily-blog-{DATE}' in html,
  'banned_terms_clear': not re.search(r'\b(porn|teen|underage|children|child|dog|pet|minecraft|mcdonald|disney|toy story)\b', text, re.I)
 }
 score=sum(1 for k,v in checks.items() if (v if isinstance(v,bool) else True))*100//len(checks); checks['quality_score']=score; checks['status']='pass' if all([checks['title_length']<60,checks['meta_length']<155,checks['word_count']>=1000,checks['one_h1'],checks['gtag_ok'],checks['quick_answer'],checks['red_flags'],checks['faqpage_jsonld'],checks['authority_refs'],checks['internal_blog_links'],checks['product_support_links'],checks['image_seo_metadata'],checks['content_marker'],checks['banned_terms_clear'],score>=85]) else 'fail'
 return checks
res={s:validate(s) for s in SLUGS}
# sitemap image metadata
sm=(ROOT/'upload/sitemap.xml').read_text(); sitemap_ok=all(f'https://shoplovanest.com/blog/{s}/' in sm and f'<lastmod>{DATE}</lastmod>' in sm and f'{s}-opus-cover.png' in sm for s in SLUGS) and 'https://shoplovanest.com/blog/' in sm
out={'date':DATE,'articles':res,'sitemap_image_metadata':sitemap_ok,'status':'pass' if all(v['status']=='pass' for v in res.values()) and sitemap_ok else 'fail'}
print(json.dumps(out,indent=2))
sys.exit(0 if out['status']=='pass' else 1)
