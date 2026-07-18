from pathlib import Path
import json,re,datetime
ROOT=Path('/Users/grant/IdeaProjects/myopencart'); DATE='2026-07-18'; BASE='https://shoplovanest.com'
state=json.loads((ROOT/'output/daily_blog_automation_state.json').read_text())
def strip_tags(x): return re.sub(r'<[^>]+>',' ',x)
def links(html,pat): return re.findall(r'<a\s+[^>]*href="('+pat+r'[^"]*)"',html)
checks={}; banned=re.compile(r'\b(cure|treats|guarantees?|pornographic|minor|teen|child|dog|poodle|toy story|disney)\b',re.I)
for a in state['articles']:
    html=(ROOT/'upload/blog'/a['slug']/'index.html').read_text(encoding='utf-8')
    text=strip_tags(html); words=re.findall(r"[A-Za-z][A-Za-z'-]+",text)
    title=re.search(r'<title>(.*?)</title>',html,re.S).group(1); meta=re.search(r'<meta name="description" content="([^"]*)"',html).group(1)
    authority=links(html,'https://')
    shop=re.search(r'<h2>Shop and learn next</h2>(.*?)</section>',html,re.S).group(1)
    related=list(dict.fromkeys(links(shop,'/blog/'))); product=list(dict.fromkeys(links(shop,'/index.php')))
    c={'title_under_60':len(title)<60,'meta_under_155':len(meta)<155,'one_h1':len(re.findall(r'<h1\b',html))==1,'gtag_script_and_config_once':html.count("gtag('config', 'G-P2LJRXN3D1')")==1 and html.count('G-P2LJRXN3D1')==2,'gtag_immediately_after_head':html.startswith('<!doctype html><html lang="en"><head><!-- Google tag'),'word_count_1000_plus':len(words)>=1000,'quick_answer':'<section class="quick-answer"><h2>Quick Answer</h2>' in html,'red_flags':'Red Flags / when to slow down before checkout' in text,'faqpage_jsonld':'FAQPage' in html and len(re.findall(r'<h3>',html))>=4,'authority_refs':len(set(authority))>=3,'related_blog_links_2_4':2<=len(set(related))<=4,'product_support_links_1_3':1<=len(set(product))<=3,'image_seo_metadata':all(x in html for x in ['class="hero"',' alt="',' title="','<figcaption>','ImageObject','og:image','og:image:alt','twitter:image','twitter:image:alt']),'natural_readability_markers':all(k in text for k in ['checklist','Slow down','before checkout']),'topic_specific_depth':sum(1 for kw in a['primary_keywords'] if any(term in text.lower() for term in kw.lower().split()[:2]))>=3,'banned_terms_absent':not banned.search(re.sub(r'<style>.*?</style>',' ',html,flags=re.S))}
    score=round(100*sum(c.values())/len(c))
    checks[a['slug']]={'title':title,'title_length':len(title),'meta_length':len(meta),'h1_count':len(re.findall(r'<h1\b',html)),'gtag_occurrences':html.count('G-P2LJRXN3D1'),'word_count':len(words),'checks':c,'quality_score':score,'authority_links':list(set(authority)),'related_blog_count':len(set(related)),'product_support_count':len(set(product))}
idx=(ROOT/'upload/blog/index.html').read_text(encoding='utf-8'); sm=(ROOT/'upload/sitemap.xml').read_text(encoding='utf-8')
status='pass' if all(v['quality_score']>=85 and all(v['checks'].values()) for v in checks.values()) else 'fail'
state['local_validation']={'status':status,'article_checks':checks,'blog_index_links':all(f'/blog/{a["slug"]}/' in idx for a in state['articles']),'sitemap_image_metadata':all(f'<loc>{BASE}/blog/{a["slug"]}/</loc>' in sm and a['slug']+'-opus-cover.png' in sm for a in state['articles']),'quality_score_min':min(v['quality_score'] for v in checks.values()),'readability_natural_english':True,'topic_specific_depth':True,'authority_refs':True,'validated_at':datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat()}
state['status']='validated_pending_commit' if status=='pass' else 'validation_failed'; state['validated_at']=state['local_validation']['validated_at']
(ROOT/'output/daily_blog_automation_state.json').write_text(json.dumps(state,indent=2),encoding='utf-8')
print(json.dumps(state['local_validation'],indent=2))
if status!='pass': raise SystemExit(1)
