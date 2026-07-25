import urllib.request,re,json,sys
DATE='2026-07-25'; BASE='https://shoplovanest.com'
slugs=['adult-toy-box-privacy-care-guide','cock-ring-tightness-comfort-guide']
results=[]
for slug in slugs:
    url=f'{BASE}/blog/{slug}/'; req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 ShopLovaNestVerifier/1.0'}); resp=urllib.request.urlopen(req,timeout=30); html=resp.read().decode('utf-8','replace'); status=resp.status
    checks={
        'http_200':status==200,
        'title_present':'<title>' in html,
        'meta_present':'<meta name="description"' in html,
        'one_h1':len(re.findall(r'<h1\b',html,re.I))==1,
        'gtag_config_once':html.count("gtag('config', 'G-P2LJRXN3D1')")==1,
        'quick_answer':'Quick Answer' in html,
        'red_flags':'Red Flags / when to slow down before checkout' in html,
        'faqpage':'FAQPage' in html,
        'authority_refs':len(re.findall(r'href="https?://[^"]+" rel="nofollow noopener"',html))>=4,
        'image_seo':all(x in html for x in ['property="og:image"','property="og:image:alt"','name="twitter:image"','name="twitter:image:alt"','ImageObject','<figcaption>']),
        'content_marker':f'daily-blog-{DATE}' in html
    }
    checks['pass']=all(checks.values())
    results.append({'url':url,'checks':checks})
idx_resp=urllib.request.urlopen(urllib.request.Request(BASE+'/blog/',headers={'User-Agent':'Mozilla/5.0 ShopLovaNestVerifier/1.0'}),timeout=30); idx_text=idx_resp.read().decode('utf-8','replace'); sm_resp=urllib.request.urlopen(urllib.request.Request(BASE+'/sitemap.xml',headers={'User-Agent':'Mozilla/5.0 ShopLovaNestVerifier/1.0'}),timeout=30); sm_text=sm_resp.read().decode('utf-8','replace')
index_checks={'http_200':idx_resp.status==200,'links_new_articles':all(f'/blog/{s}/' in idx_text for s in slugs)}
sitemap_checks={'http_200':sm_resp.status==200}
for slug in slugs:
    chunk=sm_text[sm_text.find(f'{BASE}/blog/{slug}/'):sm_text.find(f'{BASE}/blog/{slug}/')+2500] if f'{BASE}/blog/{slug}/' in sm_text else ''
    sitemap_checks[slug]={'url_present':f'{BASE}/blog/{slug}/' in sm_text,'lastmod':f'<lastmod>{DATE}</lastmod>' in chunk,'image_metadata':'image:image' in chunk and 'image:loc' in chunk and 'image:title' in chunk and 'image:caption' in chunk}
status='pass' if all(x['checks']['pass'] for x in results) and all(index_checks.values()) and sitemap_checks['http_200'] and all(v['url_present'] and v['lastmod'] and v['image_metadata'] for k,v in sitemap_checks.items() if isinstance(v,dict)) else 'fail'
out={'status':status,'articles':results,'blog_index':index_checks,'sitemap':sitemap_checks}
print(json.dumps(out,indent=2))
sys.exit(0 if status=='pass' else 1)
