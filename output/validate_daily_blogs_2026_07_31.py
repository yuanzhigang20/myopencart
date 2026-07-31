from pathlib import Path
import re, json, xml.etree.ElementTree as ET
from html.parser import HTMLParser
ROOT=Path('/Users/grant/IdeaProjects/myopencart'); DATE='2026-07-31'; BASE='https://shoplovanest.com'
slugs=['adult-toys-malware-privacy-checklist','silver-bullet-vibrator-shopping-guide']
class Text(HTMLParser):
 def __init__(self): super().__init__(); self.text=[]
 def handle_data(self,d): self.text.append(d)
def txt(html):
 p=Text(); p.feed(html); return ' '.join(p.text)
results={}
for slug in slugs:
 path=ROOT/'upload/blog'/slug/'index.html'; h=path.read_text(encoding='utf-8'); t=txt(h)
 title=re.search(r'<title>(.*?)</title>',h,re.S).group(1); meta=re.search(r'<meta name="description" content="(.*?)"',h,re.S).group(1)
 checks={
  'title_under_60':len(title)<60,'meta_under_155':len(meta)<155,'one_h1':len(re.findall(r'<h1[ >]',h))==1,
  'gtag_once':h.count('G-P2LJRXN3D1')==2 and h.find('<head>')!=-1 and h.find('<!-- Google tag')<h.find('<meta charset'),
  'word_count':len(re.findall(r"[A-Za-z][A-Za-z'-]+",t)),'quick_answer':'Quick Answer' in h,
  'red_flags':'Red Flags / when to slow down before checkout' in h,'faq_schema':'FAQPage' in h,
  'faq_count':len(re.findall(r'<h3>',h))>=4,'authority_links':sum(1 for u in ['ftc.gov','cisa.gov','bluetooth.com','saferproducts.gov','ul.com','tsa.gov'] if u in h)>=3,
  'related_links':h.count('/blog/')>=4,'product_links':h.count('route=product/search')>=1,
  'image_meta':all(x in h for x in ['og:image','og:image:alt','twitter:image','twitter:image:alt','ImageObject','<figcaption>']),
  'banned_terms':not re.search(r'\b(teen|schoolgirl|underage|guaranteed orgasm)\b',t,re.I)
 }
 score=100
 for k,v in checks.items():
  if k=='word_count':
   if v<1000: score-=30
  elif not v: score-=8
 checks['quality_score']=score; checks['pass']=score>=85 and checks['word_count']>=1000 and all(v for k,v in checks.items() if k not in ['word_count','quality_score','pass'])
 results[slug]=checks
idx=(ROOT/'upload/blog/index.html').read_text(encoding='utf-8')
sitemap=(ROOT/'upload/sitemap.xml').read_text(encoding='utf-8')
index_checks={'http_local_index_has_new_links':all(f'/blog/{s}/' in idx for s in slugs),'blog_index_last_updated':DATE in idx}
sitemap_checks={}
for slug in slugs:
 sitemap_checks[slug]=all(x in sitemap for x in [f'{BASE}/blog/{slug}/','<lastmod>'+DATE+'</lastmod>','<image:image>',f'{BASE}/blog/assets/'])
print(json.dumps({'articles':results,'index':index_checks,'sitemap':sitemap_checks},indent=2))
if not all(r['pass'] for r in results.values()) or not all(index_checks.values()) or not all(sitemap_checks.values()): raise SystemExit(1)
