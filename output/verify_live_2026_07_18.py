import urllib.request,re,sys,json,datetime
BASE='https://shoplovanest.com'
slugs=['silicone-lube-with-silicone-toys-guide','rubber-cock-ring-material-fit-guide']
images=['silicone-lube-with-silicone-toys-guide-opus-cover.png','rubber-cock-ring-material-fit-guide-opus-cover.png']
def fetch(url):
    req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 ShopLovaNest verifier'})
    with urllib.request.urlopen(req,timeout=30) as r:
        return r.status,r.read().decode('utf-8','ignore')
checks={'article_urls_http_200':True,'blog_index_http_200_and_links':False,'sitemap_http_200_and_urls':False,'sitemap_image_metadata':False,'article_title_meta_h1_gtag':True,'quick_answer_red_flags_faq_authority_refs':True,'image_seo_metadata':True,'image_assets_http_200':True}
urls=[]
for slug in slugs:
    url=f'{BASE}/blog/{slug}/'; urls.append(url); st,html=fetch(url)
    checks['article_urls_http_200'] &= st==200
    checks['article_title_meta_h1_gtag'] &= bool(re.search(r'<title>[^<]{1,59}</title>',html)) and bool(re.search(r'<meta name="description" content="[^"]{1,154}"',html)) and len(re.findall(r'<h1\b',html))==1 and html.count("gtag('config', 'G-P2LJRXN3D1')")==1 and html.count('G-P2LJRXN3D1')==2
    checks['quick_answer_red_flags_faq_authority_refs'] &= 'Quick Answer' in html and 'Red Flags / when to slow down before checkout' in html and 'FAQPage' in html and len(set(re.findall(r'href="(https://[^"]+)',html)))>=3
    checks['image_seo_metadata'] &= all(x in html for x in ['og:image','og:image:alt','twitter:image','twitter:image:alt','ImageObject','<figcaption>'])
for img in images:
    req=urllib.request.Request(f'{BASE}/blog/assets/{img}',headers={'User-Agent':'Mozilla/5.0'})
    with urllib.request.urlopen(req,timeout=30) as r: checks['image_assets_http_200'] &= r.status==200
st,idx=fetch(f'{BASE}/blog/'); urls.append(f'{BASE}/blog/')
checks['blog_index_http_200_and_links']=st==200 and all(f'/blog/{s}/' in idx for s in slugs)
st,sm=fetch(f'{BASE}/sitemap.xml'); urls.append(f'{BASE}/sitemap.xml')
checks['sitemap_http_200_and_urls']=st==200 and all(f'{BASE}/blog/{s}/' in sm and '<lastmod>2026-07-18</lastmod>' in sm for s in slugs)
checks['sitemap_image_metadata']=all(img in sm and '<image:title>' in sm and '<image:caption>' in sm for img in images)
status='pass' if all(checks.values()) else 'fail'
res={'status':status,'verified_at':datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat(),'checks':checks,'urls':urls}
print(json.dumps(res,indent=2))
if status!='pass': sys.exit(1)
