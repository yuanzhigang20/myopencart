from pathlib import Path
import json,re,xml.etree.ElementTree as ET
ROOT=Path('/Users/grant/IdeaProjects/myopencart'); DATE='2026-08-03'; BASE='https://shoplovanest.com'
slugs=['natural-water-based-lube-guide','cock-and-ball-ring-safety-guide']
results=[]
banned=['porn','xxx','teen','minor','child','cure erectile dysfunction','treat erectile dysfunction','guaranteed orgasm','guaranteed performance','fertility cure']
for slug in slugs:
 p=ROOT/'upload/blog'/slug/'index.html'; html=p.read_text(encoding='utf-8'); text=re.sub(r'<script.*?</script>|<style.*?</style>',' ',html,flags=re.S); text=re.sub(r'<[^>]+>',' ',text); text=re.sub(r'\s+',' ',text).strip(); words=re.findall(r"\b[A-Za-z][A-Za-z'-]*\b", text)
 mt=re.search(r'<title>(.*?)</title>',html,re.S); title=(mt.group(1).strip() if mt else '')
 mm=re.search(r'<meta name="description" content="(.*?)"',html,re.S); meta=(mm.group(1) if mm else '')
 h1=re.findall(r'<h1[\s>].*?</h1>',html,re.S)
 gtag_script=html.count('https://www.googletagmanager.com/gtag/js?id=G-P2LJRXN3D1')
 gtag_config=html.count("gtag('config', 'G-P2LJRXN3D1')")
 head_immediate=html.startswith('<!doctype html><html lang="en"><head><!-- Google tag') or '<head><!-- Google tag' in html[:80]
 faq_schema='"@type": "FAQPage"' in html or '"@type":"FAQPage"' in html
 qa=('Quick Answer' in html)
 red=('Red Flags / when to slow down before checkout' in html)
 hero=re.search(r'<img class="hero"[^>]+>',html); hero_tag=hero.group(0) if hero else ''
 img_meta=all(['property="og:image"' in html, 'property="og:image:alt"' in html, 'name="twitter:image"' in html, 'name="twitter:image:alt"' in html, ' alt="' in hero_tag and ' title="' in hero_tag, 'ImageObject' in html, '<figcaption>' in html])
 related_match=re.findall(r'<div class="related">.*?</div>',html,re.S)
 related_count=(related_match[0].count('<a href="/blog/') if related_match else 0)
 prod_count=len(re.findall(r'<li><a href="/index.php',html))
 refs_match=re.findall(r'<section class="content-card refs">.*?</section>',html,re.S)
 refs_count=(refs_match[0].count('href="http') if refs_match else 0)
 useful_checks=[len(title)<60,len(meta)<155,len(h1)==1,gtag_script==1,gtag_config==1,head_immediate,len(words)>=1000,qa,red,faq_schema,refs_count>=3,related_count>=2,prod_count>=1,img_meta,not any(b in text.lower() for b in banned)]
 score=70+sum(useful_checks)*2
 if len(words)>=1200: score+=3
 if refs_count>=4: score+=2
 if related_count>=4: score+=1
 score=min(score,100)
 results.append({'slug':slug,'title':title,'title_len':len(title),'meta_len':len(meta),'h1_count':len(h1),'gtag_script_count':gtag_script,'gtag_config_count':gtag_config,'gtag_immediately_after_head':head_immediate,'word_count':len(words),'quick_answer':qa,'red_flags':red,'faq_schema':faq_schema,'authority_refs':refs_count,'related_blog_links':related_count,'product_support_links':prod_count,'image_seo_metadata':img_meta,'banned_scan_pass':not any(b in text.lower() for b in banned),'quality_score':score,'pass':all(useful_checks) and score>=85})
sm=ROOT/'upload/sitemap.xml'; tree=ET.parse(sm); root=tree.getroot(); ns='{http://www.sitemaps.org/schemas/sitemap/0.9}'; ins='{http://www.google.com/schemas/sitemap-image/1.1}'
sitemap=[]
for slug in slugs:
 loc=BASE+'/blog/'+slug+'/'; found=False; ok=False
 for u in root.findall(ns+'url'):
  l=u.find(ns+'loc')
  if l is not None and l.text==loc:
   found=True; last=u.find(ns+'lastmod'); im=u.find(ins+'image')
   ok=(last is not None and last.text==DATE and im is not None and im.find(ins+'loc') is not None and im.find(ins+'title') is not None and im.find(ins+'caption') is not None)
 sitemap.append({'url':loc,'found':found,'lastmod_image_metadata_pass':ok})
index=(ROOT/'upload/blog/index.html').read_text(encoding='utf-8')
index_checks={'blog_index_links':[slug in index for slug in slugs],'blog_index_gtag_script_count':index.count('https://www.googletagmanager.com/gtag/js?id=G-P2LJRXN3D1'),'blog_index_gtag_config_count':index.count("gtag('config")} 
out={'date':DATE,'articles':results,'sitemap':sitemap,'index':index_checks,'overall_pass':all(r['pass'] for r in results) and all(s['lastmod_image_metadata_pass'] for s in sitemap) and all(index_checks['blog_index_links'])}
(ROOT/'output/daily_blog_validation_2026-08-03.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2))
raise SystemExit(0 if out['overall_pass'] else 1)
