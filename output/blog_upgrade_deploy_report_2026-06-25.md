# Blog Upgrade & Deployment Report — 2026-06-25

## Scope
Upgraded the remaining existing ShopLovaNest adult wellness blog articles after first-batch commit eb53783e83". No new articles were created. Blog static HTML structure was preserved and each page keeps exactly one Google tag script/config pair.

## Edited slugs
1. how-to-choose-a-vibrator
2. quiet-vibrator-guide
3. bullet-vibrator-guide
4. vibrators-for-beginners
5. body-safe-sex-toys
6. adult-toy-cleaner-guide
7. adult-toy-gift-guide
8. adult-toy-storage-guide
9. adult-toys-for-couples
10. anal-toys-for-beginners
11. beginner-lubricant-guide
12. cock-ring-guide
13. discreet-shipping-adult-toys
14. adult-toy-materials-guide
15. adult-toy-privacy-guide
16. how-to-clean-silicone-sex-toys
17. how-to-use-kegel-balls-safely
18. kegel-balls-guide
19. male-masturbator-guide
20. rabbit-vibrator-guide
21. rechargeable-vibrator-guide
22. silicone-lube-guide
23. travel-with-adult-toys
24. wand-massager-guide
25. waterproof-vibrator-guide

## Quality checklist results
Checklist criteria: search intent, buyer usefulness, natural English, keyword naturalness, no stuffing, no explicit/vulgar language, no unsupported health claims, internal links, title/meta, word count, and Google tag count.

All edited pages scored >=85. Local automated validation output:

```csv
slug,words,title_len,meta_len,gtag_script,gtag_config,links,banned,score
how-to-choose-a-vibrator,1865,44,133,1,1,14,,100
quiet-vibrator-guide,1738,49,133,1,1,14,,100
bullet-vibrator-guide,1720,52,127,1,1,14,,100
vibrators-for-beginners,1713,56,133,1,1,14,,100
body-safe-sex-toys,1764,41,127,1,1,14,,100
adult-toy-cleaner-guide,1845,49,129,1,1,14,,100
adult-toy-gift-guide,1731,47,144,1,1,14,,100
adult-toy-storage-guide,1730,49,140,1,1,14,,100
adult-toys-for-couples,1726,47,141,1,1,14,,100
anal-toys-for-beginners,1750,49,132,1,1,14,,100
beginner-lubricant-guide,1708,48,145,1,1,14,,100
cock-ring-guide,1720,43,124,1,1,14,,100
discreet-shipping-adult-toys,1722,47,139,1,1,14,,100
adult-toy-materials-guide,1712,48,136,1,1,14,,100
adult-toy-privacy-guide,1712,45,137,1,1,14,,100
how-to-clean-silicone-sex-toys,1870,44,131,1,1,14,,100
how-to-use-kegel-balls-safely,1856,47,135,1,1,14,,100
kegel-balls-guide,1713,50,137,1,1,14,,100
male-masturbator-guide,1696,46,136,1,1,14,,100
rabbit-vibrator-guide,1712,49,136,1,1,14,,100
rechargeable-vibrator-guide,1689,50,131,1,1,14,,100
silicone-lube-guide,1714,43,138,1,1,14,,100
travel-with-adult-toys,1775,49,143,1,1,14,,100
wand-massager-guide,1709,43,121,1,1,14,,100
waterproof-vibrator-guide,1680,47,136,1,1,14,,100
```

## Commit and push
- Blog upgrade commit: `442f0d1e5f` (`Upgrade remaining adult wellness SEO blog articles`)
- Pushed to `origin/master` after one transient SSH/proxy failure; retry succeeded.

## Deployment
Changed blog files only were deployed to production with safe rsync file list:

```bash
git diff --name-only HEAD~1..HEAD -- upload/blog | sed 's#^upload/blog/##' > /tmp/changed_blog_files.txt
rsync -avz --relative --files-from=/tmp/changed_blog_files.txt upload/blog/ root@153.75.235.56:/var/www/myopencart/upload/blog/
```

Post-rsync permission correction was required because article directories/files arrived as owner `501:staff` with restrictive modes, causing 403 responses. Corrected only the changed blog slug directories/files:

```bash
ssh root@153.75.235.56 'while read f; do d="/var/www/myopencart/upload/blog/"; chown www-data:www-data "" "/index.html"; chmod 755 ""; chmod 644 "/index.html"; done' < /tmp/changed_blog_files.txt
```

## Live verification
Representative live URL verification after permission correction:

```text
https://shoplovanest.com/blog/	200	title=Sexual Wellness Guides | ShopLovaNest Blog	meta_len=160	gtag=1/1	marker=True
https://shoplovanest.com/blog/how-to-choose-a-vibrator/	200	title=How to Choose a Vibrator: Decision Checklist	meta_len=133	gtag=1/1	marker=True
https://shoplovanest.com/blog/quiet-vibrator-guide/	200	title=Quiet Vibrator Guide: Privacy and Noise Checklist	meta_len=133	gtag=1/1	marker=True
https://shoplovanest.com/blog/bullet-vibrator-guide/	200	title=Bullet Vibrator Guide: Features and Buying Checklist	meta_len=127	gtag=1/1	marker=True
https://shoplovanest.com/blog/vibrators-for-beginners/	200	title=Vibrators for Beginners: Choose the Right First Massager	meta_len=133	gtag=1/1	marker=True
https://shoplovanest.com/blog/body-safe-sex-toys/	200	title=Body-Safe Sex Toys: Material Safety Guide	meta_len=127	gtag=1/1	marker=True
https://shoplovanest.com/blog/wand-massager-guide/	200	title=Wand Massager Guide: Power, Noise, and Care	meta_len=121	gtag=1/1	marker=True
```

Result: blog index and representative upgraded article URLs return HTTP 200, include title/meta where applicable, keep Google tag count at 1/1, and contain changed-content markers.

## Notes
- Skipped unsafe/irrelevant keyword intents from the mapping such as fidget, entertainment/media, dogs/pets, location-only, and ambiguous brand/navigation terms unless useful in a compliant buyer-safety context.
- Existing unrelated workspace changes remain outside this commit/report, including keyword Excel archive/deletion state and mapping files from earlier work.
