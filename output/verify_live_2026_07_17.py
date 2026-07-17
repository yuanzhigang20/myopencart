import urllib.request,re,json,datetime,sys
BASE='https://shoplovanest.com'; slugs=['male-masturbator-pink-sleeve-material-guide','cock-ring-with-plug-combo-safety-guide']
def fetch(url):
    req=urllib.request.Request(url,headers={'User-Agent':'ShopLovaNest daily verifier'})
    with urllib.request.urlopen(req,timeout=30) as r: return r.status,r.read().decode('utf-8','ignore')
checks={'article_urls_http_200':True,'blog_index_http_200_and_links':False,'sitemap_http_200_and_urls':False,'sitemap_image_metadata':True,'article_title_meta_h1_gtag':True,'quick_answer_red_flags_faq_authority_refs':True,'image_assets_http_200':True}
urls=[]
for slug in slugs:
    url=f'{BASE}/blog/{slug}/'; st,html=fetch(url); urls.append(url); checks['article_urls_http_200'] &= st==200
    checks['article_title_meta_h1_gtag'] &= bool(re.search(r'<title>[^<]+</title>',html) and re.search(r'<meta name="description" content="[^"]+"',html) and len(re.findall(r'<h1\b',html))==1 and html.count("gtag('config', 'G-P2LJRXN3D1')")==1 and html.count('G-P2LJRXN3D1')==2)
    checks['quick_answer_red_flags_faq_authority_refs'] &= all(x in html for x in ['Quick Answer','Red Flags / when to slow down before checkout','FAQPage','References and useful sources']) and len(re.findall(r'rel="nofollow noopener"',html))>=3
    # Article image metadata is verified here; sitemap image metadata is checked after sitemap fetch.
    checks['sitemap_image_metadata'] &= ('og:image' in html and 'twitter:image' in html and 'ImageObject' in html)
    img=re.search(r'<img class="hero" src="([^"]+)"',html).group(1)
    ist,_=fetch(BASE+img); checks['image_assets_http_200'] &= ist==200
st,idx=fetch(BASE+'/blog/'); urls.append(BASE+'/blog/'); checks['blog_index_http_200_and_links']=st==200 and all(f'/blog/{s}/' in idx for s in slugs)
st,sm=fetch(BASE+'/sitemap.xml'); urls.append(BASE+'/sitemap.xml'); checks['sitemap_http_200_and_urls']=st==200 and all(f'{BASE}/blog/{s}/' in sm and '<lastmod>2026-07-17</lastmod>' in sm for s in slugs)
checks['sitemap_image_metadata']=checks['sitemap_image_metadata'] and all((s+'-opus-cover.png') in sm and '<image:image>' in sm and '<image:title>' in sm and '<image:caption>' in sm for s in slugs)
res={'status':'pass' if all(checks.values()) else 'fail','verified_at':datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat(),'checks':checks,'urls':urls}
print(json.dumps(res,indent=2))
if res['status']!='pass': sys.exit(1)
