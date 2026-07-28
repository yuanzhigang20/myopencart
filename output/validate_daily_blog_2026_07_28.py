from pathlib import Path
from html.parser import HTMLParser
import json,re
ROOT=Path('/Users/grant/IdeaProjects/myopencart'); DATE='2026-07-28'; BASE='https://shoplovanest.com'
slugs=['remote-control-adult-toys-guide','automatic-male-masturbator-guide']
required_refs=['consumer.ftc.gov','cisa.gov','tsa.gov','ul.com','saferproducts.gov']
banned_patterns=[r'\bporn\b',r'\bteen\b',r'\bminor\b',r'\bchild\b',r'\bcure\b',r'treat erectile',r'guaranteed orgasm',r'medical grade silicone']
class P(HTMLParser):
 def __init__(self): super().__init__(); self.title=''; self.in_title=False; self.skip=False; self.text=[]; self.h1=0; self.h3=0; self.links=[]; self.metas=[]; self.imgs=[]; self.figcaption=False
 def handle_starttag(self, tag, attrs):
  d=dict(attrs)
  if tag=='title': self.in_title=True
  if tag in ('style','script'): self.skip=True
  if tag=='h1': self.h1+=1
  if tag=='h3': self.h3+=1
  if tag=='a' and 'href' in d: self.links.append(d['href'])
  if tag=='meta': self.metas.append(d)
  if tag=='img': self.imgs.append(d)
  if tag=='figcaption': self.figcaption=True
 def handle_endtag(self,tag):
  if tag=='title': self.in_title=False
  if tag in ('style','script'): self.skip=False
 def handle_data(self,data):
  if self.in_title: self.title+=data
  if not self.skip: self.text.append(data)
results=[]
for slug in slugs:
 html=(ROOT/'upload/blog'/slug/'index.html').read_text(encoding='utf-8'); p=P(); p.feed(html)
 text=' '.join(x.strip() for x in p.text if x.strip()); words=re.findall(r"\b[A-Za-z][A-Za-z'-]*\b",text)
 meta=next((m.get('content','') for m in p.metas if m.get('name')=='description'),'')
 gtag_block=html.count('https://www.googletagmanager.com/gtag/js?id=G-P2LJRXN3D1')==1 and html.lower().startswith('<!doctype html><html lang="en"><head><!-- google tag')
 faq_json='FAQPage' in html and p.h3>=5
 quick='Quick Answer' in text
 red='Red Flags / when to slow down before checkout' in text
 internal=len([h for h in p.links if h.startswith('/blog/')])
 product=len([h for h in p.links if 'route=product/search' in h or 'route=information/contact' in h])
 refs=[h for h in p.links if h.startswith('http')]
 auth=sum(1 for d in required_refs if any(d in u for u in refs))
 hero=next((i for i in p.imgs if i.get('class')=='hero' or 'hero' in i.get('class','')), p.imgs[0] if p.imgs else {})
 has_meta=lambda **kw: any(all(m.get(k)==v for k,v in kw.items()) for m in p.metas)
 image_ok=bool(hero.get('alt') and hero.get('title') and p.figcaption and has_meta(property='og:image') and has_meta(property='og:image:alt') and has_meta(name='twitter:image') and has_meta(name='twitter:image:alt') and 'ImageObject' in html)
 banned_hits=[pat for pat in banned_patterns if re.search(pat,text.lower())]
 quality=100
 if len(p.title)>=60: quality-=8
 if len(meta)>=155: quality-=8
 if p.h1!=1: quality-=15
 if not gtag_block: quality-=10
 if len(words)<1000: quality-=20
 if not quick: quality-=10
 if not red: quality-=10
 if not faq_json: quality-=10
 if internal<4: quality-=5
 if product<3: quality-=5
 if auth<3: quality-=8
 if not image_ok: quality-=10
 if banned_hits: quality-=20
 results.append({'slug':slug,'title_len':len(p.title),'meta_len':len(meta),'h1_count':p.h1,'gtag_block_once_immediately_after_head':gtag_block,'word_count':len(words),'quick_answer':quick,'red_flags':red,'faq_schema':faq_json,'internal_blog_links':internal,'product_support_links':product,'authority_reference_domains_matched':auth,'image_seo_metadata':image_ok,'banned_hits':banned_hits,'quality_score':quality,'status':'pass' if quality>=85 and not banned_hits else 'fail'})
sitemap=(ROOT/'upload/sitemap.xml').read_text(encoding='utf-8')
for r in results:
 r['sitemap_url']=f'{BASE}/blog/{r["slug"]}/' in sitemap
 r['sitemap_lastmod']=f'<lastmod>{DATE}</lastmod>' in sitemap
 r['sitemap_image_metadata']=f'{BASE}/blog/assets/{r["slug"]}-opus-cover.png' in sitemap and '<image:title>' in sitemap and '<image:caption>' in sitemap
 if not (r['sitemap_url'] and r['sitemap_lastmod'] and r['sitemap_image_metadata']): r['status']='fail'; r['quality_score']=min(r['quality_score'],84)
idx=(ROOT/'upload/blog/index.html').read_text(encoding='utf-8')
index_ok=all(f'/blog/{s}/' in idx for s in slugs)
out={'date':DATE,'results':results,'blog_index_links':index_ok,'overall':'pass' if all(r['status']=='pass' for r in results) and index_ok else 'fail'}
print(json.dumps(out,indent=2))
(ROOT/'output/daily_blog_validation_2026-07-28.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
if out['overall']!='pass': raise SystemExit(1)
