-- Lovanest round 2 wellness attributes and scenario product enrichment
-- Applied to production on 2026-06-19.

START TRANSACTION;

INSERT INTO oc_attribute_group (attribute_group_id, sort_order) VALUES (20, 1)
ON DUPLICATE KEY UPDATE sort_order=VALUES(sort_order);

INSERT INTO oc_attribute_group_description (attribute_group_id, language_id, name) VALUES (20, 1, 'Wellness Details')
ON DUPLICATE KEY UPDATE name=VALUES(name);

INSERT INTO oc_attribute (attribute_id, attribute_group_id, sort_order) VALUES
(20,20,1),(21,20,2),(22,20,3),(23,20,4),(24,20,5),(25,20,6),(26,20,7),(27,20,8),(28,20,9)
ON DUPLICATE KEY UPDATE attribute_group_id=VALUES(attribute_group_id), sort_order=VALUES(sort_order);

INSERT INTO oc_attribute_description (attribute_id, language_id, name) VALUES
(20,1,'Material'),(21,1,'Size & Fit'),(22,1,'Waterproof'),(23,1,'Power / Charging'),(24,1,'Noise Level'),(25,1,'Package Includes'),(26,1,'Best For'),(27,1,'Cleaning'),(28,1,'Discreet Shipping')
ON DUPLICATE KEY UPDATE name=VALUES(name);

DELETE FROM oc_product_attribute WHERE product_id BETWEEN 1001 AND 1006 AND attribute_id BETWEEN 20 AND 28 AND language_id=1;

INSERT INTO oc_product_attribute (product_id, attribute_id, language_id, text) VALUES
(1001,20,1,'Soft satin-look polyester blend with lace trim'),(1001,21,1,'Plus-size relaxed chemise fit; check selected size before purchase'),(1001,22,1,'Not waterproof; fabric intimatewear'),(1001,23,1,'No charging required'),(1001,24,1,'Silent'),(1001,25,1,'1 chemise nightdress in discreet outer packaging'),(1001,26,1,'Solo wellness, beginner friendly, private nightwear gifting'),(1001,27,1,'Hand wash cold, line dry, store clean and dry'),(1001,28,1,'Ships in plain packaging with no explicit wording'),
(1002,20,1,'Lightweight lace-look stretch fabric with slim straps'),(1002,21,1,'Low-rise minimal fit; choose size according to waist/hip measurement'),(1002,22,1,'Not waterproof; fabric intimatewear'),(1002,23,1,'No charging required'),(1002,24,1,'Silent'),(1002,25,1,'1 thong panty in discreet outer packaging'),(1002,26,1,'Beginner friendly, solo wellness, layering with intimate outfits'),(1002,27,1,'Hand wash cold, line dry, avoid bleach'),(1002,28,1,'Ships in plain packaging with no explicit wording'),
(1003,20,1,'Soft stretch costume fabric with lace-look details'),(1003,21,1,'Roleplay lingerie set; check sizing and included pieces before purchase'),(1003,22,1,'Not waterproof; fabric costume intimatewear'),(1003,23,1,'No charging required'),(1003,24,1,'Silent'),(1003,25,1,'1 maid-inspired lingerie set in discreet outer packaging'),(1003,26,1,'For couples, gift sets, private roleplay styling'),(1003,27,1,'Hand wash gently, dry flat or line dry'),(1003,28,1,'Ships in plain packaging with no explicit wording'),
(1004,20,1,'Lightweight costume fabric with lace-look trim'),(1004,21,1,'Classic roleplay silhouette; review size options before purchase'),(1004,22,1,'Not waterproof; fabric costume intimatewear'),(1004,23,1,'No charging required'),(1004,24,1,'Silent'),(1004,25,1,'1 classic maid costume lingerie set in discreet outer packaging'),(1004,26,1,'For couples, gift sets, private roleplay occasions'),(1004,27,1,'Hand wash cold, line dry, store away from heat'),(1004,28,1,'Ships in plain packaging with no explicit wording'),
(1005,20,1,'Lightweight fabric with lace trim and padded support'),(1005,21,1,'Two-piece chemise set; choose size according to bust/waist/hip'),(1005,22,1,'Not waterproof; fabric intimatewear'),(1005,23,1,'No charging required'),(1005,24,1,'Silent'),(1005,25,1,'1 padded chemise two-piece set in discreet outer packaging'),(1005,26,1,'Beginner friendly, couples, private gifting'),(1005,27,1,'Hand wash cold, reshape gently, line dry'),(1005,28,1,'Ships in plain packaging with no explicit wording'),
(1006,20,1,'Soft lace-trim fabric with padded support'),(1006,21,1,'Deep V backless nightdress set; check size and support fit'),(1006,22,1,'Not waterproof; fabric intimatewear'),(1006,23,1,'No charging required'),(1006,24,1,'Silent'),(1006,25,1,'1 deep V nightdress set in discreet outer packaging'),(1006,26,1,'For couples, gift sets, private nightwear styling'),(1006,27,1,'Hand wash cold, line dry, do not tumble dry'),(1006,28,1,'Ships in plain packaging with no explicit wording');

UPDATE oc_product_description SET description = CONCAT(
  description,
  '<h3>Private Wellness Notes</h3><p>This item is selected for a private, clean adult wellness shopping experience. Review the material, fit and care details before purchase.</p>',
  '<h3>Discreet Delivery</h3><p>Orders are prepared with plain outer packaging and no explicit wording on the outside parcel.</p>',
  '<h3>Care & Hygiene</h3><p>For intimate apparel, wash before first wear, clean gently after use, dry fully, and store in a clean private place.</p>'
)
WHERE product_id BETWEEN 1001 AND 1006 AND language_id=1 AND description NOT LIKE '%Private Wellness Notes%';

UPDATE oc_product SET image='catalog/adult-wellness/curated-intimates-premium/intimatewear-01-plus-size-satin-lace-chemise-nightdress-premium.jpg' WHERE product_id=1001;
UPDATE oc_product SET image='catalog/adult-wellness/curated-intimates-premium/intimatewear-02-low-rise-lace-strap-thong-panty-premium.jpg' WHERE product_id=1002;
UPDATE oc_product SET image='catalog/adult-wellness/curated-intimates-premium/intimatewear-03-maid-inspired-roleplay-lingerie-set-premium.jpg' WHERE product_id=1003;
UPDATE oc_product SET image='catalog/adult-wellness/curated-intimates-premium/intimatewear-04-classic-maid-costume-lingerie-set-premium.jpg' WHERE product_id=1004;
UPDATE oc_product SET image='catalog/adult-wellness/curated-intimates-premium/intimatewear-05-padded-lace-strap-chemise-two-piece-set-premium.jpg' WHERE product_id=1005;
UPDATE oc_product SET image='catalog/adult-wellness/curated-intimates-premium/intimatewear-06-deep-v-lace-trim-backless-nightdress-set-premium.jpg' WHERE product_id=1006;

COMMIT;
