from pathlib import Path
from html.parser import HTMLParser
import re,json,xml.etree.ElementTree as ET
ROOT=Path('/Users/grant/IdeaProjects/myopencart'); DATE='2026-07-29'; BASE='https://shoplovanest.com'
class P(HTMLParser):
 def __init__(self): super().__init__(); self.tags=[]; self.text=[]; self.title=''; self._in_title=False; self.metas=[]; self.links=[]; self.imgs=[]; self.h1=0; self.h3=0
 def handle_starttag(self,tag,attrs):
  d=dict(attrs); self.tags.append((tag,d))
  if tag=='title': self._in_title=True
  if tag=='meta': self.metas.append(d)
  if tag=='a': self.links.append(d.get('href',''))
  if tag=='img': self.imgs.append(d)
  if tag=='h1': self.h1+=1
  if tag=='h3': self.h3+=1
 def handle_endtag(self,tag):
  if tag=='title': self._in_title=False
 def handle_data(self,data):
  self.text.append(data)
  if self._in_title: self.title+=data
 def get_text(self): return ' '.join(t.strip() for t in self.text if t.strip())
state=json.loads((ROOT/'output/daily_blog_automation_state.json').read_text()); slugs=[a['slug'] for a in state['articles']]
results=[]; banned=['minor','underage','teen','medical grade','cure','treat infertility','guaranteed orgasm']
for slug in slugs:
 html=(ROOT/'upload/blog'/slug/'index.html').read_text(encoding='utf-8'); p=P(); p.feed(html); text=p.get_text(); words=re.findall(r"\b[\w'-]+\b",text)
 meta_content=next((m.get('content','') for m in p.metas if m.get('name')=='description'),'')
 refs=[h for h in p.links if h.startswith('https://')]
 related=[h for h in p.links if h.startswith('/blog/') and h != f'/blog/{slug}/']
 prod=[h for h in p.links if h.startswith('/index.php')]
 hero=next((i for i in p.imgs if i.get('class')=='hero'),{})
 image_ok=bool(hero.get('alt') and hero.get('title') and any(m.get('property')=='og:image' for m in p.metas) and any(m.get('property')=='og:image:alt' for m in p.metas) and any(m.get('name')=='twitter:image' for m in p.metas) and 'ImageObject' in html)
 banned_hits=[b for b in banned if b in text.lower()]
 checks={'title_len':10<len(p.title.strip())<60,'meta_len':80<len(meta_content)<155,'h1_one':p.h1==1,'gtag_once':html.count('G-P2LJRXN3D1')==2 and html.index('G-P2LJRXN3D1')<html.index('<meta charset'),'word_count':len(words)>=1000,'quick_answer':'Quick Answer' in text,'red_flags':'Red Flags / when to slow down before checkout' in text,'faq_schema':'FAQPage' in html and p.h3>=4,'authority_refs':len(refs)>=3 and all(u.startswith('https://') for u in refs),'internal_links':len(set(related))>=2,'product_links':len(set(prod))>=1,'image_seo':image_ok,'no_banned':not banned_hits,'topic_depth':all(x in text for x in ['Red Flags','FAQ','References and useful sources'])}
 score=round(sum(checks.values())/len(checks)*100)
 results.append({'slug':slug,'title_len':len(p.title.strip()),'meta_len':len(meta_content),'h1_count':p.h1,'gtag_id_occurrences':html.count('G-P2LJRXN3D1'),'words':len(words),'authority_refs':refs,'related_blog_links':len(set(related)),'product_links':len(set(prod)),'image_seo':image_ok,'banned_hits':banned_hits,'checks':checks,'quality_score':score,'status':'pass' if score>=85 and all(checks.values()) else 'fail'})
sm=ET.parse(ROOT/'upload/sitemap.xml').getroot(); ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9','image':'http://www.google.com/schemas/sitemap-image/1.1'}; sitemap={}
for slug in slugs+['']:
 loc=BASE+'/blog/'+(slug+'/' if slug else '')
 node=None
 for u in sm.findall('s:url',ns):
  l=u.find('s:loc',ns)
  if l is not None and l.text==loc: node=u; break
 if node is not None: sitemap[loc]={'lastmod':(node.find('s:lastmod',ns).text if node.find('s:lastmod',ns) is not None else None),'image_count':len(node.findall('image:image',ns))}
report={'date':DATE,'articles':results,'sitemap':sitemap,'all_pass':all(r['status']=='pass' for r in results) and all(BASE+'/blog/'+s+'/' in sitemap and sitemap[BASE+'/blog/'+s+'/']['lastmod']==DATE and sitemap[BASE+'/blog/'+s+'/']['image_count']>=1 for s in slugs) and sitemap.get(BASE+'/blog/',{}).get('lastmod')==DATE}
(ROOT/'output/daily_blog_validation_2026-07-29.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
if not report['all_pass']: raise SystemExit(1)
