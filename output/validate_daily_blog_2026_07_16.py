from pathlib import Path
import json,re,xml.etree.ElementTree as ET,datetime
ROOT=Path('/Users/grant/IdeaProjects/myopencart'); BLOG=ROOT/'upload/blog'; DATE='2026-07-16'; BASE='https://shoplovanest.com'
slugs=['edible-flavored-water-based-lube-guide','smart-adult-toy-privacy-security-guide']
banned=[r'\bteen\b',r'\bminor\b',r'\bchild\b',r'\bkids\b',r'\bcure\b',r'\bguaranteed\b',r'\bpornographic\b']
required_auth=['fda.gov','cdc.gov','plannedparenthood.org','consumer.ftc.gov','cisa.gov','nist.gov']
results={}
def tag_text(html, tag):
    m=re.search(rf'<{tag}[^>]*>(.*?)</{tag}>', html, re.I|re.S)
    return re.sub(r'<[^>]+>',' ',m.group(1)).strip() if m else ''
def metas(html, key, val):
    return re.findall(r'<meta[^>]*\b'+re.escape(key)+r'=["\']'+re.escape(val)+r'["\'][^>]*>', html, re.I)
def attr(tag, name):
    m=re.search(r'\b'+re.escape(name)+r'=["\']([^"\']*)["\']', tag, re.I)
    return m.group(1) if m else ''
for slug in slugs:
    p=BLOG/slug/'index.html'; html=p.read_text(encoding='utf-8')
    title=tag_text(html,'title')
    meta_tags=metas(html,'name','description'); meta_content=attr(meta_tags[0],'content') if meta_tags else ''
    h1=re.findall(r'<h1\b[^>]*>', html, re.I)
    gtag_config=len(re.findall(r"gtag\('config',\s*'G-P2LJRXN3D1'\)",html)); gtag_src=len(re.findall(r'googletagmanager\.com/gtag/js\?id=G-P2LJRXN3D1',html))
    head_after='<head><!-- Google tag' in html[:120] or '<head>'+"<!-- Google tag" in html[:120]
    text=re.sub(r'<script.*?</script>|<style.*?</style>',' ',html,flags=re.I|re.S)
    text=re.sub(r'<[^>]+>',' ',text)
    text=re.sub(r'\s+',' ',text)
    words=re.findall(r"[A-Za-z][A-Za-z'-]*", text)
    has_quick=bool(re.search(r'<section[^>]*class=["\'][^"\']*quick-answer',html,re.I)) and 'Quick Answer' in text
    has_red='Red Flags / when to slow down before checkout' in text
    faq_ld='FAQPage' in html
    links=[m.group(1) for m in re.finditer(r'<a[^>]+href=["\']([^"\']+)["\']',html,re.I)]
    related_blog=[u for u in links if u.startswith('/blog/') and u not in ['/blog/',f'/blog/{slug}/']]
    product_support=[u for u in links if 'route=product/search' in u or 'route=information/contact' in u]
    auth_links=[u for u in links if any(d in u for d in required_auth)]
    img_m=re.search(r'<img[^>]*class=["\'][^"\']*hero[^"\']*["\'][^>]*>',html,re.I)
    img_tag=img_m.group(0) if img_m else ''
    image_ok=bool(img_tag and attr(img_tag,'src') and attr(img_tag,'alt') and attr(img_tag,'title') and metas(html,'property','og:image') and metas(html,'property','og:image:alt') and metas(html,'name','twitter:image') and metas(html,'name','twitter:image:alt') and 'ImageObject' in html)
    topic_depth=all(term.lower() in html.lower() for term in (['edible','flavored','ingredient','compatibility','pregnancy','cbd'] if slug.startswith('edible') else ['bluetooth','permission','privacy','malware','account','updates']))
    natural=all(marker in text for marker in ['Slow down' if slug.startswith('edible') else 'Pause', 'before checkout']) and len(words)>=1000
    banned_absent=not any(re.search(pat, text, re.I) for pat in banned)
    checks={'title_under_60':len(title)<60,'meta_under_155':len(meta_content)<155,'one_h1':len(h1)==1,'gtag_script_and_config_once':gtag_config==1 and gtag_src==1,'gtag_immediately_after_head':head_after,'word_count_1000_plus':len(words)>=1000,'quick_answer':has_quick,'red_flags':has_red,'faqpage_jsonld':faq_ld,'authority_refs':len(auth_links)>=3,'related_blog_links_2_4':2<=len(set(related_blog))<=8,'product_support_links_1_3':1<=len(set(product_support))<=6,'image_seo_metadata':image_ok,'natural_readability_markers':natural,'topic_specific_depth':topic_depth,'banned_terms_absent':banned_absent}
    score=round(sum(checks.values())/len(checks)*100)
    results[slug]={'title':title,'title_length':len(title),'meta_length':len(meta_content),'h1_count':len(h1),'gtag_occurrences':gtag_config+gtag_src,'word_count':len(words),'checks':checks,'quality_score':score,'authority_links':auth_links[:10],'related_blog_count':len(set(related_blog)),'product_support_count':len(set(product_support))}
# index and sitemap checks
idx=(BLOG/'index.html').read_text(encoding='utf-8')
sm=(ROOT/'upload/sitemap.xml').read_text(encoding='utf-8')
index_ok=all(f'/blog/{s}/' in idx for s in slugs)
sitemap_ok=all(f'{BASE}/blog/{s}/' in sm and DATE in sm and f'{s}-opus-cover.png' in sm and '<image:image>' in sm for s in slugs)
state=json.loads((ROOT/'output/daily_blog_automation_state.json').read_text(encoding='utf-8'))
validation={'status':'pass' if all(r['quality_score']>=85 and all(r['checks'].values()) for r in results.values()) and index_ok and sitemap_ok else 'fail','article_checks':results,'blog_index_links':index_ok,'sitemap_image_metadata':sitemap_ok,'quality_score_min':min(r['quality_score'] for r in results.values()),'readability_natural_english':all(r['checks']['natural_readability_markers'] for r in results.values()),'topic_specific_depth':all(r['checks']['topic_specific_depth'] for r in results.values()),'authority_refs':all(r['checks']['authority_refs'] for r in results.values()),'validated_at':datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat()}
state['local_validation']=validation; state['validated_at']=validation['validated_at']; state['status']='validated_pending_commit_deploy_email' if validation['status']=='pass' else 'validation_failed'
(ROOT/'output/daily_blog_automation_state.json').write_text(json.dumps(state,indent=2),encoding='utf-8')
print(json.dumps(validation,indent=2))
if validation['status']!='pass': raise SystemExit(1)
