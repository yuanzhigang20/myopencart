# ShopLovaNest Daily Blog Report - 2026-07-24

Status: generated and locally validated; deployment/email pending.
Timezone: Asia/Shanghai

## Keyword source files read
- `output/merged_keyword_research_2026-06-25.csv`
- `output/keyword_to_url_mapping_2026-06-25.csv`

## Selected articles

1. **Insertable Egg Toys: Safer Buyer Guide**
   - Slug: `insertable-egg-toy-buyer-guide`
   - URL: https://shoplovanest.com/blog/insertable-egg-toy-buyer-guide/
   - Primary keyword: `adult toy eggs insertable`
   - Intent: insertable egg buyer-safety checks: retrieval design, size, materials, remote controls, cleaning, privacy, and checkout red flags.
   - Keyword file evidence: merged keyword volume 1300; mapping Priority P1 under gift/couples decisions.

2. **Bullet Vibrator Charger Guide**
   - Slug: `bullet-vibrator-charger-guide`
   - URL: https://shoplovanest.com/blog/bullet-vibrator-charger-guide/
   - Primary keywords: `bullet vibrator charger`, `bullet vibrator chargjng time`, `rechargeable bullet vibrator`
   - Intent: charger and battery-care checks: cable matching, charging time, USB power, magnetic pins, dry contacts, replacement safety, and red flags.
   - Keyword file evidence: merged keyword volumes 320, 260, 210; mapping Priority P2/P1 under compact/rechargeable vibrator clusters.

## Local quality validation
- SEO titles under 60 chars: pass
- Meta descriptions under 155 chars: pass
- Exactly one H1 per article: pass
- Google tag `G-P2LJRXN3D1` config exactly once and immediately after `<head>`: pass
- Word count 1000+: pass
  - insertable egg guide: 1051 words
  - charger guide: 1054 words
- Quick Answer near top: pass
- Red Flags section: pass
- 5 FAQs and FAQPage JSON-LD per article: pass
- 4 related blog links and product/support links: pass
- Authority references: pass
- Image SEO metadata and JSON-LD ImageObject: pass
- Banned/unsafe scan: pass
- Quality score: 100/100 each

## Images
Generated with required custom model `opus-image-1.5` via configured Responses API image generation tool.
- `upload/blog/assets/insertable-egg-toy-buyer-guide-opus-cover.png`
- `upload/blog/assets/bullet-vibrator-charger-guide-opus-cover.png`

## Sitemap and index
- `upload/blog/index.html` updated with both article cards and count 138.
- `upload/sitemap.xml` updated with both new article URLs, `lastmod=2026-07-24`, and image metadata.

## Pending
- Git commit/push
- Production rsync deployment
- Live verification
- Success email via `/opt/homebrew/bin/msmtp`

## Blocker update - 08:44 CST
- Local commit created: `053081ad4a` (`Add ShopLovaNest daily blogs for 2026-07-24`).
- Git push blocked: SSH to GitHub failed twice with connection closed / banner exchange timeout; remote repository could not be read.
- Production deploy blocked: targeted rsync/SSH to `root@153.75.235.56` failed with connection closed during rsync, then repeated SSH banner exchange timeouts.
- Live verification and success email were not completed because deployment is blocked. Per rule, email was not sent and state remains incomplete for retry.

## Retry update - 2026-07-24T10:38:07+08:00
- Git push recovered: pushed `master` to GitHub using SSH over port 443 (`ssh.github.com`). Current commit: `2dd0d86412`.
- Production deploy still blocked: SSH to `153.75.235.56:22` accepts TCP but returns no SSH banner and times out during banner exchange; targeted rsync cannot start.
- Live verification remains incomplete: `insertable-egg-toy-buyer-guide` is not serving the generated static article content and sitemap does not include the new URL; `bullet-vibrator-charger-guide` returns an article page but the day's two-article deployment is not complete.
- Success email was not sent because deployment/live verification did not pass.

## Completion update - 12:35 CST
- Production SSH recovered.
- Targeted rsync deployment completed for:
  - `upload/blog/insertable-egg-toy-buyer-guide/`
  - `upload/blog/bullet-vibrator-charger-guide/`
  - both topic-specific `opus-image-1.5` cover images
  - `upload/blog/index.html`
  - `upload/sitemap.xml`
- Production ownership/perms fixed: `www-data:www-data`, directories `755`, files `644`.
- Live verification passed:
  - both article URLs return HTTP 200
  - title/meta present
  - exactly one H1
  - Google tag config exactly once
  - Quick Answer and Red Flags present
  - FAQPage JSON-LD present
  - authority references present
  - image SEO metadata present
  - blog index HTTP 200 and links both new articles
  - sitemap HTTP 200 and includes both URLs, `lastmod=2026-07-24`, and image metadata
- Success email accepted by `/opt/homebrew/bin/msmtp` using `/Users/grant/.msmtprc`.
- Final status: complete.
- Final completion-state commit: `988e52c1c9` (email body listed deployed/content commit `4087e03aef`).
