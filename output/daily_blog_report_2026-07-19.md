# Daily ShopLovaNest Blog Automation Report - 2026-07-19

Status: COMPLETE - generated, committed, pushed, deployed, live-verified, and success email accepted by msmtp.

Commit: `6718339b73`

Updated: 2026-07-19T08:40:33+08:00

## Articles
- **Adult Toy Cleaner vs Soap: What to Check**
  - URL: https://shoplovanest.com/blog/adult-toy-cleaner-vs-soap-guide/
  - Slug: `adult-toy-cleaner-vs-soap-guide`
  - Primary keywords: adult toy cleaner, sex toy cleaning spray, toy cleaner spray, toy-safe cleaning, adult toy care
  - Intent: Adult toy cleaner comparison intent — cleaner vs mild soap, sprays/wipes, material compatibility, electronics caution, label reading, storage, and checkout red flags
- **Mini Bullet Vibrator: Size & Noise Guide**
  - URL: https://shoplovanest.com/blog/mini-bullet-vibrator-size-noise-guide/
  - Slug: `mini-bullet-vibrator-size-noise-guide`
  - Primary keywords: mini bullet vibrator, small bullet vibrator, silver bullet vibrator, bullet vibrators, quiet vibrator
  - Intent: Mini bullet vibrator buyer intent — compact size tradeoffs, noise expectations, controls, charging/battery, material clarity, travel privacy, and checkout red flags

## Keyword source files read
- `output/merged_keyword_research_2026-06-25.csv`
- `output/keyword_to_url_mapping_2026-06-25.csv`

## Content quality and validation
- Local validation status: pass
- Minimum quality score: 100
- Blog index links: True
- Sitemap image metadata: True
### adult-toy-cleaner-vs-soap-guide
- Title length 40; meta length 118; one H1: True; word count 1159; quality score 100
- Authority references: https://www.fda.gov/cosmetics/cosmetics-labeling-regulations/cosmetics-labeling-guide, https://www.epa.gov/coronavirus/safe-and-effective-disinfectant-use, https://consumer.ftc.gov/articles/online-shopping, https://www.saferproducts.gov/
- All checks passed: True
### mini-bullet-vibrator-size-noise-guide
- Title length 44; meta length 121; one H1: True; word count 1160; quality score 100
- Authority references: https://www.iec.ch/ip-ratings, https://consumer.ftc.gov/articles/online-shopping, https://www.tsa.gov/travel/security-screening/whatcanibring/all, https://www.saferproducts.gov/
- All checks passed: True

## Images
- Generation status: pass
- Model: opus-image-1.5 via configured custom Sub2API Responses API /v1/responses with image_generation tool
- `upload/blog/assets/adult-toy-cleaner-vs-soap-guide-opus-cover.png`: pass; response `resp_0e631029a58966f4016a5c1b740200819bbc697f122c691ad8`
- `upload/blog/assets/mini-bullet-vibrator-size-noise-guide-opus-cover.png`: pass; response `resp_0ba823e199d717f5016a5c1ba1717c819a9a4441d967b5e768`

## Deployment and live verification
- Deploy status: pass
- Method: targeted rsync to root@153.75.235.56:/var/www/myopencart/upload
- Permissions: www-data:www-data; dirs 755; files 644
- Live verification: pass
- Verified URLs: https://shoplovanest.com/blog/adult-toy-cleaner-vs-soap-guide/, https://shoplovanest.com/blog/mini-bullet-vibrator-size-noise-guide/, https://shoplovanest.com/blog/, https://shoplovanest.com/sitemap.xml

## Email
- Recipient: yuanzhigang20@gmail.com
- Subject: ShopLovaNest Daily Blog Deployment Complete - 2026-07-19
- Message file: `output/daily_blog_2026-07-19_success.eml`
- Status: sent/accepted by msmtp exit 0
- Method: /opt/homebrew/bin/msmtp with temporary port 465 SMTPS config derived from /Users/grant/.msmtprc; passwordeval/keychain unchanged; msmtp exit 0

## Completion rule
{
  "exactly_2_new_articles": true,
  "blog_index_updated": true,
  "sitemap_updated": true,
  "content_quality_validation_passed": true,
  "git_commit_pushed": true,
  "production_deployed": true,
  "live_verification_passed": true,
  "success_email_sent_accepted": true
}
