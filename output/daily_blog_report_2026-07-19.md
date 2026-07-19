# Daily ShopLovaNest Blog Automation Report - 2026-07-19

- Status: validated_pending_commit
- Quota: 2 new articles
- Keyword source files read:
  - `output/merged_keyword_research_2026-06-25.csv`
  - `output/keyword_to_url_mapping_2026-06-25.csv`

## Selected articles
### Adult Toy Cleaner vs Soap: What to Check
- Slug: `adult-toy-cleaner-vs-soap-guide`
- URL: https://shoplovanest.com/blog/adult-toy-cleaner-vs-soap-guide/
- Primary keywords: adult toy cleaner, sex toy cleaning spray, toy cleaner spray, toy-safe cleaning, adult toy care
- Intent cluster: Adult toy cleaner comparison intent — cleaner vs mild soap, sprays/wipes, material compatibility, electronics caution, label reading, storage, and checkout red flags
- Keyword source note: Read output/merged_keyword_research_2026-06-25.csv and output/keyword_to_url_mapping_2026-06-25.csv. Selected adult toy cleaner (Volume 1900) and related cleaner/spray intent from the adult-toys and cleaning-storage cluster. Existing cleaning guides cover silicone care and common mistakes; this article focuses on buyer comparison between toy cleaner, spray, wipes, and mild soap instead of a generic cleaning routine.

### Mini Bullet Vibrator: Size & Noise Guide
- Slug: `mini-bullet-vibrator-size-noise-guide`
- URL: https://shoplovanest.com/blog/mini-bullet-vibrator-size-noise-guide/
- Primary keywords: mini bullet vibrator, small bullet vibrator, silver bullet vibrator, bullet vibrators, quiet vibrator
- Intent cluster: Mini bullet vibrator buyer intent — compact size tradeoffs, noise expectations, controls, charging/battery, material clarity, travel privacy, and checkout red flags
- Keyword source note: Read output/merged_keyword_research_2026-06-25.csv and output/keyword_to_url_mapping_2026-06-25.csv. Selected mini bullet vibrator (Volume 590), small bullet vibrator (Volume 390), silver bullet vibrator (Volume 1000), bullet vibrators (Volume 1900), and supporting quiet vibrator intent from the compact-vibrator cluster. Existing bullet and quiet-vibrator pages are broad; this article clusters the distinct mini-size/noise/controls buyer intent.

## Image generation

- Status: pass
- Model: opus-image-1.5 via configured custom Sub2API Responses API /v1/responses with image_generation tool
- upload/blog/assets/adult-toy-cleaner-vs-soap-guide-opus-cover.png: pass; response `resp_0e631029a58966f4016a5c1b740200819bbc697f122c691ad8`
- upload/blog/assets/mini-bullet-vibrator-size-noise-guide-opus-cover.png: pass; response `resp_0ba823e199d717f5016a5c1ba1717c819a9a4441d967b5e768`

## Local validation

- Status: pass
- Minimum quality score: 100
### adult-toy-cleaner-vs-soap-guide
- Title length: 40; meta length: 118; H1 count: 1; word count: 1159; quality score: 100
- Authority links: https://www.fda.gov/cosmetics/cosmetics-labeling-regulations/cosmetics-labeling-guide, https://www.epa.gov/coronavirus/safe-and-effective-disinfectant-use, https://consumer.ftc.gov/articles/online-shopping, https://www.saferproducts.gov/
- Checks passed: True
### mini-bullet-vibrator-size-noise-guide
- Title length: 44; meta length: 121; H1 count: 1; word count: 1160; quality score: 100
- Authority links: https://www.iec.ch/ip-ratings, https://consumer.ftc.gov/articles/online-shopping, https://www.tsa.gov/travel/security-screening/whatcanibring/all, https://www.saferproducts.gov/
- Checks passed: True

## Pending operations

Commit, push, deploy, live verification, and success email are pending after local validation.
