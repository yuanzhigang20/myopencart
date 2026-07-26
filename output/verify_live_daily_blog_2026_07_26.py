import urllib.request,re,json,sys
urls=['https://shoplovanest.com/blog/kegel-balls-beginner-weight-guide/','https://shoplovanest.com/blog/waterproof-vibrator-ip-ratings-guide/']
result={}
def fetch(u):
    req=urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0 ShopLovaNestVerification/1.0'})
    with urllib.request.urlopen(req,timeout=30) as r:
        return r.status,r.read().decode('utf-8','replace')
for u in urls:
    status,html=fetch(u)
    result[u]={
        'http_200':status==200,
        'title_present':bool(re.search(r'<title>[^<]+</title>',html,re.S)),
        'meta_description_present':bool(re.search(r'<meta name="description" content="[^"]+"',html)),
        'one_h1':len(re.findall(r'<h1\b',html))==1,
        'gtag_block_once':html.count('<!-- Google tag (gtag.js) -->')==1 and html.count('G-P2LJRXN3D1')==2,
        'quick_answer': 'Quick Answer' in html,
        'red_flags':'Red Flags / when to slow down before checkout' in html,
        'faq_schema':'"@type": "FAQPage"' in html,
        'authority_refs':any(d in html for d in ['fda.gov','nhs.uk','cdc.gov','iec.ch','ul.com','saferproducts.gov','consumer.ftc.gov']),
        'image_seo_metadata':all(x in html for x in ['og:image','og:image:alt','twitter:image','twitter:image:alt','ImageObject','figcaption']),
    }
status,idx=fetch('https://shoplovanest.com/blog/')
result['https://shoplovanest.com/blog/']={'http_200':status==200,'links_new_articles':all(u.replace('https://shoplovanest.com','') in idx for u in urls)}
status,sm=fetch('https://shoplovanest.com/sitemap.xml')
result['https://shoplovanest.com/sitemap.xml']={'http_200':status==200,'includes_new_urls':all(u in sm for u in urls),'includes_lastmod_2026_07_26':'2026-07-26' in sm,'includes_image_metadata':'image:image' in sm and all(u.split('/blog/')[1].strip('/') in sm for u in urls)}
print(json.dumps(result,indent=2))
if not all(all(v.values()) for v in result.values()): sys.exit(1)
