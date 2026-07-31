#!/usr/bin/env python3
import json, re, sys, urllib.request
from html.parser import HTMLParser
from urllib.error import HTTPError, URLError

SLUGS = [
    "adult-toys-malware-privacy-checklist",
    "silver-bullet-vibrator-shopping-guide",
]
BASE = "https://shoplovanest.com"

class H1Parser(HTMLParser):
    def __init__(self):
        super().__init__(); self.h1=0; self.title=''; self.in_title=False; self.metas=[]; self.images=[]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag.lower()=="h1": self.h1 += 1
        if tag.lower()=="title": self.in_title=True
        if tag.lower()=="meta": self.metas.append(a)
        if tag.lower()=="img": self.images.append(a)
    def handle_endtag(self, tag):
        if tag.lower()=="title": self.in_title=False
    def handle_data(self, data):
        if self.in_title: self.title += data

def fetch(url):
    req=urllib.request.Request(url, headers={"User-Agent":"ShopLovaNestDailyVerifier/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        body=r.read().decode("utf-8", "replace")
        return r.status, body

def verify_article(slug):
    url=f"{BASE}/blog/{slug}/"
    status, html=fetch(url)
    p=H1Parser(); p.feed(html)
    meta_desc=[m.get('content','') for m in p.metas if m.get('name','').lower()=='description']
    checks={
      "http_200": status==200,
      "title_present": bool(p.title.strip()),
      "meta_description_present": bool(meta_desc and meta_desc[0].strip()),
      "one_h1": p.h1==1,
      "gtag_block_once": html.count("https://www.googletagmanager.com/gtag/js?id=G-P2LJRXN3D1")==1 and html.count("gtag('config', 'G-P2LJRXN3D1')")==1,
      "quick_answer": "Quick Answer" in html,
      "red_flags": "Red Flags" in html,
      "faq_schema": '"FAQPage"' in html,
      "authority_refs": all(x in html for x in (["ftc.gov", "cisa.gov", "bluetooth.com"] if slug.startswith('adult-toys') else ["saferproducts.gov", "ul.com", "tsa.gov"])),
      "image_alt_title": bool(re.search(r'<img[^>]+alt="[^"]+"[^>]+title="[^"]+"', html)),
      "og_image": 'property="og:image"' in html and 'property="og:image:alt"' in html,
      "twitter_image": 'name="twitter:image"' in html and 'name="twitter:image:alt"' in html,
      "jsonld_image": '"ImageObject"' in html,
    }
    return {"url": url, "checks": checks, "pass": all(checks.values())}

def main():
    out={"articles": {slug: verify_article(slug) for slug in SLUGS}}
    st_idx, idx=fetch(f"{BASE}/blog/")
    out["blog_index"]={"http_200": st_idx==200, **{slug: f"/blog/{slug}/" in idx for slug in SLUGS}}
    st_sm, sm=fetch(f"{BASE}/sitemap.xml")
    out["sitemap"]={"http_200": st_sm==200}
    for slug in SLUGS:
        block = re.search(rf"<url>.*?/blog/{re.escape(slug)}/.*?</url>", sm, re.S)
        txt=block.group(0) if block else ""
        out["sitemap"][slug]={
          "url_present": bool(block),
          "lastmod_2026_07_31": "<lastmod>2026-07-31</lastmod>" in txt,
          "image_metadata": "<image:image>" in txt and "<image:loc>" in txt and "<image:title>" in txt and "<image:caption>" in txt,
        }
    out["pass"] = all(a["pass"] for a in out["articles"].values()) and all(out["blog_index"].values()) and out["sitemap"]["http_200"] and all(all(v.values()) for k,v in out["sitemap"].items() if isinstance(v,dict))
    print(json.dumps(out, indent=2, ensure_ascii=False))
    sys.exit(0 if out["pass"] else 1)
if __name__ == "__main__": main()
