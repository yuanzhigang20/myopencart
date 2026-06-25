#!/usr/bin/env python3
from pathlib import Path
import re, html, json
ROOT=Path('/Users/grant/IdeaProjects/myopencart')
files=list((ROOT/'upload/blog').glob('*/index.html'))+[ROOT/'upload/blog/index.html']
banned=re.compile(r'\b(teen|minor|underage|child|schoolgirl|porn|porno|xxx|nude|onlyfans|leaked|rape|forced|incest|bestiality|zoophilia|drug|crack|hack|pirate|torrent|free download|toy story|disney|barbie|adam\s*&?\s*eve|amazon|target|walmart|etsy|mcdonald)\b',re.I)
fail=[]; rows=[]
new_slugs={
'app-controlled-adult-toys','remote-control-adult-toys','wearable-vibrator-guide','suction-massager-guide','g-spot-vibrator-guide','glass-adult-toys-guide','stainless-steel-adult-toys','abs-plastic-adult-toys','jelly-adult-toys-red-flags','silicone-vs-abs-adult-toys','non-porous-sex-toys-guide','hypoallergenic-adult-toys','sex-toy-cleaning-mistakes','how-to-dry-adult-toys','adult-toy-storage-box-guide','lockable-adult-toy-storage','travel-size-adult-toys','tsa-adult-toys-travel-guide','discreet-billing-adult-toys','adult-toy-delivery-guide','adult-toy-returns-guide','adult-toy-warranty-guide','first-vibrator-questions','mini-vibrator-guide','palm-vibrator-guide','egg-vibrator-guide','wand-attachments-guide','rechargeable-vs-battery-vibrators','usb-charging-adult-toys','waterproof-vs-water-resistant-toys','quiet-adult-toys-shared-home','adult-toys-for-couples-beginners','couples-vibrator-guide','date-night-adult-toy-gift','luxury-adult-toys-guide','budget-adult-toys-guide','lubricant-ingredients-guide','sensitive-skin-lube-guide','anal-lube-guide','toy-compatible-lube-guide','massage-oil-vs-lube','kegel-balls-sizing-guide','kegel-balls-cleaning-storage','anal-plug-size-guide','anal-toy-flared-base','male-masturbator-cleaning','male-masturbator-materials','lingerie-size-guide','plus-size-lingerie-buying-guide','lace-lingerie-care-guide'}
for p in files:
    s=p.read_text(encoding='utf-8')
    rel=str(p.relative_to(ROOT))
    if not s.lstrip().lower().startswith('<!doctype html>'): fail.append((rel,'doctype'))
    title=re.search(r'<title>(.*?)</title>',s,re.S)
    desc=re.search(r'<meta name="description" content="([^"]*)"',s,re.S)
    h1=len(re.findall(r'<h1\b',s,re.I))
    g=s.count('G-P2LJRXN3D1')
    # exactly one Google tag block = one gtag js id occurrence and one config occurrence -> current pattern has 2 id refs. Validate no duplicates by requiring count 2.
    if not title or len(html.unescape(re.sub('<.*?>','',title.group(1))).strip())>60: fail.append((rel,'title length'))
    if not desc or len(html.unescape(desc.group(1)))>155: fail.append((rel,'meta length'))
    if h1!=1: fail.append((rel,f'h1 {h1}'))
    if g!=2: fail.append((rel,f'gtag refs {g}'))
    hit=banned.search(s)
    if hit: fail.append((rel,f'banned {hit.group(0)}'))
    words=len(re.findall(r'\b[A-Za-z][A-Za-z\'-]*\b', re.sub('<[^>]+>',' ',s)))
    if '/index.html' in rel and Path(rel).parts[-2] in new_slugs and words<1000: fail.append((rel,f'words {words}'))
    rows.append((rel,words,len(html.unescape(re.sub('<.*?>','',title.group(1))).strip()) if title else 0,len(html.unescape(desc.group(1))) if desc else 0,g))
print('files',len(files),'failures',len(fail))
for f in fail[:100]: print('FAIL',f)
print('new article min words',min(w for rel,w,_,_,_ in rows if len(Path(rel).parts)>2 and Path(rel).parts[-2] in new_slugs))
raise SystemExit(1 if fail else 0)
