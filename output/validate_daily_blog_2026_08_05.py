from pathlib import Path
import re,json,xml.etree.ElementTree as ET
ROOT=Path('/Users/grant/IdeaProjects/myopencart'); DATE='2026-08-05'; BASE='https://shoplovanest.com'
slugs=['adjustable-cock-ring-sizing-guide','wand-massager-attachments-guide']
refs=['fda.gov','cdc.gov','ftc.gov','cpsc.gov','clevelandclinic.org','nhs.uk','iec.ch']
def strip_tags(h): return re.sub(r'<[^>]+>',' ',h)
results=[]
for slug in slugs:
 html=(ROOT/'upload/blog'/slug/'index.html').read_text(encoding='utf-8'); text=strip_tags(html); words=re.findall(r"\b[A-Za-z][A-Za-z'-]*\b", text)
 title=(re.search(r'<title>(.*?)</title>',html,re.S).group(1) if re.search(r'<title>(.*?)</title>',html,re.S) else '').strip()
 mm=re.search(r'<meta name="description" content="([^"]*)"',html); meta=mm.group(1) if mm else ''
 h1=len(re.findall(r'<h1\b',html)); faq_h3=len(re.findall(r'<h3>[^<]*\?',html)); blog_links=len(re.findall(r'<a href="/blog/(?!")',html)); prod_links=len(re.findall(r'route=product/search',html))
 checks={
  'title_under_60':len(title)<60,'meta_under_155':len(meta)<155,'exactly_one_h1':h1==1,
  'gtag_once':html.count('gtag/js?id=G-P2LJRXN3D1')==1 and html.count("gtag('config', 'G-P2LJRXN3D1')")==1 and html.index('<head>') < html.index('G-P2LJRXN3D1') < html.index('<meta charset'),
  'word_count_1000_plus':len(words)>=1000,'quick_answer':'class="quick-answer"' in html and 'Quick Answer' in text,'red_flags':'Red Flags / when to slow down before checkout' in text,
  'faq_count_4_6':4<=faq_h3<=6,'faq_schema':'FAQPage' in html,'related_blog_links_2_4':blog_links>=2,'product_links_1_3':prod_links>=1,
  'authority_refs':sum(1 for r in refs if r in html)>=2,'image_metadata':all(x in html for x in ['class="hero"','alt="','title="','<figcaption>','og:image','og:image:alt','twitter:image','twitter:image:alt','ImageObject']),
  'adult_safe_language':not re.search(r'\b(teen|minor|xxx|porn|cure|treats|guaranteed hardness|fertility)\b', text, re.I),'natural_english_depth': all(k in text for k in ['Red Flags','References and useful sources','Shop and learn next'])}
 score=round(sum(checks.values())/len(checks)*100)
 results.append({'slug':slug,'title':title,'title_len':len(title),'meta_len':len(meta),'word_count':len(words),'quality_score':score,'checks':checks})
index=(ROOT/'upload/blog/index.html').read_text(encoding='utf-8')
root=ET.parse(ROOT/'upload/sitemap.xml').getroot(); ns='{http://www.sitemaps.org/schemas/sitemap/0.9}'; ins='{http://www.google.com/schemas/sitemap-image/1.1}'
sitemap={}
for u in root.findall(ns+'url'):
 loc=u.findtext(ns+'loc')
 if loc: sitemap[loc]={'lastmod':u.findtext(ns+'lastmod'),'images':len(u.findall(ins+'image'))}
for r in results:
 slug=r['slug']; url=f'{BASE}/blog/{slug}/'
 r['index_link_present']=f'/blog/{slug}/' in index; r['sitemap_url_present']=url in sitemap; r['sitemap_lastmod_today']=sitemap.get(url,{}).get('lastmod')==DATE; r['sitemap_image_metadata']=sitemap.get(url,{}).get('images',0)>=1
 r['passed']=r['quality_score']>=85 and all(r['checks'].values()) and r['index_link_present'] and r['sitemap_url_present'] and r['sitemap_lastmod_today'] and r['sitemap_image_metadata']
out={'date':DATE,'results':results,'all_passed':all(r['passed'] for r in results)}
(ROOT/'output/daily_blog_validation_2026-08-05.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
# merge into state
state_path=ROOT/'output/daily_blog_automation_state.json'
state=json.loads(state_path.read_text(encoding='utf-8'))
state['content_quality_validation']=out
state['status']='validated_pending_commit' if out['all_passed'] else 'validation_failed'
state_path.write_text(json.dumps(state,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2)); raise SystemExit(0 if out['all_passed'] else 1)
