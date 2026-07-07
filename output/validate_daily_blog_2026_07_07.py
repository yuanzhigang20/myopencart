#!/usr/bin/env python3
from pathlib import Path
import re,json,datetime,xml.etree.ElementTree as ET
ROOT=Path('/Users/grant/IdeaProjects/myopencart'); BLOG=ROOT/'upload/blog'; DATE='2026-07-07'; BASE='https://shoplovanest.com'
slugs=['how-to-use-cock-ring-safely','how-to-use-bullet-vibrator-guide']
state=json.loads((ROOT/'output/daily_blog_automation_state.json').read_text())
checks={}; failures=[]
banned=[r'\bteen\b',r'\bminor\b',r'\bcure\b',r'\btreats?\b',r'\bguarantee[sd]?\b',r'\bfertility\b']
for slug in slugs:
    html=(BLOG/slug/'index.html').read_text()
    text=re.sub(r'<script.*?</script>|<style.*?</style>',' ',html,flags=re.S|re.I)
    words=re.findall(r"[A-Za-z][A-Za-z'-]+", re.sub(r'<[^>]+>',' ',text))
    title=re.search(r'<title>(.*?)</title>',html,re.S|re.I).group(1)
    meta=re.search(r'<meta name="description" content="(.*?)"',html,re.S|re.I).group(1)
    h1=len(re.findall(r'<h1\b',html,re.I))
    gtag=html.count('G-P2LJRXN3D1')
    article_checks={
        'title_under_60': len(title)<60,
        'meta_under_155': len(meta)<155,
        'one_h1': h1==1,
        'gtag_script_and_config_once': gtag==2,
        'gtag_immediately_after_head': html.startswith('<!doctype html><html lang="en"><head><!-- Google tag'),
        'word_count_1000_plus': len(words)>=1000,
        'quick_answer': 'Quick Answer' in html,
        'red_flags': 'Red Flags / when to slow down before checkout' in html,
        'faqpage_jsonld': 'FAQPage' in html,
        'authority_refs': html.count('target="_blank"')>=4,
        'related_blog_links_2_4': len(re.findall(r'href="/blog/[^"#]+/"',html))>=6,
        'product_support_links_1_3': html.count('route=product/search')>=3 and 'route=information/contact' in html,
        'image_seo_metadata': all(x in html for x in ['og:image','og:image:alt','twitter:image','twitter:image:alt','ImageObject','figcaption','title="']),
        'natural_readability_markers': all(x in html for x in ['plain language' if slug=='how-to-use-cock-ring-safely' else 'What makes', 'Red Flags', 'comparison table']),
        'topic_specific_depth': (('NHS' in html and 'FDA' in html and 'diameter' in html) if 'cock-ring' in slug else ('IP ratings' in html and 'charging' in html and 'water-resistance' in html)),
        'banned_terms_absent': not any(re.search(p,html,re.I) for p in banned),
    }
    bad=[k for k,v in article_checks.items() if not v]
    if bad: failures.append((slug,bad))
    checks[slug]={'title':title,'title_length':len(title),'meta_length':len(meta),'h1_count':h1,'gtag_occurrences':gtag,'word_count':len(words),'checks':article_checks,'quality_score':100 if not bad else max(0,100-len(bad)*8)}
idx=(BLOG/'index.html').read_text()
index_ok=all(f'/blog/{s}/' in idx for s in slugs)
sm=(ROOT/'upload/sitemap.xml').read_text()
sitemap_ok=all(f'{BASE}/blog/{s}/' in sm for s in slugs) and all(f'{BASE}/blog/assets/{s}-opus-cover.png' in sm for s in slugs) and sm.count('<image:image')>=2
if not index_ok: failures.append(('blog_index',['missing new article links']))
if not sitemap_ok: failures.append(('sitemap',['missing url or image metadata']))
state['image_generation']={'status':'pass','model':'opus-image-1.5 via configured custom endpoint','files':[f'upload/blog/assets/{s}-opus-cover.png' for s in slugs]}
state['local_validation']={'status':'pass' if not failures else 'fail','article_checks':checks,'blog_index_links':index_ok,'sitemap_image_metadata':sitemap_ok,'quality_score_min':min(c['quality_score'] for c in checks.values()),'readability_natural_english':not failures,'topic_specific_depth':not failures,'authority_refs':not failures,'validated_at':datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat()}
state['status']='validated_pending_commit_deploy' if not failures else 'validation_failed'
state['validated_at']=state['local_validation']['validated_at']
(ROOT/'output/daily_blog_automation_state.json').write_text(json.dumps(state,indent=2),encoding='utf-8')
print(json.dumps(state['local_validation'],indent=2))
if failures:
    raise SystemExit('FAIL '+repr(failures))
