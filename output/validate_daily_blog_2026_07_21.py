from pathlib import Path
import re,json
ROOT=Path('/Users/grant/IdeaProjects/myopencart'); DATE='2026-07-21'; BASE='https://shoplovanest.com'
slugs=['adult-toy-eggs-insertable-guide','rechargeable-bullet-vibrator-guide']
state=json.loads((ROOT/'output/daily_blog_automation_state.json').read_text())
def strip_tags(x): return re.sub(r'<[^>]+>',' ',x)
def attr(tag,name):
 m=re.search(name+r'=["\']([^"\']*)["\']',tag or '')
 return m.group(1) if m else ''
results=[]
for slug in slugs:
 html=(ROOT/'upload/blog'/slug/'index.html').read_text(encoding='utf-8'); text=strip_tags(html)
 title=re.search(r'<title>(.*?)</title>',html,re.S).group(1).strip(); meta=re.search(r'<meta name="description" content="([^"]*)"',html).group(1)
 h1=re.findall(r'<h1\b[^>]*>',html,re.I); h2=[strip_tags(x).strip() for x in re.findall(r'<h2\b[^>]*>(.*?)</h2>',html,re.I|re.S)]
 words=re.findall(r"\b[A-Za-z][A-Za-z'-]*\b", text); refs=re.findall(r'<a href="(https?://[^"]+)" rel="nofollow noopener"',html)
 internal=[u for u in re.findall(r'<a href="([^"]+)"',html) if u.startswith('/blog/') and u!=f'/blog/{slug}/']
 product=[u for u in re.findall(r'<a href="([^"]+)"',html) if 'route=product/search' in u or 'route=information/contact' in u]
 imgm=re.search(r'<img class="hero"([^>]*)>',html,re.S); imgtag=imgm.group(0) if imgm else ''
 checks={'title_len':len(title),'title_under_60':len(title)<60,'meta_len':len(meta),'meta_under_155':len(meta)<155,'h1_count':len(h1),'one_h1':len(h1)==1,'gtag_id_count':html.count('G-P2LJRXN3D1'),'gtag_exactly_once_config':html.count("gtag('config', 'G-P2LJRXN3D1')")==1,'gtag_immediately_after_head':html.startswith('<!doctype html><html lang="en"><head><!-- Google tag'),'word_count':len(words),'word_count_1000_plus':len(words)>=1000,'quick_answer':any('Quick Answer'==x for x in h2),'red_flags':any('Red Flags' in x for x in h2),'faq_count':len(re.findall(r'<h3\b',html)),'faqpage_jsonld':'FAQPage' in html,'internal_blog_links':len(set(internal)),'product_support_links':len(set(product)),'authority_refs':len(refs),'has_authority':len(refs)>=4,'og_image':'property="og:image"' in html,'og_image_alt':'property="og:image:alt"' in html,'twitter_image':'name="twitter:image"' in html,'twitter_image_alt':'name="twitter:image:alt"' in html,'image_alt_title_figcaption':bool(imgtag and attr(imgtag,'alt') and attr(imgtag,'title') and '<figcaption>' in html),'jsonld_imageobject':'ImageObject' in html,'banned_scan_pass':not re.search(r'\b(minor|teen|porn|xxx|guaranteed orgasm|cure|treats?|fertility|therapy)\b', text, re.I),'quick_answer_near_top':html.find('Quick Answer') < html.find('<section class="content-card"') if 'Quick Answer' in html else False}
 must=['title_under_60','meta_under_155','one_h1','gtag_exactly_once_config','gtag_immediately_after_head','word_count_1000_plus','quick_answer','red_flags','faqpage_jsonld','has_authority','og_image','og_image_alt','twitter_image','twitter_image_alt','image_alt_title_figcaption','jsonld_imageobject','banned_scan_pass']
 checks['quality_score']=100-sum(8 for m in must if not checks[m])-max(0,4-len(set(internal)))*2-max(0,3-len(set(product)))*2-max(0,4-len(refs))*2
 checks['pass']=all(checks[m] for m in must) and checks['internal_blog_links']>=4 and checks['product_support_links']>=3 and checks['quality_score']>=85
 results.append({'slug':slug,'title':title,'meta':meta,'checks':checks,'refs':refs})
sm=(ROOT/'upload/sitemap.xml').read_text(encoding='utf-8'); sitemap={}
for slug in slugs:
 url=f'{BASE}/blog/{slug}/'; chunk=sm[sm.find(url):sm.find(url)+1800] if url in sm else ''
 sitemap[slug]={'url_present':url in sm,'lastmod':f'<lastmod>{DATE}</lastmod>' in chunk,'image_metadata':'image:image' in chunk and 'image:loc' in chunk and 'image:title' in chunk and 'image:caption' in chunk}
index=(ROOT/'upload/blog/index.html').read_text(encoding='utf-8')
index_checks={'links_new_articles':all(f'/blog/{s}/' in index for s in slugs),'blog_count_meta_updated':'133 discreet' in index or 'numberOfItems": 133' in index}
status='pass' if all(r['checks']['pass'] for r in results) and all(v['url_present'] and v['lastmod'] and v['image_metadata'] for v in sitemap.values()) and index_checks['links_new_articles'] else 'fail'
state['content_quality_validation']={'status':status,'results':results,'sitemap_checks':sitemap,'index_checks':index_checks,'validated_at':DATE}
if status=='pass': state['status']='validated_pending_commit_deploy_email'
(ROOT/'output/daily_blog_automation_state.json').write_text(json.dumps(state,indent=2),encoding='utf-8')
print(json.dumps(state['content_quality_validation'],indent=2)[:8000])
raise SystemExit(0 if status=='pass' else 1)
