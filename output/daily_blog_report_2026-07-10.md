# ShopLovaNest Daily Blog Automation Report — 2026-07-10

Status: **INCOMPLETE — deployment blocked by production SSH banner timeout**

Updated: 2026-07-10T09:00:42+08:00 Asia/Shanghai

## Selected keyword-sourced topics

1. **Best Male Masturbator: Buyer Safety Checklist**
   - Slug: `best-male-masturbator-buyer-guide`
   - URL: https://shoplovanest.com/blog/best-male-masturbator-buyer-guide/
   - Primary keywords: best-fit wearable male masturbator, best male male masturbator, male masturbator, male masturbators, automatic male masturbator
   - Intent cluster: Best male masturbator comparison intent — fit range, stability, motor and control claims, body-contact material, sleeve care, charging, privacy, and seller transparency
   - Keyword source: output/merged_keyword_research_2026-06-25.csv rows: male masturbator (Volume 14800), male masturbators (9900), best male masturbator (4400), automatic male masturbator (1900), best-fit wearable male masturbator (1000), best male male masturbator (880); output/keyword_to_url_mapping_2026-06-25.csv maps broad male-masturbator intent to education, but the comparison, material, fit, and cleaning intent was not covered by a dedicated page. Created as a buyer-safety checklist, distinct from the existing male masturbator and automatic male masturbator guides.

2. **Cordless Wand Massager: Charging Buyer Guide**
   - Slug: `cordless-wand-massager-guide`
   - URL: https://shoplovanest.com/blog/cordless-wand-massager-guide/
   - Primary keywords: cordless wand massager, cordless wand massagers, wand massager, usb charging adult toys, vibrator charging cable
   - Intent cluster: Cordless wand massager ownership intent — battery specs, cable/port type, magnetic charging contacts, travel lock, charging safety, water-resistance, cleaning, storage, and privacy checks
   - Keyword source: output/merged_keyword_research_2026-06-25.csv rows: cordless wand massager (Volume 480), rechargeable vibraters (590), waterproof vibrator (720), USB/charging and vibrator buyer queries across adult-toys and rechargeable-vibrator seed files; output/keyword_to_url_mapping_2026-06-25.csv maps charging-related intent to education but did not include a dedicated rechargeable-vibrator ownership checklist. Created as a battery/charging safety and buyer-transparency page, distinct from wand massager and power-adapter guides.

## Local generation and quality checks

- Article quota: 2
- Articles generated: 2
- Blog index updated locally: yes
- Sitemap updated locally: yes
- Required keyword files inspected: `output/merged_keyword_research_2026-06-25.csv`, `output/keyword_to_url_mapping_2026-06-25.csv`
- Image model: opus-image-1.5 via configured custom endpoint
- Generated/used image assets:
  - `upload/blog/assets/best-male-masturbator-buyer-guide-opus-cover.png`
  - `upload/blog/assets/cordless-wand-massager-guide-opus-cover.png`
- Local validation status: pass
- Minimum quality score: 100
- Content checks: title/meta length, exactly one H1, Google tag immediately after head, 1000+ words, Quick Answer, Red Flags, FAQPage JSON-LD, authority references, related/internal/product/support links, image SEO metadata, sitemap image metadata, natural readability, topic-specific depth, banned-term absence.

## Commit / push

- Commit: `7877e4dbc3` (`Add ShopLovaNest daily blogs for 2026-07-10`)
- Push status: pushed to `origin/master` (ahead/behind 0/0 when checked)

## Deployment status

**Blocked.** Targeted deploy was attempted to:

`root@153.75.235.56:/var/www/myopencart/upload`

Failure details:

- TCP port 22 sometimes reports open, but SSH repeatedly fails before authentication.
- Error observed: `Connection timed out during banner exchange` / `Connection to 153.75.235.56 port 22 timed out`.
- Because SSH does not complete the banner exchange, rsync deployment and remote permission fixes cannot run reliably.

## Live verification status

Partial checks before/around retry:

- `https://shoplovanest.com/blog/best-male-masturbator-buyer-guide/` returned HTTP 200 but served the OpenCart homepage title instead of the generated static article. This URL requires a successful deploy retry.
- `https://shoplovanest.com/blog/cordless-wand-massager-guide/` returned HTTP 200 and contained expected markers: title, Quick Answer, Red Flags, FAQPage, and Google tag occurrences.
- Blog index and sitemap returned HTTP 200, but full verification is pending a clean deploy retry.

## Email status

- Status: **not sent**
- Reason: success email may only be sent after deploy and live verification pass. Deployment is blocked by SSH banner timeout.

## Next retry action

On the next scheduled check, retry only the incomplete deployment/verification/email steps. Do **not** create extra July 10 articles. Deploy these files/folders only:

- `upload/blog/best-male-masturbator-buyer-guide/`
- `upload/blog/cordless-wand-massager-guide/`
- `upload/blog/assets/best-male-masturbator-buyer-guide-opus-cover.png`
- `upload/blog/assets/cordless-wand-massager-guide-opus-cover.png`
- `upload/blog/index.html`
- `upload/sitemap.xml`

After successful deploy, fix ownership/permissions, verify both article URLs plus blog index and sitemap, then send the msmtp success email and mark the state complete.
