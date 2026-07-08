# ShopLovaNest Daily Blog Report - 2026-07-08

## Status
Complete — generated exactly 2 new English SEO blog articles from the mandatory keyword files, created topic-specific opus-image-1.5 images, updated blog index and sitemap, passed local validation, committed/pushed, deployed to production, verified live, and sent the success email accepted by msmtp.

Completion time: 2026-07-08T12:32:32.346793+08:00

## Articles generated from keyword files

1. **Best Rabbit Vibrator: Buyer Safety Checklist**
   - URL: https://shoplovanest.com/blog/best-rabbit-vibrator-buyer-guide/
   - Primary keywords: best rabbit vibrator, best rabbit vibrators, rabbit vibrator, the rabbit vibrator, rabbit vibrater
   - Source: `output/merged_keyword_research_2026-06-25.csv` rabbit-vibrator rows and `output/keyword_to_url_mapping_2026-06-25.csv` rabbit-vibrator mappings.
   - Intent: rabbit vibrator comparison/buyer-safety checklist.

2. **Weighted Kegel Balls: Safe Buyer Checklist**
   - URL: https://shoplovanest.com/blog/weighted-kegel-balls-guide/
   - Primary keywords: weighted kegel balls, kegel balls, kegel ball, silicone kegel balls, what are kegel balls
   - Source: `output/merged_keyword_research_2026-06-25.csv` kegel-ball rows and `output/keyword_to_url_mapping_2026-06-25.csv` pelvic wellness accessory mappings.
   - Intent: weighted kegel balls material/size/retrieval/cautious-use buyer checklist.

## Content quality checks

Validation passed locally with quality score 100 for both articles:
- SEO title <60 chars and meta description <155 chars.
- Exactly one H1.
- Google tag `G-P2LJRXN3D1` script and config exactly once, immediately after `<head>`.
- 1000+ useful words.
- Quick Answer section near top.
- Red Flags / when to slow down before checkout section.
- 4-5 practical FAQs with FAQPage JSON-LD.
- Authority references included.
- Related blog links and product/support links included.
- Topic-specific depth, natural American English, and cautious no-medical-claims wording.
- Image SEO metadata present.

## Authority references

Rabbit vibrator guide includes IEC IP ratings, Planned Parenthood lubricant overview, CPSC battery safety, and FTC online shopping guidance.

Weighted kegel balls guide includes Cleveland Clinic Kegel exercise overview, NHS pelvic floor exercise guidance, FDA medical-device consumer basics, and FTC online shopping guidance.

## Image and sitemap checks

- Generated topic-relevant cover images with `opus-image-1.5` via the configured custom endpoint:
  - `upload/blog/assets/best-rabbit-vibrator-buyer-guide-opus-cover.png`
  - `upload/blog/assets/weighted-kegel-balls-guide-opus-cover.png`
- Article pages include image alt/title, figcaption, og:image/og:image:alt, twitter:image/twitter:image:alt, and JSON-LD ImageObject metadata.
- `upload/sitemap.xml` updated with both article URLs, `2026-07-08` lastmod, and image metadata.
- `upload/blog/index.html` updated and live index links both new articles.

## Git/deploy/live verification

- Commit: `73bf204f8b`
- Push: passed to `origin/master`.
- Deployment: targeted rsync to `root@153.75.235.56:/var/www/myopencart/upload`; ownership/perms fixed to `www-data:www-data`, directories 755, files 644.
- Live verification passed:
  - Both articles HTTP 200.
  - Blog index HTTP 200 and links both new articles.
  - Sitemap HTTP 200 and includes both new URLs, lastmod, and image metadata.

## Email status

Complete. Initial email attempt at 10:42 was blocked by a temporary timeout to `smtp.gmail.com:587`; retry at 2026-07-08T12:32:32.346793+08:00 succeeded after SMTP connectivity recovered.

- Recipient: yuanzhigang20@gmail.com
- Tool: `/opt/homebrew/bin/msmtp -C /Users/grant/.msmtprc`
- Subject: `ShopLovaNest Daily Blog Deployment Complete - 2026-07-08`
- Status: SENT/ACCEPTED by msmtp, exit code 0
- Credential handling: Gmail app password was not printed or stored.
