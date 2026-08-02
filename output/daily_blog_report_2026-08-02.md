# Daily Blog Automation Report - 2026-08-02

- Timezone: Asia/Shanghai
- Status: complete
- Completed at: 2026-08-02T12:38:33.566739+08:00
- Quota: exactly 2 articles
- Commit: `16a61f98cb57` pushed to origin/master
- Keyword source files read: output/merged_keyword_research_2026-06-25.csv; output/keyword_to_url_mapping_2026-06-25.csv

## Articles

### Silicone Anal Lube Safety Guide
- Slug: `silicone-anal-lube-safety-guide`
- Live URL: https://shoplovanest.com/blog/silicone-anal-lube-safety-guide/
- Primary keywords: silicone anal lube, silicone based anal lube, is silicone lube safe
- Intent cluster: Silicone anal lube buyer-safety intent — shoppers want to know when silicone lubricant makes sense, what it can be used with, what materials it may damage, how cleanup differs, and which listing claims deserve caution.
- Keyword source rationale: Read output/merged_keyword_research_2026-06-25.csv and output/keyword_to_url_mapping_2026-06-25.csv. Selected silicone anal lube, silicone based anal lube, silicone personal lube, best silicone based lube, and is silicone lube safe from the silicone-lube cluster. Clustered them into one anal-use buyer-safety intent focused on condom compatibility, silicone-toy conflicts, cleanup, ingredient transparency, and checkout red flags rather than thin keyword pages.
- Local validation: PASS; quality score 100; word count 1271; title length 31; meta length 139
- Required checks: one H1=True; gtag script=1; gtag config=1; gtag immediately after head=True; Quick Answer=True; Red Flags=True; FAQPage schema=True; authority refs=4; related blog links=4; product/support links=3; image SEO metadata=True; banned scan pass=True
- Live verification: PASS; HTTP 200; title/meta present; H1 count 1; gtag script/config 1/1; authority refs 4; image SEO metadata True

### Vibrating Kegel Balls Safety Guide
- Slug: `vibrating-kegel-balls-safety-guide`
- Live URL: https://shoplovanest.com/blog/vibrating-kegel-balls-safety-guide/
- Primary keywords: vibrating kegel balls, silicone kegel balls, kegel balls for beginners
- Intent cluster: Vibrating kegel balls buyer-safety intent — shoppers want a beginner-friendly checklist for size, weight, retrieval features, vibration controls, charging limits, cleaning, body-contact materials, and claim red flags.
- Keyword source rationale: Read output/merged_keyword_research_2026-06-25.csv and output/keyword_to_url_mapping_2026-06-25.csv. Selected vibrating kegel balls, silicone kegel balls, silicone kegel ball, kegel balls for beginners, and kegel balls for men from the kegel-balls cluster. Clustered them into one buyer-safety intent focused on size, weight, retrieval design, controls, cleaning, charging, and cautious claims rather than medical promises.
- Local validation: PASS; quality score 100; word count 1289; title length 34; meta length 139
- Required checks: one H1=True; gtag script=1; gtag config=1; gtag immediately after head=True; Quick Answer=True; Red Flags=True; FAQPage schema=True; authority refs=4; related blog links=4; product/support links=3; image SEO metadata=True; banned scan pass=True
- Live verification: PASS; HTTP 200; title/meta present; H1 count 1; gtag script/config 1/1; authority refs 2; image SEO metadata True

## Image Generation
- Status: pass
- Model: opus-image-1.5 via configured custom endpoint
- upload/blog/assets/silicone-anal-lube-safety-guide-opus-cover.png: pass; endpoint=responses; model=opus-image-1.5; bytes=2351576
- upload/blog/assets/vibrating-kegel-balls-safety-guide-opus-cover.png: pass; endpoint=responses; model=opus-image-1.5; bytes=2317258

## Blog Index and Sitemap
- Blog index: HTTP 200; links both new articles: True
- Sitemap: HTTP 200; includes URLs: True; lastmod 2026-08-02: True; image metadata: True

## Deployment
- Method: targeted rsync only for the two new blog folders, two image assets, blog index, and sitemap.xml.
- Permissions fixed: www-data:www-data; dirs 755; files 644.

## Email
- Recipient: yuanzhigang20@gmail.com
- Tool: /opt/homebrew/bin/msmtp with /Users/grant/.msmtprc
- Subject: ShopLovaNest Daily Blog Deployment Complete - 2026-08-02
- Status: sent/accepted; msmtp exit code 0

## Final Completion Rule
All required steps are complete: 2 keyword-source articles generated, index and sitemap updated, validation passed, commit pushed, deployed to production, live verified, and success email accepted by msmtp.
