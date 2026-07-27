# ShopLovaNest Daily Blog Report - 2026-07-27

Status: COMPLETE  
Timezone: Asia/Shanghai  
Completed at: 2026-07-27T14:38:57+08:00

## Articles Deployed

1. [Bullet Vibrator Charger Guide](https://shoplovanest.com/blog/bullet-vibrator-charger-guide/)
   - Slug: `bullet-vibrator-charger-guide`
   - Primary keywords: bullet vibrator charger, bullet vibrator charging time, rechargeable bullet vibrator
   - Intent cluster: Bullet vibrator charger intent — shoppers want to replace, compare, or troubleshoot charging cables and understand charging time without unsafe electrical assumptions.

2. [Adult Toy Advent Calendar Guide](https://shoplovanest.com/blog/adult-toy-advent-calendar-guide/)
   - Slug: `adult-toy-advent-calendar-guide`
   - Primary keywords: adult toy advent calendar, adult toy subscription box, adult toy box subscription
   - Intent cluster: Adult toy advent calendar and subscription box intent — shoppers compare surprise boxes, privacy, value, consent, returns, materials, and red flags before gifting or buying.

## Keyword Source Compliance

Read required keyword files before topic selection:
- `output/merged_keyword_research_2026-06-25.csv`
- `output/keyword_to_url_mapping_2026-06-25.csv`

Selected two compliant, distinct-intent clusters and avoided skipped/irrelevant groups.

## Content Quality Validation

Local validation passed for both articles:
- SEO title under 60 characters.
- Meta description under 155 characters.
- Exactly one H1.
- Google tag `G-P2LJRXN3D1` exactly once immediately after `<head>`.
- 1000+ words.
- Quick Answer section present.
- Red Flags section present.
- FAQPage JSON-LD present with 5 FAQs per article.
- Related blog links and product/support links present.
- Authority references present.
- Topic-specific generated images from `opus-image-1.5` included with alt/title/caption, OG/Twitter image metadata, and JSON-LD image metadata.
- Sitemap image metadata present.
- Quality score: 100 for both articles.

## Authority References

- Bullet vibrator charger guide: consumer.ftc.gov, ftc.gov, cpsc.gov, tsa.gov, ul.com.
- Adult toy advent calendar guide: consumer.ftc.gov, ftc.gov, saferproducts.gov, plannedparenthood.org.

## Git

- Article commit: `2efb813ed334ab0fc50a36c1bd62d50622f0bfe9`
- Deployment verification commit: `c698e9f492`
- Final report/state commit: pending at report write time.
- Push status: successful to `origin/master`.

## Deployment

Targeted rsync completed to:
- `root@153.75.235.56:/var/www/myopencart/upload/blog/bullet-vibrator-charger-guide/`
- `root@153.75.235.56:/var/www/myopencart/upload/blog/adult-toy-advent-calendar-guide/`
- `root@153.75.235.56:/var/www/myopencart/upload/blog/assets/`
- `root@153.75.235.56:/var/www/myopencart/upload/blog/index.html`
- `root@153.75.235.56:/var/www/myopencart/upload/sitemap.xml`

Permissions fixed: `www-data:www-data`, directories `755`, files `644`.

## Live Verification

Passed:
- Both article URLs returned HTTP 200.
- Title/meta present.
- Exactly one H1.
- Google tag script/config exactly one.
- Quick Answer, Red Flags, FAQPage schema present.
- Authority references present.
- OG/Twitter/JSON-LD image SEO metadata present.
- Blog index returned HTTP 200 and links both articles.
- Sitemap returned HTTP 200 and includes both article URLs, `2026-07-27` lastmod, and image metadata.

## Email

- Recipient: `yuanzhigang20@gmail.com`
- Subject: `ShopLovaNest Daily Blog Deployment Complete - 2026-07-27`
- Status: sent/accepted by `/opt/homebrew/bin/msmtp`.
- Note: first attempt using `/Users/grant/.msmtprc` port 587 timed out. Retry used a temporary msmtp config derived from `/Users/grant/.msmtprc` with Gmail port 465 and `tls_starttls off`; password remained in macOS Keychain via passwordeval and was not printed or stored.

## Completion Rule

Complete: exactly 2 new articles generated from keyword files, index/sitemap updated, validation passed, git pushed, production deployed, live verified, and email accepted by msmtp.
