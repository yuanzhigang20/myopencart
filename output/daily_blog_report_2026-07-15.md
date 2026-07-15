# ShopLovaNest Daily Blog Automation Report — 2026-07-15

## Status
In progress — two keyword-sourced articles have been generated locally, mandatory `opus-image-1.5` topic images are now generated successfully, and local validation passes. Remaining steps: commit/push, targeted deploy, live verification, and msmtp success email.

## Selected topics from mandatory keyword files
The files `output/merged_keyword_research_2026-06-25.csv` and `output/keyword_to_url_mapping_2026-06-25.csv` were inspected before topic selection.

1. `adult-sensory-toys-comfort-guide`
   - URL target: `https://shoplovanest.com/blog/adult-sensory-toys-comfort-guide/`
   - Primary keywords: `adult sensory toys`, `toys that are for adults to chew on`, `texture-focused adult toys`, `quiet adult sensory toys`, `body-safe sensory adult toys`
   - Source: `merged_keyword_research_2026-06-25.csv` rows `adult sensory toys` (Volume 1300) and `toys that are for adults to chew on` (Volume 1000); `keyword_to_url_mapping_2026-06-25.csv` mapped both to broad manual review, so a distinct buyer-safety article was created to answer sensory/texture/noise/oral-use ambiguity.
   - Intent cluster: texture, tactile comfort, oral-use ambiguity, material labeling, quiet/privacy expectations, cleaning limits, storage, and red flags for unsafe chew or medical-style claims.

2. `body-safe-glass-adult-toys-guide`
   - URL target: `https://shoplovanest.com/blog/body-safe-glass-adult-toys-guide/`
   - Primary keywords: `body safe glass sex toys made of`, `glass adult toys`, `body-safe glass adult toys`, `glass sex toy care`, `nonporous adult toy materials`
   - Source: `merged_keyword_research_2026-06-25.csv` row `body safe glass sex toys made of` (Volume 720); `keyword_to_url_mapping_2026-06-25.csv` mapped it as secondary to a silicone-cleaning URL, but existing broad glass/material pages did not provide this exact material/inspection answer.
   - Intent cluster: what glass products are made of, nonporous claims, borosilicate vs vague glass labels, chip inspection, temperature caution, cleaning, storage, lubricant compatibility, and red flags.

Skipped/avoided groups included fidget, Toy Story/media, pets/dogs, local-only, competitor/navigation ambiguity, and unsupported medical/psychological claim angles.

## Local files prepared
- `upload/blog/adult-sensory-toys-comfort-guide/index.html`
- `upload/blog/body-safe-glass-adult-toys-guide/index.html`
- `upload/blog/assets/adult-sensory-toys-comfort-guide-opus-cover.png`
- `upload/blog/assets/body-safe-glass-adult-toys-guide-opus-cover.png`
- `upload/blog/index.html` updated locally
- `upload/sitemap.xml` updated locally with lastmod and image metadata
- `output/generate_daily_blogs_2026_07_15.py`
- `output/validate_daily_blog_2026_07_15.py`
- `output/daily_blog_automation_state.json`
- `output/daily_blog_report_2026-07-15.md`

## Local validation
Local validation passed after generating required images.

- SEO title <60 chars: pass
- Meta description <155 chars: pass
- Exactly one H1: pass
- Google tag `G-P2LJRXN3D1` script/config exactly once immediately after `<head>`: pass
- Word count: pass
  - `adult-sensory-toys-comfort-guide`: 1377 words
  - `body-safe-glass-adult-toys-guide`: 1225 words
- Quick Answer section: pass
- Red Flags section: pass
- FAQ + FAQPage JSON-LD: pass
- 2-4 related blog links: pass
- 1-3 relevant product/support links: pass
- Authority references: pass
- Banned/unsafe term scan: pass
- Image SEO metadata in page, OG/Twitter, JSON-LD, and sitemap: pass
- Quality score: 100 / 100 for both articles

## Authority references included
- CPSC safety education / choking-prevention resources
- FTC online shopping guidance
- FDA cosmetics labeling guide
- Planned Parenthood consent guidance
- ASTM glass and ceramic standards overview
- Cleveland Clinic safer sex discussion guide

## Image generation status
Pass.

Required model: `opus-image-1.5` via the configured custom endpoint.

Route used: Sub2API-compatible OpenAI Responses API `/v1/responses` with an `image_generation` tool. The legacy OpenAI Images endpoint `/v1/images/generations` was not used. A first Python `urllib` direct request hit Cloudflare 403 / code 1010, then a curl-based Responses API request completed with `status=completed` for both images.

Generated files:
- `upload/blog/assets/adult-sensory-toys-comfort-guide-opus-cover.png`
- `upload/blog/assets/body-safe-glass-adult-toys-guide-opus-cover.png`

## Git / deploy / email
- Commit: pending
- Push: pending
- Deploy: pending
- Live verification: pending
- Email: pending
