import json, re, urllib.request, xml.etree.ElementTree as ET
from html.parser import HTMLParser
DATE='2026-07-30'; BASE='https://shoplovanest.com'
slugs=['cock-ring-fit-time-limit-guide','best-water-based-lube-checklist']
class P(HTMLParser):
 def __init__(self): super().__init__(); self.title=''; self._title=False; self.metas=[]; self.h1=0; self.text=[]; self.links=[]; self.imgs=[]
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if tag=='title': self._title=True
  if tag=='meta': self.metas.append(d)
  if tag=='h1': self.h1+=1
  if tag=='a': self.links.append(d.get('href',''))
  if tag=='img': self.imgs.append(d)
 def handle_endtag(self,tag):
  if tag=='title': self._title=False
 def handle_data(self,d):
  if self._title: self.title+=d
  if d.strip(): self.text.append(d.strip())
 def get_text(self): return ' '.join(self.text)
def fetch(url):
 req=urllib.request.Request(url, headers={'User-Agent':'ShopLovaNestDailyVerifier/1.0'})
 with urllib.request.urlopen(req, timeout=30) as r:
  return r.status, r.geturl(), r.read().decode('utf-8','replace')
results=[]
for slug in slugs:
 url=f'{BASE}/blog/{slug}/'; status,final,html=fetch(url); p=P(); p.feed(html); text=p.get_text(); meta=next((m.get('content','') for m in p.metas if m.get('name')=='description'),'')
 hero=next((i for i in p.imgs if i.get('class')=='hero' or slug in i.get('src','')), {})
 checks={'http_200':status==200,'title_present':bool(p.title.strip()),'meta_present':80<len(meta)<155,'h1_one':p.h1==1,'gtag_once':html.count('G-P2LJRXN3D1')==2,'quick_answer':'Quick Answer' in text,'red_flags':'Red Flags / when to slow down before checkout' in text,'faq_schema':'FAQPage' in html,'authority_refs':sum(1 for u in p.links if u.startswith('https://'))>=3,'image_seo':bool(hero.get('alt') and hero.get('title') and 'og:image' in html and 'twitter:image' in html and 'ImageObject' in html),'daily_marker':f'daily-blog-{DATE}' in html}
 results.append({'slug':slug,'url':url,'status':status,'title':p.title.strip(),'meta_len':len(meta),'h1_count':p.h1,'checks':checks,'pass':all(checks.values())})
status,index_url,index_html=fetch(BASE+'/blog/'); sitemap_status,sitemap_url,sitemap_xml=fetch(BASE+'/sitemap.xml')
idx_checks={'http_200':status==200,**{f'links_{s}':f'/blog/{s}/' in index_html for s in slugs}}
ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9','image':'http://www.google.com/schemas/sitemap-image/1.1'}
root=ET.fromstring(sitemap_xml.encode())
site_checks={'http_200':sitemap_status==200}
for slug in slugs:
 loc=f'{BASE}/blog/{slug}/'; node=None
 for u in root.findall('s:url',ns):
  l=u.find('s:loc',ns)
  if l is not None and l.text==loc: node=u; break
 site_checks[f'includes_{slug}']=node is not None
 site_checks[f'lastmod_{slug}']=(node.find('s:lastmod',ns).text==DATE if node is not None and node.find('s:lastmod',ns) is not None else False)
 site_checks[f'image_{slug}']=(len(node.findall('image:image',ns))>=1 if node is not None else False)
report={'date':DATE,'articles':results,'blog_index':idx_checks,'sitemap':site_checks,'all_pass':all(r['pass'] for r in results) and all(idx_checks.values()) and all(site_checks.values())}
open('/Users/grant/IdeaProjects/myopencart/output/daily_blog_live_verification_2026-07-30.json','w').write(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
if not report['all_pass']: raise SystemExit(1)
