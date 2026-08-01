# ShopLovaNest Daily Blog Automation Report - 2026-08-01

Status: complete.
Timezone: Asia/Shanghai

## Articles Generated

1. https://shoplovanest.com/blog/what-do-cock-rings-do-safety-guide/
   - Title: What Do Cock Rings Do? Safety Guide
   - Primary keywords: what do cock rings do; what is a cock ring for; cock ring benefits
   - Source: output/merged_keyword_research_2026-06-25.csv and output/keyword_to_url_mapping_2026-06-25.csv
   - Intent: plain-English cock ring function, fit, materials, time limits, and checkout red flags.

2. https://shoplovanest.com/blog/electric-male-masturbator-buying-checklist/
   - Title: Electric Male Masturbator Buying Checklist
   - Primary keywords: electric male masturbator; male masturbator machine; top rated male masturbators
   - Source: output/merged_keyword_research_2026-06-25.csv and output/keyword_to_url_mapping_2026-06-25.csv
   - Intent: powered male wellness device buying checklist covering motor style, sleeve care, drying, charging, noise, privacy, and support.

## Local Quality Validation

Validation file: output/daily_blog_validation_2026-08-01.json

- SEO title length: pass
- Meta description length: pass
- Exactly one H1: pass
- Google tag block immediately after `<head>` with one script and one config: pass
- Word count: pass (1243 and 1158 useful words)
- Quick Answer: pass
- Red Flags section: pass
- FAQPage JSON-LD: pass
- Authority references: pass (4 per article)
- Related blog links: pass
- Product/support links: pass
- Topic-specific generated images using opus-image-1.5: pass
- og/twitter image metadata and JSON-LD ImageObject: pass
- Sitemap lastmod and image metadata: pass
- Quality scores: 92 and 93

## Pending Steps

- Commit and push: pass (62ecf7bc44df8a2fa61d10dfb13ec617b4ac177a)
- Deploy changed files to production: pass (targeted rsync)
- Verify live article pages, blog index, and sitemap: pass (output/live_verification_2026-08-01.json)
- Send success email via /opt/homebrew/bin/msmtp: pass (exit 0, accepted by msmtp)
- Update this report and state file with final email status: pass


## Commit / Deploy / Verification

- Commit: 62ecf7bc44df8a2fa61d10dfb13ec617b4ac177a (pushed to origin/master)
- Deployment: targeted rsync to root@153.75.235.56:/var/www/myopencart/upload; ownership and permissions fixed.
- Live verification: pass for both article URLs, blog index, and sitemap including image metadata.
- Email: sent via /opt/homebrew/bin/msmtp at 2026-08-01 10:30 Asia/Shanghai (exit 0, accepted by msmtp).


## Email Attempt / Completion

- Initial attempt: 2026-08-01 08:50 Asia/Shanghai failed because `smtp.gmail.com:587` timed out; direct checks to ports 587 and 465 also timed out.
- Retry: 2026-08-01 10:30 Asia/Shanghai after SMTP connectivity recovered.
- Tool: /opt/homebrew/bin/msmtp with /Users/grant/.msmtprc
- Recipient: yuanzhigang20@gmail.com
- Subject: ShopLovaNest Daily Blog Deployment Complete - 2026-08-01
- Result: sent/accepted by msmtp, exit code 0.
- Completion status: complete. Articles, commit, deployment, live verification, blog index, sitemap, and success email are complete.
