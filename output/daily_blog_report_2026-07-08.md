# ShopLovaNest Daily Blog Report - 2026-07-08

## Status
Blocked at email notification after successful generation, validation, commit/push, deployment, and live verification.

**Blocker:** `/opt/homebrew/bin/msmtp` cannot connect to `smtp.gmail.com:587`; both `nc -vz -w 20 smtp.gmail.com 587` and msmtp timed out. msmtp exited `75`. Gmail app password was not printed or stored; debug output masked it.

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

Not complete. Success email was prepared but not accepted by msmtp because SMTP connectivity timed out:

```text
msmtp: cannot connect to smtp.gmail.com, port 587: Operation timed out
msmtp: could not send mail (account default from /Users/grant/.msmtprc)
```

The next scheduled retry should not create extra articles. It should retry the existing prepared email after checking SMTP connectivity, then mark the day complete only if msmtp accepts the message.
