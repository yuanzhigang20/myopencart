# shoplovanest.com SEO implementation report

Date: 2026-06-19

## Phase 1 - Technical/on-page SEO implemented

- Added canonical/prev/next link output in the shared header template.
- Added default robots meta, Open Graph, and Twitter card metadata.
- Added JSON-LD support to the OpenCart Document library and header template.
- Added WebSite JSON-LD on homepage.
- Added Product JSON-LD with Offer data on product pages.
- Added CollectionPage JSON-LD on category pages.
- Replaced demo footer copy with trust-oriented store copy.
- Created production `robots.txt` that allows public product/category/image crawling and blocks admin/account/checkout/search/filter URLs.
- Created production `sitemap.xml` for homepage, category pages, product pages, information pages, and contact page.

## Phase 2 - GSC submission package

Submit this sitemap in Google Search Console:

- `https://shoplovanest.com/sitemap.xml`

Recommended GSC property:

- Domain property: `shoplovanest.com`
- URL-prefix property fallback: `https://shoplovanest.com/`

First URLs to inspect/request indexing:

- `https://shoplovanest.com/`
- `https://shoplovanest.com/index.php?route=product/category&language=en-gb&path=101`
- `https://shoplovanest.com/index.php?route=product/product&language=en-gb&product_id=1001`
- `https://shoplovanest.com/index.php?route=product/product&language=en-gb&product_id=1006`

## Phase 3 - Ongoing GSC analysis plan

Once GSC has data, review weekly:

- Pages indexed vs. discovered/crawled but not indexed.
- Query impressions and CTR by product/category page.
- Duplicate/canonical warnings.
- Core Web Vitals and mobile usability.
- Sitemap submitted/processed status.

Recommended next iteration after data appears:

- Rewrite low-CTR titles/descriptions.
- Expand category landing copy based on impressions.
- Add FAQ content only where visible and useful.
- Build internal links from guide/information pages into key product categories.

## Notes

- No public URL structure was removed.
- No fake reviews or fake ratings were added.
- Checkout/account routes remain blocked from indexing.
