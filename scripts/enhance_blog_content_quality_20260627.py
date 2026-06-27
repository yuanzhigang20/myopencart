#!/usr/bin/env python3
from __future__ import annotations
import re, html
from pathlib import Path
from datetime import date

ROOT = Path('/Users/grant/IdeaProjects/myopencart')
BLOG = ROOT / 'upload' / 'blog'
SITEMAP = ROOT / 'upload' / 'sitemap.xml'
TODAY = '2026-06-27'

REFS = {
    'iec': ('International Electrotechnical Commission IP ratings', 'https://www.iec.ch/ip-ratings'),
    'ipwiki': ('IP Code overview', 'https://en.wikipedia.org/wiki/IP_code'),
    'fda': ('FDA biocompatibility resource center', 'https://www.fda.gov/medical-devices/premarket-submissions-selecting-and-preparing-correct-submission/biocompatibility-assessment-resource-center'),
    'cpsc': ('U.S. Consumer Product Safety Commission', 'https://www.cpsc.gov/'),
    'cdc': ('CDC sexual health resources', 'https://www.cdc.gov/sexual-health/'),
    'nhs': ('NHS sexual health information', 'https://www.nhs.uk/live-well/sexual-health/'),
    'pp': ('Planned Parenthood sexual health education', 'https://www.plannedparenthood.org/learn'),
    'tsa': ('TSA What Can I Bring?', 'https://www.tsa.gov/travel/security-screening/whatcanibring/all'),
    'ftc': ('FTC shopping online guidance', 'https://consumer.ftc.gov/articles/how-shop-online-safely'),
}

def esc(s: str) -> str:
    return html.escape(s, quote=True)

def title_from_html(src: str, slug: str) -> str:
    m = re.search(r'<h1[^>]*>(.*?)</h1>', src, re.I|re.S)
    if m:
        return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', html.unescape(m.group(1)))).strip()
    return slug.replace('-', ' ').title()

def category(slug: str, title: str) -> str:
    s = f'{slug} {title}'.lower()
    if any(x in s for x in ['waterproof','water-resistant','water resistant','usb','rechargeable','battery']): return 'waterproof'
    if any(x in s for x in ['wearable','app-controlled','app controlled','remote-control','remote control','egg vibrator','couples vibrator']): return 'wearable'
    if any(x in s for x in ['material','silicone','abs','glass','stainless','jelly','non-porous','hypoallergenic']): return 'materials'
    if any(x in s for x in ['lube','lubricant','massage-oil']): return 'lube'
    if any(x in s for x in ['clean','dry','storage','cleaner']): return 'cleaning'
    if any(x in s for x in ['travel','tsa','delivery','shipping','billing','privacy','returns','warranty']): return 'privacy'
    if any(x in s for x in ['kegel','anal','plug']): return 'fit'
    if any(x in s for x in ['lingerie','lace','size guide','fabric']): return 'lingerie'
    if any(x in s for x in ['beginner','first','buying guide','gift','couples','date night']): return 'beginner'
    if any(x in s for x in ['quiet','shared home']): return 'privacy'
    return 'general'

def topic_pack(cat: str, title: str):
    t = title
    if cat == 'waterproof':
        return {
            'quick_h2': 'Quick answer: waterproof, water-resistant, and safe cleaning',
            'lede': f'If you are comparing {t.lower()}, look past broad marketing words and check what the product can actually tolerate. The practical questions are simple: can it be wiped, rinsed, used in the shower, or temporarily submerged, and what does the charging design allow?',
            'quick': 'Water-resistant usually means limited moisture exposure such as splashes or light rinsing. Waterproof should mean stronger protection, but the claim is only useful when the product page explains the IP rating, charging-port seal, cleaning limits, and drying instructions.',
            'deep_h2': 'How to verify water claims before buying',
            'deep': ['Look for a specific rating such as IPX4, IPX7, or IPX8 instead of relying only on the word “waterproof.” IP ratings describe water protection under defined test conditions; they do not automatically mean unlimited bath use, high-pressure water exposure, or careless charging after cleaning.', 'Check the charging design closely. Magnetic charging contacts, sealed ports, and fully enclosed designs can reduce risk, but every product should still be dried completely before charging or storage. If a page does not explain whether the toy can be submerged, treat it as wipe-clean or splash-resistant only.'],
            'refs': ['iec','ipwiki','cpsc'],
            'faqs': [('What is the difference between waterproof and water-resistant adult toys?', 'Water-resistant toys are usually built for limited moisture such as splashes, wiping, or brief rinsing. Waterproof toys should tolerate stronger water exposure, but the safest choice is one that lists a clear IP rating and care instructions.'), ('Can I fully submerge a waterproof vibrator?', 'Only if the product instructions clearly allow submersion. A general waterproof label is not enough; check the IP rating, charging-port design, and drying instructions first.'), ('What does IPX7 mean for intimate wellness products?', 'IPX7 generally refers to temporary immersion under defined test conditions. It does not mean unlimited underwater use or ignoring the manufacturer’s care guide.'), ('Are rechargeable waterproof toys safe to rinse?', 'Many are safe to rinse when designed for it, but the charging area must be completely dry before charging. Follow the product instructions and avoid charging any device while damp.'), ('What is the safest cleaning routine?', 'Use the cleaning method recommended by the seller, rinse only when the toy is rated for it, dry fully, and store it away from lint, heat, and incompatible materials.')]
        }
    if cat == 'wearable':
        return {
            'quick_h2': 'Quick answer: fit, noise, controls, and privacy matter most',
            'lede': f'If you are considering {t.lower()}, the real decision is not just which feature sounds exciting. Fit, sound level, control style, app or remote privacy, cleaning, and storage all affect whether the product feels practical in real life.',
            'quick': 'Choose the simplest design that matches the actual use case. For wearable, remote, or app-connected products, prioritize clear dimensions, body-contact material, stable fit, easy controls, realistic noise expectations, and privacy-friendly setup.',
            'deep_h2': 'How to evaluate wearable and connected designs',
            'deep': ['Start with the real situation: private home use, partnered use, travel, shared housing, or discreet storage. A product that looks appealing in photos can still feel inconvenient if the controls are hard to reach, the app requires unnecessary permissions, or the charging routine is awkward.', 'For app-controlled or remote products, review whether the device can be used without oversharing personal data. Physical remotes may be simpler for privacy, while app features should be judged by permissions, pairing reliability, and whether the product still works if the app is not ideal.'],
            'refs': ['ftc','cpsc','nhs'],
            'faqs': [('Are wearable or remote adult toys beginner-friendly?', 'They can be beginner-friendly when the design is simple, the size is clearly explained, and the controls are easy to understand. Beginners should avoid vague product pages or app-only products with unclear privacy details.'), ('How quiet should a discreet toy be?', 'Noise varies by motor, material, shape, and intensity setting. If discretion matters, look for customer reviews, lower-intensity options, and realistic language rather than relying only on words like “silent.”'), ('Are app-controlled toys private?', 'Privacy depends on the app, permissions, account requirements, and connection method. Read the app details before buying and consider whether a physical remote gives enough control without extra data sharing.'), ('What material details should I check?', 'Look for clear body-contact material labels, care instructions, and compatibility notes for lubricant or cleaner. Avoid vague soft blends or pages that skip cleaning guidance.'), ('How should I store a connected toy?', 'Dry it fully, keep chargers or remotes together, and store the toy in a clean pouch or box away from lint, heat, and incompatible materials.')]
        }
    if cat == 'materials':
        return {
            'quick_h2': 'Quick answer: material transparency is the first safety filter',
            'lede': f'When reading about {t.lower()}, start with the material label rather than the marketing name. A useful product page should say what touches the body, how porous the surface is, which lubricant or cleaner is compatible, and how the item should be stored.',
            'quick': 'Prefer clearly named, non-porous materials when possible, such as body-safe silicone, ABS, glass, or stainless steel. Be cautious with vague soft blends, strong odors, sticky surfaces, or product pages that avoid cleaning and storage instructions.',
            'deep_h2': 'Material details that deserve a second look',
            'deep': ['Body-contact products need clear material information because cleaning, comfort, lubricant compatibility, and long-term storage all depend on the surface. “Soft,” “realistic,” or “premium feel” are not material names; look for precise labels and care guidance.', 'Porous materials can hold residue more easily than non-porous surfaces. If a product requires special cleaning, separate storage, or specific lubricant restrictions, the product page should say so plainly before checkout.'],
            'refs': ['fda','cpsc','nhs'],
            'faqs': [('What does body-safe material mean?', 'It should mean the seller clearly identifies the body-contact material and explains cleaning, lubricant compatibility, and storage. Treat vague claims as a reason to ask support before buying.'), ('Are non-porous materials easier to clean?', 'Generally yes. Non-porous surfaces such as silicone, glass, stainless steel, and ABS are usually easier to clean than porous soft blends, but you should still follow product-specific care instructions.'), ('Can I use silicone lubricant with silicone toys?', 'Many silicone toys are safest with water-based lubricant unless the seller confirms compatibility with silicone lubricant. When unsure, use water-based lubricant to reduce surface-damage risk.'), ('What material red flags should I avoid?', 'Avoid vague soft blends, strong odors, sticky surfaces, missing care instructions, or sellers that will not disclose material details.'), ('Are material guides medical advice?', 'No. They are shopping and care guidance. Stop using any product that causes pain or irritation and consult a qualified professional for health concerns.')]
        }
    if cat == 'lube':
        return {
            'quick_h2': 'Quick answer: match lubricant to material and use case',
            'lede': f'Choosing {t.lower()} is mainly about compatibility. The best option depends on the product material, condom use, skin sensitivity, cleanup routine, and whether the lubricant is intended for intimate use rather than massage or general body care.',
            'quick': 'Water-based lubricant is often the safest first comparison point because it is widely compatible with many toys and condoms. Silicone-based lubricant can last longer but may not suit some silicone toys. Oil-based products can damage latex condoms and are not interchangeable with intimate lubricant.',
            'deep_h2': 'How to compare lubricant labels without overthinking',
            'deep': ['Read the ingredient list, intended use, condom compatibility, and toy-material compatibility before buying. If a product page does not explain compatibility, choose a simpler water-based option or ask support.', 'Sensitive-skin shoppers should avoid unnecessary fragrance, warming additives, or unclear ingredient lists. Patch testing on external skin can be helpful, but any irritation means the product should be discontinued.'],
            'refs': ['cdc','nhs','pp'],
            'faqs': [('Is water-based lubricant the safest beginner choice?', 'It is often the easiest starting point because it works with many toys and many condoms. Still, read the label for intended use, ingredients, and compatibility.'), ('Can silicone lubricant damage silicone toys?', 'Some silicone lubricants may affect some silicone toy surfaces. Unless the seller confirms compatibility, use water-based lubricant with silicone toys.'), ('Is massage oil the same as lubricant?', 'No. Massage oil and intimate lubricant are not interchangeable. Oil-based products can damage latex condoms and may not be suitable for intimate use.'), ('What should sensitive-skin shoppers check?', 'Look for simple ingredient lists, avoid unnecessary fragrance or warming additives, and stop using any product that causes irritation.'), ('Do lubricants provide medical benefits?', 'No. They are comfort and compatibility products, not medical treatments. Consult a qualified professional for health concerns.')]
        }
    if cat == 'cleaning':
        return {
            'quick_h2': 'Quick answer: clean, dry, and store by material',
            'lede': f'Good care habits make {t.lower()} more practical. The main routine is simple: clean with a compatible method, rinse only when the product is rated for it, dry completely, and store it away from lint, heat, moisture, and incompatible surfaces.',
            'quick': 'Cleaning depends on material and electronics. Non-electronic glass or stainless steel may tolerate more thorough cleaning than rechargeable devices with seams or charging points. Always follow the product guide and dry fully before storage.',
            'deep_h2': 'A practical care routine for everyday shoppers',
            'deep': ['Separate cleaning from storage. A product can be clean but still not ready for storage if moisture remains around seams, texture, or charging contacts. Let items air-dry fully on a clean towel before putting them away.', 'Store different materials separately when possible. Clean pouches, breathable boxes, and keeping instructions or charging cables together reduce lint, residue transfer, and lost accessories.'],
            'refs': ['cpsc','nhs','fda'],
            'faqs': [('How should I clean an adult toy safely?', 'Follow the product instructions, use compatible mild soap or cleaner, rinse only when allowed, and dry fully before storage.'), ('Can I boil or disinfect every toy?', 'No. Electronics, porous materials, glued parts, or certain finishes can be damaged. Only use high-heat or stronger methods when the manufacturer clearly allows them.'), ('Why is drying important?', 'Moisture left around seams, texture, or charging contacts can create odor, residue, or damage risk. Full drying is part of safe storage.'), ('Should toys be stored separately?', 'Yes when possible. Separate pouches or clean boxes reduce lint, material transfer, and accidental contact with incompatible surfaces.'), ('What if a product causes irritation?', 'Stop using it and review the material, cleaner, and lubricant. For ongoing symptoms, consult a qualified professional.')]
        }
    if cat == 'privacy':
        return {
            'quick_h2': 'Quick answer: privacy is packaging, billing, tracking, and storage',
            'lede': f'For {t.lower()}, privacy is not one promise on a product page. It includes plain packaging, neutral billing, delivery timing, tracking access, return handling, support language, and how the item will be stored once it arrives.',
            'quick': 'Before checkout, confirm what appears on the package and payment statement, whether tracking is available, how returns are handled, and whether support can answer sensitive questions discreetly.',
            'deep_h2': 'Privacy checks before checkout',
            'deep': ['Look for specific privacy language instead of broad reassurance. “Discreet shipping” should explain the outer package, billing descriptor, tracking process, and whether the product name appears on labels or paperwork.', 'At home, plan storage before delivery. A clean pouch or lockable box, a place for chargers and instructions, and a delivery window that works for your household can prevent avoidable stress.'],
            'refs': ['ftc','tsa','cpsc'],
            'faqs': [('What does discreet shipping usually mean?', 'It usually means plain outer packaging and neutral billing, but each store should explain its exact policy. Read the shipping and privacy pages before checkout.'), ('Can adult wellness products be returned?', 'Return rules vary because intimate products may have hygiene restrictions. Check whether unopened items, defective products, or wrong deliveries are handled differently.'), ('How can I make delivery more private?', 'Use tracking, choose a delivery address you trust, review the billing descriptor, and contact support before checkout if privacy is essential.'), ('What should I know before traveling with adult products?', 'Check airline, TSA, and destination rules, keep items clean and powered off, and pack chargers separately when needed.'), ('Is online shopping privacy guaranteed?', 'No store can control every situation, but clear packaging, billing, tracking, and support policies reduce surprises.')]
        }
    if cat == 'fit':
        return {
            'quick_h2': 'Quick answer: fit, size, base design, and comfort come first',
            'lede': f'When comparing {t.lower()}, prioritize comfort and control over dramatic claims. Size, shape, base design, material, lubricant compatibility, cleaning, and the ability to stop immediately matter more than novelty.',
            'quick': 'Choose beginner-friendly sizing, clear dimensions, smooth non-porous materials when possible, compatible lubricant, and product designs that support safe handling and easy removal.',
            'deep_h2': 'Fit and comfort checks before buying',
            'deep': ['Read dimensions carefully and compare them to your comfort level, not to marketing photos. Beginners usually benefit from smaller, simpler designs and clear care instructions.', 'For any product intended for anal use, a flared base or retrieval-safe design is essential. Avoid improvising with products that are not designed for that purpose.'],
            'refs': ['nhs','pp','cpsc'],
            'faqs': [('What size is best for beginners?', 'A smaller, simpler product with clear dimensions and smooth material is usually easier to evaluate. Comfort and control matter more than size.'), ('Why does a flared base matter?', 'For products intended for anal use, a flared base or retrieval-safe design helps prevent the product from moving too far inward.'), ('What lubricant should I use?', 'Use a compatible lubricant listed by the seller. Water-based lubricant is often the simplest first option for many toys and condoms.'), ('How should I clean fit-focused products?', 'Follow the material-specific cleaning guide, rinse only when allowed, dry completely, and store separately.'), ('When should I stop using a product?', 'Stop immediately if there is pain, irritation, numbness, or pressure that does not feel comfortable. This guide is not medical advice.')]
        }
    if cat == 'lingerie':
        return {
            'quick_h2': 'Quick answer: fit, fabric, comfort, and care decide value',
            'lede': f'For {t.lower()}, the best choice is the one that feels comfortable, fits your body, and can be cared for without stress. Fabric, stretch, seams, sizing, wash instructions, and privacy during delivery all matter.',
            'quick': 'Check the size chart, fabric blend, stretch, closure style, wash instructions, and return rules before buying. Avoid relying only on model photos because fit can vary by body shape and garment construction.',
            'deep_h2': 'How to compare lingerie details like a careful shopper',
            'deep': ['Read fabric and stretch information before choosing a size. Lace, mesh, elastic, satin, and hardware can all feel different against skin, especially during longer wear.', 'Care instructions affect long-term value. Delicate fabrics usually last longer with gentle washing, air drying, and separate storage away from rough hardware or Velcro-like surfaces.'],
            'refs': ['ftc','cpsc','nhs'],
            'faqs': [('How do I choose lingerie size online?', 'Measure yourself, compare with the store’s size chart, and read whether the style has stretch, adjustable straps, or structured cups.'), ('What fabrics are most comfortable?', 'Comfort depends on skin sensitivity and fit. Soft mesh, stretch lace, satin, and cotton-lined areas can all work when seams and elastic do not dig in.'), ('How should delicate lingerie be washed?', 'Use gentle washing, cool water when recommended, and air drying. Follow the garment label and avoid heat that can damage elastic or lace.'), ('What if I am between sizes?', 'Check the stretch and closure style. For comfort-focused pieces, adjustable straps or flexible bands may be easier than rigid sizing.'), ('How do I keep lingerie purchases private?', 'Review packaging, billing, delivery tracking, and return policy before checkout.')]
        }
    # beginner/general
    return {
        'quick_h2': 'Quick answer: choose clarity, comfort, and privacy over hype',
        'lede': f'If you are reading about {t.lower()}, the safest buying path is calm and practical. Focus on clear product details, body-contact materials, size, cleaning, privacy, and support instead of exaggerated promises or pressure-based messaging.',
        'quick': 'A good first comparison starts with the actual use case, simple controls, transparent materials, realistic care instructions, private delivery, and a seller that answers sensitive questions clearly.',
        'deep_h2': 'How to make a confident beginner-friendly choice',
        'deep': ['Define the real situation before comparing products: solo use, partnered use, gift planning, travel, storage at home, or replacing something you already understand. That context makes features easier to judge.', 'Choose the product page that explains the basics plainly: material, size, power, cleaning, storage, shipping privacy, and return limits. Missing details are a reason to slow down or ask support.'],
        'refs': ['ftc','cpsc','nhs'],
        'faqs': [('What should beginners check first?', 'Start with size, material, controls, cleaning instructions, and privacy policies. Avoid products that rely on hype but skip practical details.'), ('How do I compare value without overbuying?', 'Choose the simplest product that fits the real use case. Extra modes, apps, or accessories are only valuable if you will actually use and maintain them.'), ('What privacy details matter before checkout?', 'Check plain packaging, neutral billing, tracking, return rules, and whether support can answer sensitive questions discreetly.'), ('Are adult wellness products medical treatments?', 'No. They are personal wellness products, not medical treatments. Do not rely on them for diagnosis, treatment, fertility, or therapeutic outcomes.'), ('When should I contact support?', 'Ask before checkout if material, dimensions, cleaning, shipping, or returns are unclear. A trustworthy seller should answer plainly.')]
    }

def refs_html(keys):
    links = ''.join(f'<li><a href="{url}" rel="nofollow noopener" target="_blank">{esc(label)}</a></li>' for k in keys for label,url in [REFS[k]])
    return f'<section class="content-card authority-card"><h2>Authority and safety references</h2><p>ShopLovaNest articles are buyer guides, not medical advice. For standards, consumer-safety context, and broader sexual-health education, these reliable sources can help readers verify the practical guidance above.</p><ul>{links}</ul></section>'

def quick_html(pack):
    return f'<section class="content-card quick-answer"><h2>{esc(pack["quick_h2"])}</h2><p>{esc(pack["quick"])}</p></section>'

def deep_html(pack):
    ps = ''.join(f'<p>{esc(p)}</p>' for p in pack['deep'])
    return f'<section class="content-card topic-depth"><h2>{esc(pack["deep_h2"])}</h2>{ps}</section>'

def red_flags_html(cat):
    base = ['The product page avoids material, dimensions, cleaning, or charging details.', 'The seller makes guaranteed medical, fertility, relationship, or therapeutic claims.', 'The page uses pressure-based language but does not explain returns, privacy, or support.', 'Care instructions are missing or conflict with the product’s water, material, or power design.']
    items = ''.join(f'<li>{esc(x)}</li>' for x in base)
    return f'<section class="content-card red-flags"><h2>Red flags to slow down before checkout</h2><ul>{items}</ul></section>'

def faq_html(pack):
    body = ''.join(f'<h3>{esc(q)}</h3><p>{esc(a)}</p>' for q,a in pack['faqs'])
    return f'<section class="content-card faq-card"><h2>FAQ</h2>{body}</section>'

def replace_section_by_h2(src: str, h2_text: str, replacement: str) -> str:
    # content-card section with matching h2 text
    pat = re.compile(r'<section class="content-card"[^>]*>\s*<h2>\s*' + re.escape(h2_text) + r'\s*</h2>.*?</section>', re.I|re.S)
    return pat.sub(replacement, src, count=1)

def enhance_file(p: Path):
    src = p.read_text(encoding='utf-8', errors='ignore')
    slug = p.parent.name
    title = title_from_html(src, slug)
    cat = category(slug, title)
    pack = topic_pack(cat, title)

    # Replace lede with natural topic-specific opening.
    src = re.sub(r'<div class="lede">.*?</div>', f'<div class="lede">{esc(pack["lede"])}</div>', src, count=1, flags=re.I|re.S)

    # Remove old enhancement blocks to make the script idempotent.
    src = re.sub(r'<section class="content-card (?:quick-answer|topic-depth|authority-card|red-flags|faq-card)".*?</section>', '', src, flags=re.I|re.S)

    # Replace generic FAQ entirely.
    src = re.sub(r'<section class="content-card">\s*<h2>FAQ</h2>.*?</section>', faq_html(pack), src, count=1, flags=re.I|re.S)

    # Make generic first section more specific.
    src = replace_section_by_h2(src, 'What this search really means', deep_html(pack))

    # Insert quick answer after lede if not present.
    src = re.sub(r'(<div class="lede">.*?</div>)', r'\1' + quick_html(pack), src, count=1, flags=re.I|re.S)

    # Insert red flags before privacy or shop-and-learn area.
    if 'red-flags' not in src:
        marker = re.search(r'<section class="content-card">\s*<h2>Privacy, delivery, and storage notes</h2>', src, re.I)
        if marker:
            src = src[:marker.start()] + red_flags_html(cat) + src[marker.start():]
        else:
            src = re.sub(r'(<section class="content-card">\s*<h2>Shop and learn next</h2>)', red_flags_html(cat) + r'\1', src, count=1, flags=re.I)

    # Insert references before FAQ.
    if 'authority-card' not in src:
        src = re.sub(r'(<section class="content-card faq-card">)', refs_html(pack['refs']) + r'\1', src, count=1, flags=re.I)

    # Improve generic headings while preserving structure.
    heading_map = {
        'Buying checklist before you compare prices': 'Buyer checklist before you compare products',
        'Common mistakes to avoid': 'Common mistakes that reduce comfort, privacy, or value',
        'Bottom line': 'Bottom line: choose the clearest and safest option',
    }
    for old, new in heading_map.items():
        src = src.replace(f'<h2>{old}</h2>', f'<h2>{new}</h2>')

    # Update dateModified in JSON-LD and visible modified date where applicable.
    src = re.sub(r'"dateModified"\s*:\s*"[^"]+"', f'"dateModified": "{TODAY}"', src)

    # Add FAQPage JSON-LD before </head> if absent.
    if 'FAQPage' not in src:
        faqs = pack['faqs']
        main = ',\n'.join('{"@type":"Question","name":"%s","acceptedAnswer":{"@type":"Answer","text":"%s"}}' % (esc(q), esc(a)) for q,a in faqs)
        faq_json = f'<script type="application/ld+json" data-shoplovanest-faq-seo="true">{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{main}]}}</script>\n'
        src = src.replace('</head>', faq_json + '</head>')

    p.write_text(src, encoding='utf-8')
    return slug, cat, title

def update_sitemap(slugs):
    if not SITEMAP.exists(): return
    src = SITEMAP.read_text(encoding='utf-8', errors='ignore')
    # Blog index changed because linked content quality changed.
    src = re.sub(r'(<loc>https://shoplovanest.com/blog/</loc><lastmod>)[^<]+', r'\g<1>'+TODAY, src)
    for slug in slugs:
        src = re.sub(r'(<loc>https://shoplovanest.com/blog/' + re.escape(slug) + r'/</loc><lastmod>)[^<]+', r'\g<1>'+TODAY, src)
    SITEMAP.write_text(src, encoding='utf-8')


def main():
    changed=[]
    for p in sorted(BLOG.glob('*/index.html')):
        if p.parent.name == 'assets':
            continue
        changed.append(enhance_file(p))
    update_sitemap([x[0] for x in changed])
    print(f'enhanced {len(changed)} articles')
    counts={}
    for _,cat,_ in changed: counts[cat]=counts.get(cat,0)+1
    print(counts)

if __name__ == '__main__':
    main()
