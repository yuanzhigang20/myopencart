import urllib.request,re,json
from html.parser import HTMLParser
DATE='2026-07-28'; BASE='https://shoplovanest.com'; slugs=['remote-control-adult-toys-guide','automatic-male-masturbator-guide']
class P(HTMLParser):
 def __init__(self): super().__init__(); self.title=''; self.in_title=False; self.text=[]; self.h1=0; self.h3=0; self.links=[]; self.metas=[]; self.imgs=[]; self.fig=False; self.skip=False
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if tag=='title': self.in_title=True
  if tag in ('script','style'): self.skip=True
  if tag=='h1': self.h1+=1
  if tag=='h3': self.h3+=1
  if tag=='a' and 'href' in d: self.links.append(d['href'])
  if tag=='meta': self.metas.append(d)
  if tag=='img': self.imgs.append(d)
  if tag=='figcaption': self.fig=True
 def handle_endtag(self,tag):
  if tag=='title': self.in_title=False
  if tag in ('script','style'): self.skip=False
 def handle_data(self,data):
  if self.in_title: self.title+=data
  if not self.skip: self.text.append(data)
def fetch(url):
 req=urllib.request.Request(url,headers={'User-Agent':'OpenClaw daily blog verifier'})
 with urllib.request.urlopen(req,timeout=30) as r: return r.status, r.read().decode('utf-8','replace')
res=[]
for slug in slugs:
 status,html=fetch(f'{BASE}/blog/{slug}/'); p=P(); p.feed(html); text=' '.join(x.strip() for x in p.text if x.strip())
 metas=p.metas; has_meta=lambda **kw: any(all(m.get(k)==v for k,v in kw.items()) for m in metas)
 refs=[h for h in p.links if h.startswith('http')]
 image_ok=bool(p.imgs and p.fig and has_meta(property='og:image') and has_meta(property='og:image:alt') and has_meta(name='twitter:image') and has_meta(name='twitter:image:alt') and 'ImageObject' in html)
 res.append({'slug':slug,'http':status,'title_present':bool(p.title),'meta_present':any(m.get('name')=='description' for m in metas),'h1_count':p.h1,'gtag_script_once':html.count('https://www.googletagmanager.com/gtag/js?id=G-P2LJRXN3D1')==1,'gtag_config_once':html.count("gtag('config', 'G-P2LJRXN3D1')")==1,'quick_answer':'Quick Answer' in text,'red_flags':'Red Flags / when to slow down before checkout' in text,'faq_schema':'FAQPage' in html,'authority_refs':len(refs),'image_seo_metadata':image_ok,'pass': status==200 and bool(p.title) and p.h1==1 and 'Quick Answer' in text and 'Red Flags / when to slow down before checkout' in text and 'FAQPage' in html and image_ok})
idx_status,idx=fetch(BASE+'/blog/'); sm_status,sm=fetch(BASE+'/sitemap.xml')
out={'date':DATE,'articles':res,'blog_index':{'http':idx_status,'links_all':all(f'/blog/{s}/' in idx for s in slugs)},'sitemap':{'http':sm_status,'urls_all':all(f'{BASE}/blog/{s}/' in sm for s in slugs),'lastmod':f'<lastmod>{DATE}</lastmod>' in sm,'image_metadata':all(f'{BASE}/blog/assets/{s}-opus-cover.png' in sm for s in slugs)},'overall':None}
out['overall']='pass' if all(r['pass'] for r in res) and out['blog_index']['http']==200 and out['blog_index']['links_all'] and out['sitemap']['http']==200 and out['sitemap']['urls_all'] and out['sitemap']['lastmod'] and out['sitemap']['image_metadata'] else 'fail'
print(json.dumps(out,indent=2))
open('/Users/grant/IdeaProjects/myopencart/output/daily_blog_live_verification_2026-07-28.json','w').write(json.dumps(out,indent=2))
if out['overall']!='pass': raise SystemExit(1)
