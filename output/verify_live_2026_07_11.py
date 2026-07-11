import json, re, sys, urllib.request, xml.etree.ElementTree as ET
from html.parser import HTMLParser
urls = [
    'https://shoplovanest.com/blog/vibrating-cock-ring-buyer-guide/',
    'https://shoplovanest.com/blog/bullet-vibrator-charger-guide/',
]
index_url = 'https://shoplovanest.com/blog/'
sitemap_url = 'https://shoplovanest.com/sitemap.xml'
class P(HTMLParser):
    def __init__(self):
        super().__init__(); self.h1=0; self.title=''; self.in_title=False; self.meta_desc=''; self.imgs=[]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=='title': self.in_title=True
        if tag=='h1': self.h1 += 1
        if tag=='meta' and a.get('name')=='description': self.meta_desc=a.get('content','')
        if tag=='img': self.imgs.append(a)
    def handle_endtag(self, tag):
        if tag=='title': self.in_title=False
    def handle_data(self, data):
        if self.in_title: self.title += data

def fetch(url):
    req=urllib.request.Request(url, headers={'User-Agent':'OpenClaw daily verifier'})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.status, r.read().decode('utf-8','replace'), dict(r.headers)
results={}
ok=True
for url in urls:
    status, html, headers=fetch(url); p=P(); p.feed(html)
    checks={
      'http_200': status==200,
      'title_present': bool(p.title.strip()),
      'meta_present': bool(p.meta_desc.strip()),
      'one_h1': p.h1==1,
      'gtag_script_and_config_once': html.count('G-P2LJRXN3D1')==2 and html.count('https://www.googletagmanager.com/gtag/js?id=G-P2LJRXN3D1')==1 and html.count("gtag('config', 'G-P2LJRXN3D1')")==1,
      'quick_answer': 'Quick Answer' in html,
      'red_flags': 'Red Flags' in html,
      'faqpage_schema': 'FAQPage' in html,
      'authority_refs': all(x in html for x in ['consumer.ftc.gov','www.iec.ch']) or ('cpsc.gov' in html and 'tsa.gov' in html),
      'image_seo': 'og:image' in html and 'twitter:image' in html and 'ImageObject' in html and any(img.get('alt') for img in p.imgs),
    }
    results[url]={'status':status,'title':p.title.strip(),'meta_length':len(p.meta_desc),'h1_count':p.h1,'checks':checks}
    ok = ok and all(checks.values())
status, idx, _=fetch(index_url)
idx_checks={'http_200':status==200, 'links_articles': all(u.replace('https://shoplovanest.com','') in idx for u in urls)}
results[index_url]={'status':status,'checks':idx_checks}
ok=ok and all(idx_checks.values())
status, sm, _=fetch(sitemap_url)
sm_checks={'http_200':status==200}
for u in urls:
    slug=u.rstrip('/').split('/')[-1]
    block=re.search(r'<url><loc>'+re.escape(u)+r'</loc>.*?</url>', sm, re.S)
    sm_checks[slug+'_present']=block is not None
    sm_checks[slug+'_lastmod']=bool(block and '<lastmod>2026-07-11</lastmod>' in block.group(0))
    sm_checks[slug+'_image_metadata']=bool(block and '<image:image>' in block.group(0) and '<image:loc>' in block.group(0) and '<image:title>' in block.group(0) and '<image:caption>' in block.group(0))
results[sitemap_url]={'status':status,'checks':sm_checks}
ok=ok and all(sm_checks.values())
print(json.dumps({'ok':ok,'results':results}, indent=2))
sys.exit(0 if ok else 1)
