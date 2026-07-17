# Daily Blog Automation Report - 2026-07-17

Status: deployed and live verified; blocked only on msmtp email acceptance.
Timezone: Asia/Shanghai
Quota: exactly 2 new articles

## Keyword source inspection

Read before topic selection:
- `output/merged_keyword_research_2026-06-25.csv`
- `output/keyword_to_url_mapping_2026-06-25.csv`

Skipped irrelevant/misleading groups per standing rules: fidget toys, Toy Story/Disney/media, dogs/pets, location-only store queries, competitor/navigation ambiguity, and non-adult-wellness meanings.

## Selected articles

1. Pink Sleeve Masturbator: Material Guide
- Slug: `male-masturbator-pink-sleeve-material-guide`
- URL: https://shoplovanest.com/blog/male-masturbator-pink-sleeve-material-guide/
- Primary keywords: male masturbator pink sleeve; male masturbator; realistic male masturbator; male masturbator materials; male masturbator cleaning
- Source rationale: selected `male masturbator pink sleeve` (Volume 590) from merged keyword research and clustered with mapped male masturbator/material/cleaning intents. Existing pages cover broad product type and care; this article targets the distinct color/realistic sleeve material-safety intent.
- Authority references: FDA cosmetics labeling, CPSC saferproducts.gov, FTC online shopping, CDC handwashing.
- Image: `upload/blog/assets/male-masturbator-pink-sleeve-material-guide-opus-cover.png`, generated with `opus-image-1.5` via configured custom Responses API endpoint.

2. Cock Ring With Plug: Fit Safety Guide
- Slug: `cock-ring-with-plug-combo-safety-guide`
- URL: https://shoplovanest.com/blog/cock-ring-with-plug-combo-safety-guide/
- Primary keywords: cock ring butt plug; cock ring dildo; cock and ball ring; cock ring metal; adjustable cock ring
- Source rationale: selected `cock ring butt plug` (Volume 260), `cock ring dildo` (Volume 260), `cock and ball ring` (Volume 1300), `cock ring metal` (Volume 260), and `adjustable cock ring` (Volume 1000) from the mapped couples accessories cluster. Existing cock ring pages cover general sizing; this clusters combination-accessory fit/base safety intent.
- Authority references: Cleveland Clinic sexual health/pain signals, NHS safer sex, CDC condoms, FTC online shopping.
- Image: `upload/blog/assets/cock-ring-with-plug-combo-safety-guide-opus-cover.png`, generated with `opus-image-1.5` via configured custom Responses API endpoint.

## Local validation summary

All checks passed with quality score 100 for both articles:
- SEO title under 60 characters
- Meta description under 155 characters
- Exactly one H1
- Google tag `G-P2LJRXN3D1` script/config exactly once and immediately after `<head>`
- 1000+ useful words
- Quick Answer section present
- Red Flags / slow down before checkout section present
- FAQ section and FAQPage JSON-LD present
- 4 authority references per article
- 4 related blog links per article
- 3 relevant product/support links per article
- Topic-specific image metadata: alt/title, figcaption, og:image, og:image:alt, twitter:image, twitter:image:alt, JSON-LD ImageObject
- Banned/unsafe term scan passed
- Blog index updated with new article cards
- Sitemap updated with lastmod 2026-07-17 and image metadata for both new article URLs

## Deployment and verification

Commit: 25e148679451
Push: pass to origin/master
Deploy: pass via targeted rsync to production; permissions fixed to www-data:www-data, dirs 755, files 644.
Live verification: pass at 2026-07-17T08:41:09.482402+08:00
- Article URLs HTTP 200: true
- Blog index HTTP 200 and links both new articles: true
- Sitemap HTTP 200 with both URLs, 2026-07-17 lastmod, and image metadata: true
- Article title/meta/H1/gtag, Quick Answer, Red Flags, FAQ schema, authority references, and image metadata: true

## Email status

Blocked: `/opt/homebrew/bin/msmtp -C /Users/grant/.msmtprc -t < output/daily_blog_2026-07-17_success.eml` exited 76 twice with:

```text
msmtp: the server sent an empty reply
msmtp: could not send mail (account default from /Users/grant/.msmtprc)
```

Completion remains incomplete until msmtp exits 0 and the success email is accepted.
