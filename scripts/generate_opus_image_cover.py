#!/usr/bin/env python3
from __future__ import annotations
import base64, json, mimetypes, os, re, sys, time, urllib.error, urllib.request
from pathlib import Path

CONFIG = Path('/Users/grant/.openclaw/openclaw.json')
ROOT = Path('/Users/grant/IdeaProjects/myopencart')
ASSETS = ROOT / 'upload' / 'blog' / 'assets'
ASSETS.mkdir(parents=True, exist_ok=True)

def load_provider():
    txt=CONFIG.read_text()
    # openclaw.json is JSON in this install.
    cfg=json.loads(txt)
    p=cfg['models']['providers']['openai']
    return p['baseUrl'].rstrip('/'), p['apiKey']

def prompt_for(title: str, slug: str) -> str:
    low=(title+' '+slug).lower()
    if any(x in low for x in ['lube','lubricant','condom']):
        scene='water-based lubricant bottle, sealed condom packets, water droplets, compatibility checklist card, clean cotton towel, bedside table'
    elif any(x in low for x in ['shipping','privacy','billing','storage','travel','tsa','delivery']):
        scene='plain discreet parcel, lockable storage box, neutral billing card, soft travel pouch, elegant bedroom shelf'
    elif any(x in low for x in ['lingerie','lace','fabric','size']):
        scene='luxury satin and lace lingerie flat-lay, measuring tape, care card, soft champagne bedding'
    elif any(x in low for x in ['clean','dry','cleaner','care']):
        scene='clean intimate wellness product care setup, soft towel, cleaning spray, water droplets, drying tray'
    elif any(x in low for x in ['vibrator','wand','rabbit','bullet','egg','suction','wearable','remote','rechargeable','waterproof','usb','g-spot','mini','palm']):
        scene='sleek premium vibrator-style wellness device silhouette, charging cable, storage pouch, bedside lamp, product box'
    elif any(x in low for x in ['material','silicone','glass','steel','abs','jelly','body-safe','porous','hypoallergenic']):
        scene='body-safe material samples, matte silicone swatch, glass shine, stainless detail, safety checklist card'
    elif any(x in low for x in ['couple','date','gift']):
        scene='tasteful adult wellness gift box, two glasses, candle, consent note card, soft romantic nightstand'
    elif any(x in low for x in ['anal','plug']):
        scene='beginner-safe tapered product silhouette, water-based lubricant, size guide card, clean towel'
    else:
        scene='premium adult wellness product flat-lay, discreet packaging, shopping checklist, soft candle, private bedroom shelf'
    return f'''Create a premium editorial ecommerce cover image for a ShopLovaNest adult wellness blog article titled "{title}". Scene: {scene}. Mature 18+ but non-explicit and policy-safe. Tasteful, slightly bold sensual DTC brand style, warm ivory/cocoa/blush/champagne color palette, photorealistic product photography, soft natural light, high-end female-friendly intimate wellness aesthetic. Show product-relevant objects clearly. No nudity, no visible genitals, no sex act, no explicit posing, no pornographic content, no readable text except abstract label marks. 16:9 composition, website blog hero cover, conversion-friendly and directly relevant to the article topic.'''

def call_image(prompt: str, out: Path, size='1536x1024'):
    base, key = load_provider()
    url = base + '/images/generations'
    payload = {
        'model': 'opus-image-1.5',
        'prompt': prompt,
        'n': 1,
        'size': size,
        'response_format': 'b64_json'
    }
    data=json.dumps(payload).encode()
    req=urllib.request.Request(url, data=data, headers={'Authorization': f'Bearer {key}', 'Content-Type':'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            raw=r.read().decode('utf-8','ignore')
            obj=json.loads(raw)
    except urllib.error.HTTPError as e:
        body=e.read().decode('utf-8','ignore')[:2000]
        raise RuntimeError(f'HTTP {e.code} from custom opus-image-1.5 endpoint: {body}')
    item=obj.get('data',[{}])[0]
    if item.get('b64_json'):
        b=base64.b64decode(item['b64_json'])
        out.write_bytes(b)
        return out
    if item.get('url'):
        with urllib.request.urlopen(item['url'], timeout=120) as r:
            out.write_bytes(r.read())
        return out
    raise RuntimeError('No b64_json/url in image response: '+json.dumps(obj)[:1000])

def main():
    slug=sys.argv[1]
    title=' '.join(sys.argv[2:]) or slug.replace('-',' ').title()
    out=ASSETS/f'{slug}-opus-cover.png'
    call_image(prompt_for(title, slug), out)
    print(out)

if __name__=='__main__': main()
