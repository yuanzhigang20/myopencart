#!/usr/bin/env python3
from __future__ import annotations
import base64, json, re, time, urllib.request, urllib.error, html, argparse
from pathlib import Path
ROOT=Path('/Users/grant/IdeaProjects/myopencart')
CONFIG=Path('/Users/grant/.openclaw/openclaw.json')
BLOG=ROOT/'upload'/'blog'
ASSETS=BLOG/'assets'
STATE=ROOT/'output'/'opus_image_generation_state_2026-06-26.json'
PRIORITY=['water-based-lube-condom-guide','sex-toys-for-beginners','best-adult-toys-for-beginners','body-safe-sex-toys','discreet-shipping-adult-toys','vibrators-for-beginners','quiet-vibrator-guide','water-based-lube-guide','how-to-clean-silicone-sex-toys','adult-toy-buying-guide','rabbit-vibrator-guide','male-masturbator-guide','adult-toys-for-couples']

def provider():
    cfg=json.loads(CONFIG.read_text())
    p=cfg['models']['providers']['openai']
    return p['baseUrl'].rstrip('/'), p['apiKey']

def title_for(slug):
    p=BLOG/slug/'index.html'
    t=p.read_text(errors='ignore')
    m=re.search(r'<h1[^>]*>(.*?)</h1>',t,re.S|re.I)
    return html.unescape(re.sub('<[^>]+>','',m.group(1))).strip() if m else slug.replace('-',' ').title()

def scene_for(slug,title):
    low=(slug+' '+title).lower()
    if any(x in low for x in ['lube','lubricant','condom']): return 'water-based lubricant bottle, sealed condom packets, water droplets, clean towel, compatibility checklist card, elegant nightstand'
    if any(x in low for x in ['shipping','privacy','billing','storage','travel','tsa','delivery']): return 'plain discreet parcel, lockable storage box, neutral billing card, travel pouch, elegant bedroom shelf'
    if any(x in low for x in ['lingerie','lace','fabric','size']): return 'luxury satin and lace lingerie flat-lay, measuring tape, care card, champagne bedding'
    if any(x in low for x in ['clean','dry','cleaner','care']): return 'clean intimate wellness product care setup, soft towel, cleaning spray, water droplets, drying tray'
    if any(x in low for x in ['vibrator','wand','rabbit','bullet','egg','suction','wearable','remote','rechargeable','waterproof','usb','g-spot','mini','palm']): return 'sleek premium vibrator-style wellness device silhouette, charging cable, storage pouch, bedside lamp, product box'
    if any(x in low for x in ['material','silicone','glass','steel','abs','jelly','body-safe','porous','hypoallergenic']): return 'body-safe material samples, matte silicone swatch, glass shine, stainless detail, safety checklist card'
    if any(x in low for x in ['couple','date','gift']): return 'tasteful adult wellness gift box, two glasses, candle, consent note card, soft romantic nightstand'
    if any(x in low for x in ['anal','plug']): return 'beginner-safe tapered product silhouette, water-based lubricant, size guide card, clean towel'
    return 'premium adult wellness product flat-lay, discreet packaging, shopping checklist, soft candle, private bedroom shelf'

def prompt(slug,title,kind):
    scene=scene_for(slug,title)
    purpose={'cover':'website blog hero cover','guide-1':'in-article visual checklist','detail-1':'in-article product detail and care visual'}[kind]
    return f'''Create a premium photorealistic {purpose} for ShopLovaNest adult wellness article titled "{title}". Scene: {scene}. Mature 18+ but non-explicit and policy-safe. Tasteful but bolder sensual ecommerce styling, high-end female-friendly DTC intimate wellness brand, warm ivory/cocoa/blush/champagne palette, soft natural light, luxury bathroom or nightstand flat-lay. Show objects clearly and make them directly relevant to the topic. No nudity, no visible genitals, no sex act, no explicit posing, no pornographic content, no readable text except abstract label marks. 16:9 composition, editorial product photography, conversion-friendly.'''

def call_opus(prompt_text):
    base,key=provider(); url=base+'/responses'
    payload={'model':'opus-image-1.5','input':prompt_text,'tools':[{'type':'image_generation'}]}
    headers={'Authorization':'Bearer '+key,'Content-Type':'application/json','User-Agent':'OpenAI/Python 1.0.0','Accept':'application/json'}
    req=urllib.request.Request(url,data=json.dumps(payload).encode(),headers=headers)
    try:
        with urllib.request.urlopen(req,timeout=300) as r:
            obj=json.loads(r.read().decode('utf-8','ignore'))
    except urllib.error.HTTPError as e:
        raise RuntimeError(f'HTTP {e.code}: '+e.read().decode('utf-8','ignore')[:1000])
    # Find image_generation_call result base64.
    for item in obj.get('output',[]):
        if item.get('type')=='image_generation_call' and item.get('result'):
            return base64.b64decode(item['result'])
    # Some gateways return nested content.
    raw=json.dumps(obj)[:1500]
    raise RuntimeError('No image result in response: '+raw)

def patch_html(slug, kind, filename):
    p=BLOG/slug/'index.html'; t=p.read_text(errors='ignore')
    if kind=='cover':
        t=t.replace(f'/blog/assets/{slug}-cover.svg', f'/blog/assets/{filename}')
    else:
        t=t.replace(f'/blog/assets/{slug}-{kind}.svg', f'/blog/assets/{filename}')
    p.write_text(t)

def load_state():
    if STATE.exists(): return json.loads(STATE.read_text())
    return {'done':[],'failed':[]}

def save_state(s): STATE.write_text(json.dumps(s,ensure_ascii=False,indent=2))

def generate(slug,kinds):
    title=title_for(slug)
    made=[]
    for kind in kinds:
        out=ASSETS/f'{slug}-opus-{kind}.png'
        if out.exists() and out.stat().st_size>10000:
            patch_html(slug,kind,out.name); made.append(str(out)); continue
        data=call_opus(prompt(slug,title,kind))
        out.write_bytes(data)
        patch_html(slug,kind,out.name)
        made.append(str(out))
        time.sleep(1)
    return made

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--all',action='store_true'); ap.add_argument('--limit',type=int,default=0); ap.add_argument('--kinds',default='cover'); ap.add_argument('slugs',nargs='*')
    a=ap.parse_args(); kinds=[x.strip() for x in a.kinds.split(',') if x.strip()]
    if a.slugs: slugs=a.slugs
    elif a.all: slugs=PRIORITY+[p.parent.name for p in sorted(BLOG.glob('*/index.html')) if p.parent.name not in PRIORITY]
    else: slugs=PRIORITY
    if a.limit: slugs=slugs[:a.limit]
    st=load_state()
    for slug in slugs:
        key=slug+':'+'/'.join(kinds)
        if key in st['done']: continue
        try:
            made=generate(slug,kinds)
            st['done'].append(key); save_state(st)
            print('OK',slug,made,flush=True)
        except Exception as e:
            st['failed'].append({'slug':slug,'kinds':kinds,'error':str(e)[:1000]}); save_state(st)
            print('FAIL',slug,e,flush=True)
            # continue to next; transient failures logged.
if __name__=='__main__': main()
