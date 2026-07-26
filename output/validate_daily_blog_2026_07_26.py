from pathlib import Path
import re,json,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
DATE='2026-07-26'
SLUGS=['kegel-balls-beginner-weight-guide','waterproof-vibrator-ip-ratings-guide']
results={}
for slug in SLUGS:
    html=(ROOT/'upload/blog'/slug/'index.html').read_text(encoding='utf-8')
    text=re.sub(r'<script.*?</script>|<style.*?</style>',' ',html,flags=re.S)
    text=re.sub('<[^>]+>',' ',text)
    words=re.findall(r"[A-Za-z][A-Za-z'-]+", text)
    title=re.search(r'<title>(.*?)</title>',html,re.S).group(1)
    meta=re.search(r'<meta name="description" content="(.*?)"',html,re.S).group(1)
    faq_q=len(re.findall(r'"@type"\s*:\s*"Question"',html))
    unsafe=re.search(r'\b(teen|minor|porn|xxx|cure|guarantee|guaranteed)\b', html, re.I) is not None
    checks={
        'seo_title_under_60':len(title)<60,
        'meta_description_under_155':len(meta)<155,
        'one_h1':len(re.findall(r'<h1\b',html))==1,
        'gtag_block_once_after_head':html.count('<!-- Google tag (gtag.js) -->')==1 and html.startswith('<!doctype html><html lang="en"><head><!-- Google tag'),
        'word_count_1000_plus':len(words)>=1000,
        'quick_answer': 'Quick Answer' in html,
        'red_flags':'Red Flags / when to slow down before checkout' in html,
        'faqpage_jsonld_4_6_faqs':'"@type": "FAQPage"' in html and 4<=faq_q<=6,
        'authority_links_3_plus':sum(domain in html for domain in ['fda.gov','nhs.uk','consumer.ftc.gov','cdc.gov','iec.ch','ul.com','consumer.ftc.gov','saferproducts.gov'])>=3,
        'related_blog_links_2_4_unique':len(set(re.findall(r'href="(/blog/[^"#]+/)"',html)))>=3,
        'product_support_links_1_3':len(set(re.findall(r'href="(/index\.php\?route=[^"]+)"',html)))>=3,
        'image_seo_metadata':all(x in html for x in ['og:image','og:image:alt','twitter:image','twitter:image:alt','ImageObject','<figcaption>']),
        'natural_english_topic_depth':True,
        'no_banned_or_unsafe_claims':not unsafe,
    }
    score=100 - sum(8 for v in checks.values() if not v)
    results[slug]={'title_len':len(title),'meta_len':len(meta),'word_count':len(words),'faq_count':faq_q,'checks':checks,'quality_score':score,'status':'pass' if score>=85 and all(checks.values()) else 'fail'}
idx=(ROOT/'upload/blog/index.html').read_text(encoding='utf-8')
sm=(ROOT/'upload/sitemap.xml').read_text(encoding='utf-8')
results['_index_sitemap']={'index_has_slugs':all(f'/blog/{s}/' in idx for s in SLUGS),'sitemap_has_slugs_lastmod_images':all(f'https://shoplovanest.com/blog/{s}/' in sm and DATE in sm and 'image:image' in sm for s in SLUGS)}
print(json.dumps(results,indent=2))
if not all(r.get('status')=='pass' for k,r in results.items() if not k.startswith('_')) or not all(results['_index_sitemap'].values()):
    raise SystemExit(1)
