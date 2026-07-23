# ShopLovaNest Daily Blog Report - 2026-07-23
## Status
- Complete: generated exactly 2 articles, validated, committed/pushed, deployed, verified live, and sent success email accepted by msmtp.
## Articles
- Connected Adult Toys: Privacy & Security Guide
  - URL: https://shoplovanest.com/blog/connected-adult-toys-privacy-security-guide/
  - Slug: `connected-adult-toys-privacy-security-guide`
  - Primary keywords: app controlled adult toys, remote control adult toys, remote adult toys, long distance adult toys
  - Intent cluster: Connected adult wellness device privacy intent — app permissions, Bluetooth range, account safety, firmware updates, remote access, long-distance consent, support, and data-minimization red flags
  - Keyword source: Read output/merged_keyword_research_2026-06-25.csv and output/keyword_to_url_mapping_2026-06-25.csv. Selected app controlled adult toys (Volume 720), remote control adult toys (720), remote adult toys (590), and long distance adult toys (590). Mapping assigns these to broad buying-decision pages, so this article targets a distinct buyer-safety intent: connected-device privacy, permissions, updates, account control, and long-distance consent rather than a thin product list.
- Body-Safe Glass Toys: Material Guide
  - URL: https://shoplovanest.com/blog/body-safe-glass-toys-material-guide/
  - Slug: `body-safe-glass-toys-material-guide`
  - Primary keywords: body safe glass sex toys made of
  - Intent cluster: Body-safe glass material intent — borosilicate/soda-lime claims, nonporous surface, finish quality, chips and cracks, temperature caution, cleaning, storage, and seller red flags
  - Keyword source: Read output/merged_keyword_research_2026-06-25.csv and output/keyword_to_url_mapping_2026-06-25.csv. Selected body safe glass sex toys made of (Volume 720) from the body-safe-sex-toys file. The mapping points to silicone cleaning, but glass material and finish-quality intent is distinct enough for a dedicated buyer-safety article that avoids cannibalizing silicone care pages.
## Keyword source files read
- `output/merged_keyword_research_2026-06-25.csv`
- `output/keyword_to_url_mapping_2026-06-25.csv`
## Image generation
- Status: pass
- Model: opus-image-1.5 via configured custom Sub2API Responses API /v1/responses with image_generation tool
- `upload/blog/assets/connected-adult-toys-privacy-security-guide-opus-cover.png`
- `upload/blog/assets/body-safe-glass-toys-material-guide-opus-cover.png`

## Content quality validation
- Status: pass
- `connected-adult-toys-privacy-security-guide`: quality 100, words 1795, title 50, meta 139, FAQs 5, authority refs 4, pass=True
  - References: https://consumer.ftc.gov/articles/protect-your-personal-information-hackers-and-scammers, https://consumer.ftc.gov/articles/online-shopping, https://www.nist.gov/itl/smallbusinesscyber/guidance-topic/internet-things, https://www.cisa.gov/news-events/news/using-caution-mobile-devices
- `body-safe-glass-toys-material-guide`: quality 100, words 1725, title 36, meta 136, FAQs 5, authority refs 4, pass=True
  - References: https://www.fda.gov/food/chemical-contaminants-pesticides/environmental-contaminants-food, https://www.saferproducts.gov/, https://consumer.ftc.gov/articles/online-shopping, https://www.corning.com/worldwide/en/innovation/materials-science/glass/borosilicate-glass.html

## Sitemap and index checks
{
  "sitemap_checks": {
    "connected-adult-toys-privacy-security-guide": {
      "url_present": true,
      "lastmod": true,
      "image_metadata": true
    },
    "body-safe-glass-toys-material-guide": {
      "url_present": true,
      "lastmod": true,
      "image_metadata": true
    }
  },
  "index_checks": {
    "links_new_articles": true,
    "blog_count_meta_updated": true,
    "expected_count": 137
  }
}

## Deployment / live verification / email
- Commit: 6ee559ae0b
- Deploy: pass via targeted rsync; permissions fixed.
- Live verification: pass at 2026-07-23T08:40:47.304609+08:00
- Email: sent_accepted to yuanzhigang20@gmail.com at 2026-07-23T08:41:13.674924+08:00
