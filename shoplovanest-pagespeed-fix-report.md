# ShopLovaNest PageSpeed Fix Report - 2026-06-27

## Source report
- URL: https://pagespeed.web.dev/analysis/https-shoplovanest-com/j20fimnuaw?utm_source=search_console&form_factor=mobile&hl=zh_CN
- Mobile before: Performance 68, Accessibility 88, Best Practices 100, SEO 100
- Key metrics shown in report: FCP 3.3s, LCP 15.8s, TBT 50ms, CLS 0, Speed Index 3.3s

## Issues identified
- LCP dominated by large image delivery: homepage hero PNG ~1.8MB and beginner banner PNG ~1.7MB.
- Multiple above/below-fold homepage images were eager loaded or missing dimensions.
- Font Awesome CSS from CDN was render-blocking.
- Bootstrap JS loaded synchronously at page end.
- Footer had placeholder social links with `href="#"`.
- Some tap targets were under Lighthouse's comfortable target size threshold.
- Sitemap root lastmod did not reflect homepage/template changes.

## Fixes applied
- Generated optimized JPEG versions:
  - `/image/catalog/lovanest/home-hero-optimized.jpg` ~80KB, down from ~1.8MB PNG.
  - `/image/catalog/lovanest/beginner-banner-optimized.jpg` ~70KB, down from ~1.7MB PNG.
- Updated homepage CSS background image-set to prefer optimized JPEG with original PNG fallback.
- Added preconnect hints for CDN origins.
- Changed Font Awesome CSS to preload + async stylesheet with noscript fallback.
- Deferred Bootstrap bundle script.
- Removed placeholder footer social links.
- Removed production console error logging from cart handler.
- Changed homepage best-seller/category images to lazy loading and added explicit width/height where missing.
- Increased key CTA/button min-height to 44px.
- Updated root sitemap lastmod to 2026-06-27.
- Repaired production directory permissions for `/upload`, `/upload/image`, `/upload/catalog`, and blog/static assets after rsync exposed restrictive local permissions.

## Deployment verification
- `nginx -t`: successful.
- Live homepage HTTP 200 and contains optimized image references.
- Live optimized hero image HTTP 200, 80,532 bytes, image/jpeg.
- Live optimized beginner banner HTTP 200, 69,785 bytes, image/jpeg.
- Live sitemap HTTP 200 and root lastmod `2026-06-27` present.
- Live homepage has no `loading="eager"` images and has 17 lazy images.

## Retest note
- PageSpeed API retest hit HTTP 429 quota/rate limit after the user's report was opened. Re-run PSI later to get updated score.
