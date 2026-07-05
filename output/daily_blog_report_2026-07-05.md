# ShopLovaNest Daily Blog Deployment Report — 2026-07-05

## Status
Complete: generated exactly 2 new English SEO blog articles from the mandatory keyword files, created topic-specific opus-image-1.5 images, updated blog index and sitemap, passed local validation, committed/pushed, deployed to production, verified live, and sent the success email accepted by msmtp.

## Keyword sources inspected
- `output/merged_keyword_research_2026-06-25.csv`
- `output/keyword_to_url_mapping_2026-06-25.csv`

## Articles

### 1. Remote Control Cock Ring: Buying Checklist
- Slug: `remote-control-cock-ring-guide`
- URL: https://shoplovanest.com/blog/remote-control-cock-ring-guide/
- Primary keywords: remote control cock ring; cock ring with vibrator; vibrating cock rings; adjustable cock ring
- Intent cluster: remote-control cock ring shopping intent — fit, release design, range limits, battery style, partner consent, cleaning, and privacy checks
- Image: `/blog/assets/remote-control-cock-ring-guide-opus-cover.png`
- Authority references: FDA, CPSC, FTC, TSA
- Local validation: pass; quality score 100; 1963 words; one H1; title 42 chars; meta 134 chars; Quick Answer; Red Flags; FAQPage JSON-LD; image SEO metadata; internal/product/support links.

### 2. Silicone Lube Spray: Label and Compatibility Guide
- Slug: `silicone-lube-spray-guide`
- URL: https://shoplovanest.com/blog/silicone-lube-spray-guide/
- Primary keywords: silicone lube spray; silicone lube; best silicone lube; silicone vs water based lube
- Intent cluster: silicone-lube spray shopping intent — spray format, ingredient label, toy compatibility, condom notes, cleanup, privacy, and checkout red flags
- Image: `/blog/assets/silicone-lube-spray-guide-opus-cover.png`
- Authority references: FDA, CDC, FTC, Planned Parenthood
- Local validation: pass; quality score 100; 1947 words; one H1; title 50 chars; meta 131 chars; Quick Answer; Red Flags; FAQPage JSON-LD; image SEO metadata; internal/product/support links.

## Index and sitemap
- `upload/blog/index.html` updated to 102 guides and includes both new article cards.
- `upload/sitemap.xml` includes both new article URLs with `lastmod` 2026-07-05 and image sitemap metadata.

## Validation summary
- Validator: `output/validate_daily_blog_2026_07_05.py`
- Result: pass
- Required custom images: present as topic-specific `opus-image-1.5` generated PNG files.

## Deployment / verification / email
- Commit: `26dc13e709` — Add daily ShopLovaNest blogs for 2026-07-05.
- Git push: pass; `origin/master` already contains commit `26dc13e709`.
- Production deploy: pass; targeted rsync deployed both article folders, both opus images, blog index, and sitemap to `root@153.75.235.56:/var/www/myopencart/upload`; ownership/perms fixed to `www-data:www-data`, dirs 755, files 644.
- Live verification: pass at 2026-07-05T08:47:26.924249+08:00; both article URLs returned HTTP 200 with title/meta, one H1, Google tag configured once, Quick Answer, Red Flags, FAQPage schema, authority references, image SEO metadata; blog index HTTP 200 links both articles; sitemap HTTP 200 includes both URLs, `2026-07-05` lastmod, and image metadata.
- Email: sent/accepted via `/opt/homebrew/bin/msmtp --file=/Users/grant/.msmtprc yuanzhigang20@gmail.com`, exit code 0. Subject: `ShopLovaNest Daily Blog Deployment Complete - 2026-07-05`.

## Final status
Complete: exactly 2 new articles generated from keyword files, validated, committed/pushed, deployed live, verified, and success email accepted by msmtp.
