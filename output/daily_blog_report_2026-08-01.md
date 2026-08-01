# ShopLovaNest Daily Blog Automation Report - 2026-08-01

Status: email blocked after live verification.
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
- Send success email via /opt/homebrew/bin/msmtp: failed (exit 75)
- Update this report and state file with final email status: pass


## Commit / Deploy / Verification

- Commit: 62ecf7bc44df8a2fa61d10dfb13ec617b4ac177a (pushed to origin/master)
- Deployment: targeted rsync to root@153.75.235.56:/var/www/myopencart/upload; ownership and permissions fixed.
- Live verification: pass for both article URLs, blog index, and sitemap including image metadata.
- Email: failed via /opt/homebrew/bin/msmtp (exit 75): smtp.gmail.com:587 timed out; direct checks to ports 587 and 465 also timed out. State remains incomplete for next scheduled retry.


## Email Attempt / Blocker

- Attempted: 2026-08-01 08:50 Asia/Shanghai
- Tool: /opt/homebrew/bin/msmtp with /Users/grant/.msmtprc
- Recipient: yuanzhigang20@gmail.com
- Result: failed, exit code 75
- Error: `msmtp: cannot connect to smtp.gmail.com, port 587: Operation timed out`
- Additional connectivity check: `smtp.gmail.com:587` and `smtp.gmail.com:465` both timed out from this Mac.
- Completion status: incomplete only because email was not accepted. Articles, commit, deployment, live verification, blog index, and sitemap are already complete; next scheduled retry should resume at the email step and avoid creating extra articles.
