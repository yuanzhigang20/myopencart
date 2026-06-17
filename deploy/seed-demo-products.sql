-- Demo product/category seed for myopencart testing. Run against the OpenCart database after install.
-- This does not create new IDs; it updates the default OpenCart demo rows into clearer testing data.

UPDATE oc_setting SET value='MyOpenCart Demo Store' WHERE `key`='config_name' AND store_id=0;
UPDATE oc_setting SET value='Demo OpenCart independent store for checkout testing' WHERE `key`='config_meta_description' AND store_id=0;

UPDATE oc_category_description
SET name='Demo Electronics', description='Demo electronics category for storefront testing', meta_title='Demo Electronics'
WHERE category_id=20 AND language_id=1;
UPDATE oc_category SET status=1 WHERE category_id=20;

UPDATE oc_product_description
SET name='Wireless Bluetooth Headphones',
    description='<p>Demo product: wireless over-ear headphones with noise reduction, long battery life, and soft ear cushions. Use this item to test product detail pages, cart, and checkout.</p>',
    meta_title='Wireless Bluetooth Headphones'
WHERE product_id=28 AND language_id=1;
UPDATE oc_product SET model='DEMO-HEADPHONE-001', price=59.9900, quantity=120, status=1, date_available=CURDATE() WHERE product_id=28;

UPDATE oc_product_description
SET name='Smart Fitness Watch',
    description='<p>Demo product: smart watch with heart-rate monitoring, step tracking, waterproof body, and phone notifications.</p>',
    meta_title='Smart Fitness Watch'
WHERE product_id=29 AND language_id=1;
UPDATE oc_product SET model='DEMO-WATCH-002', price=89.9900, quantity=85, status=1, date_available=CURDATE() WHERE product_id=29;

UPDATE oc_product_description
SET name='Portable USB-C Power Bank',
    description='<p>Demo product: compact 20000mAh power bank with USB-C fast charging. Good for mobile accessory test scenarios.</p>',
    meta_title='Portable USB-C Power Bank'
WHERE product_id=30 AND language_id=1;
UPDATE oc_product SET model='DEMO-POWER-003', price=39.9900, quantity=200, status=1, date_available=CURDATE() WHERE product_id=30;

UPDATE oc_product_description
SET name='Mechanical Gaming Keyboard',
    description='<p>Demo product: RGB mechanical keyboard with tactile switches and durable metal frame.</p>',
    meta_title='Mechanical Gaming Keyboard'
WHERE product_id=31 AND language_id=1;
UPDATE oc_product SET model='DEMO-KEYBOARD-004', price=74.9900, quantity=60, status=1, date_available=CURDATE() WHERE product_id=31;

UPDATE oc_product_description
SET name='4K Action Camera',
    description='<p>Demo product: compact 4K action camera for travel and sports videos, with waterproof case and wide-angle lens.</p>',
    meta_title='4K Action Camera'
WHERE product_id=32 AND language_id=1;
UPDATE oc_product SET model='DEMO-CAMERA-005', price=129.9900, quantity=45, status=1, date_available=CURDATE() WHERE product_id=32;

UPDATE oc_product_description
SET name='Ergonomic Office Chair',
    description='<p>Demo product: adjustable ergonomic chair with lumbar support, breathable mesh, and smooth wheels.</p>',
    meta_title='Ergonomic Office Chair'
WHERE product_id=33 AND language_id=1;
UPDATE oc_product SET model='DEMO-CHAIR-006', price=149.9900, quantity=30, status=1, date_available=CURDATE() WHERE product_id=33;

DELETE FROM oc_product_to_category WHERE product_id IN (28,29,30,31,32,33) AND category_id=20;
INSERT INTO oc_product_to_category (product_id, category_id) VALUES (28,20),(29,20),(30,20),(31,20),(32,20),(33,20);
