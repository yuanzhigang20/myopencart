# ShopLovaNest Daily Blog Automation Report - 2026-07-09

- Status: complete
- Timezone: Asia/Shanghai
- Article quota: 2
- Commit: aecb16b0f2d41b9e618a99bb32f75c1807413652
- Email: sent_accepted to yuanzhigang20@gmail.com via /opt/homebrew/bin/msmtp

## Articles

### Best Bullet Vibrator: Small Buyer Checklist
- Slug: `best-bullet-vibrator-guide`
- URL: https://shoplovanest.com/blog/best-bullet-vibrator-guide/
- Primary keywords: best bullet vibrator, best bullet vibrators, bullet vibrator, bullet vibrators, small bullet vibrator
- Intent cluster: Best bullet vibrator comparison intent — small form factor, simple controls, motor strength versus comfort, water-resistance/charging claims, cleaning, travel privacy, and ecommerce red flags
- Keyword source: output/merged_keyword_research_2026-06-25.csv rows: bullet vibrator (Volume 14800), bullet vibrators (1900), best bullet vibrator (1600), best bullet vibrators (480), small bullet vibrator (390), mini bullet vibrator (590); output/keyword_to_url_mapping_2026-06-25.csv maps broad bullet-vibrator intent to existing education, but did not include a dedicated best-bullet comparison page. Created as a compact-motor buyer-safety checklist, distinct from the existing bullet vibrator guide and how-to-use article.

### Adult Toy Advent Calendar: Consent-First Guide
- Slug: `adult-toy-advent-calendar-guide`
- URL: https://shoplovanest.com/blog/adult-toy-advent-calendar-guide/
- Primary keywords: adult toy advent calendar, adult toy advent calendars, adult toys advent calendar, adult toy gift calendar, adult wellness gift set
- Intent cluster: Adult toy advent calendar / multi-item gift-set intent — consent-first gifting, item transparency, body-contact materials, sizing variability, hygiene seals, returns, shipping privacy, and value red flags
- Keyword source: output/merged_keyword_research_2026-06-25.csv rows: adult toy advent calendar (Volume 480) and related gift/seasonal adult-toy queries; output/keyword_to_url_mapping_2026-06-25.csv maps gift intent to consent/privacy education. Created as a distinct seasonal multi-item gift-set buyer-safety checklist, not a duplicate of the adult toy gift guide or date-night gift page.

## Content Quality Validation
- Status: pass
- Minimum quality score: 100

### `best-bullet-vibrator-guide`
- Title length: 43 (<60)
- Meta length: 136 (<155)
- H1 count: 1
- Word count: 2119
- Quality score: 100
- Required checks: title_under_60, meta_under_155, one_h1, gtag_script_and_config_once, gtag_immediately_after_head, word_count_1000_plus, quick_answer, red_flags, faqpage_jsonld, authority_refs, related_blog_links_2_4, product_support_links_1_3, image_seo_metadata, natural_readability_markers, topic_specific_depth, banned_terms_absent

### `adult-toy-advent-calendar-guide`
- Title length: 46 (<60)
- Meta length: 133 (<155)
- H1 count: 1
- Word count: 2086
- Quality score: 100
- Required checks: title_under_60, meta_under_155, one_h1, gtag_script_and_config_once, gtag_immediately_after_head, word_count_1000_plus, quick_answer, red_flags, faqpage_jsonld, authority_refs, related_blog_links_2_4, product_support_links_1_3, image_seo_metadata, natural_readability_markers, topic_specific_depth, banned_terms_absent

## Image and Sitemap Checks
- Image generation: pass using opus-image-1.5 via configured custom endpoint
- Image files:
  - `upload/blog/assets/best-bullet-vibrator-guide-opus-cover.png`
  - `upload/blog/assets/adult-toy-advent-calendar-guide-opus-cover.png`
- Sitemap updated: True
- Sitemap live check: HTTP 200, includes new URLs, 2026-07-09 lastmod, image metadata

## Deployment and Live Verification
- Deploy status: pass
- Deploy method: targeted rsync to root@153.75.235.56:/var/www/myopencart/upload
- Permissions: www-data:www-data, dirs 755, files 644
- Live verification status: pass
- Article live checks: HTTP 200, title/meta present, one H1, gtag script and config exactly once, Quick Answer, Red Flags, FAQPage schema, authority references, image SEO metadata
- Blog index: HTTP 200 and links both new articles

## Email
- Status: sent_accepted
- Subject: ShopLovaNest Daily Blog Deployment Complete - 2026-07-09
- Sent at: 2026-07-09T08:41:28.662375+08:00
