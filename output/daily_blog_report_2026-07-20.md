# Daily ShopLovaNest Blog Automation Report - 2026-07-20

Status: COMPLETE - generated, committed, pushed, deployed, live-verified, and success email accepted by msmtp.

Commit: `516e52de0b`

Updated: 2026-07-20T08:43:01+08:00

## Articles
- **Male Masturbator Devices: Type Guide**
  - URL: https://shoplovanest.com/blog/male-masturbator-device-types-guide/
  - Slug: `male-masturbator-device-types-guide`
  - Primary keywords: male masturbation device, male masturbation devices, automatic male masturbators, electric male masturbator, best male masturbator toy
  - Intent: Male masturbator device type comparison intent — manual sleeve vs automatic/electric vs hands-free, cleaning access, motors, noise, controls, charging, material clarity, privacy, and checkout red flags
- **Rabbit Vibrator Ears: Fit & Control Guide**
  - URL: https://shoplovanest.com/blog/rabbit-vibrator-ears-fit-guide/
  - Slug: `rabbit-vibrator-ears-fit-guide`
  - Primary keywords: rabbit vibrating ears, dual rabbit vibrator, small rabbit vibrator, what is a rabbit vibrator, how to use a rabbit vibrator
  - Intent: Rabbit vibrator ear and fit intent — external ear shape, internal shaft size, dual alignment variability, small vs full-size tradeoffs, controls, charging, cleaning, and checkout red flags

## Keyword source files read
- `output/merged_keyword_research_2026-06-25.csv`
- `output/keyword_to_url_mapping_2026-06-25.csv`

## Content quality and validation
- Local validation status: pass
- Minimum quality score: 100
- Blog index links: True
- Sitemap image metadata: True
### male-masturbator-device-types-guide
- Title length 36; meta length 132; one H1: True; word count 1047; quality score 100
- Authority references: https://consumer.ftc.gov/articles/online-shopping, https://www.saferproducts.gov/, https://www.fda.gov/cosmetics/cosmetics-labeling-regulations/cosmetics-labeling-guide, https://www.iec.ch/ip-ratings
- All checks passed: True
### rabbit-vibrator-ears-fit-guide
- Title length 45; meta length 136; one H1: True; word count 1128; quality score 100
- Authority references: https://www.iec.ch/ip-ratings, https://consumer.ftc.gov/articles/online-shopping, https://www.saferproducts.gov/, https://www.plannedparenthood.org/learn
- All checks passed: True

## Images
- Generation status: pass
- Model: opus-image-1.5 via configured custom Sub2API Responses API /v1/responses with image_generation tool
- `upload/blog/assets/male-masturbator-device-types-guide-opus-cover.png`: pass; response `resp_0f2cdd4c38510b9f016a5d6d7bfc68819baed7f31cc3f2ca87`
- `upload/blog/assets/rabbit-vibrator-ears-fit-guide-opus-cover.png`: pass; response `resp_0b4ae80f235c7aa3016a5d6dab58ac8198a4370078eaca3459`

## Deployment and live verification
- Deploy status: pass
- Method: targeted rsync to root@153.75.235.56:/var/www/myopencart/upload
- Permissions: www-data:www-data; dirs 755; files 644
- Live verification: pass
- Verified URLs: https://shoplovanest.com/blog/male-masturbator-device-types-guide/, https://shoplovanest.com/blog/rabbit-vibrator-ears-fit-guide/, https://shoplovanest.com/blog/, https://shoplovanest.com/sitemap.xml

## Email
- Recipient: yuanzhigang20@gmail.com
- Subject: ShopLovaNest Daily Blog Deployment Complete - 2026-07-20
- Message file: `output/daily_blog_2026-07-20_success.eml`
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
