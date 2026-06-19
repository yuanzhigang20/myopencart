<?php
// Adds 1688 offer 693405335527 as an English OpenCart product without storing external credentials.
// Run from OpenCart upload root: php database/2026-06-19-add-fb089-beauty-brush-massager.php
require 'config.php';
$mysqli = new mysqli(DB_HOSTNAME, DB_USERNAME, DB_PASSWORD, DB_DATABASE, (int)DB_PORT);
if ($mysqli->connect_errno) { fwrite(STDERR, "DB connect failed\n"); exit(1); }
$mysqli->set_charset('utf8mb4');
$prefix = DB_PREFIX;
$lang = 1;
$store = 0;
function q($s) { global $mysqli; return $mysqli->real_escape_string($s); }
function one($sql) { global $mysqli; $r=$mysqli->query($sql); if(!$r) throw new Exception($mysqli->error."\nSQL: ".$sql); $row=$r->fetch_row(); return $row ? $row[0] : null; }
function execq($sql) { global $mysqli; if(!$mysqli->query($sql)) throw new Exception($mysqli->error."\nSQL: ".$sql); return $mysqli->insert_id; }
function ensure_category($name, $parent_id, $meta_title, $meta_description, $description, $keyword) {
  global $prefix,$lang,$store,$mysqli;
  $id = one("SELECT c.category_id FROM `{$prefix}category` c JOIN `{$prefix}category_description` cd ON c.category_id=cd.category_id WHERE cd.language_id=$lang AND cd.name='".q($name)."' LIMIT 1");
  if (!$id) {
    execq("INSERT INTO `{$prefix}category` SET image='', parent_id=".(int)$parent_id.", sort_order=20, status=1");
    $id = $mysqli->insert_id;
    execq("INSERT INTO `{$prefix}category_description` SET category_id=$id, language_id=$lang, name='".q($name)."', description='".q($description)."', meta_title='".q($meta_title)."', meta_description='".q($meta_description)."', meta_keyword='' ");
    execq("INSERT IGNORE INTO `{$prefix}category_to_store` SET category_id=$id, store_id=$store");
    if ($parent_id) {
      $rows=$mysqli->query("SELECT path_id, level FROM `{$prefix}category_path` WHERE category_id=".(int)$parent_id." ORDER BY level");
      while($row=$rows->fetch_assoc()) execq("INSERT INTO `{$prefix}category_path` SET category_id=$id, path_id=".(int)$row['path_id'].", level=".(int)$row['level']);
      $level = (int)one("SELECT MAX(level)+1 FROM `{$prefix}category_path` WHERE category_id=$id");
    } else { $level=0; }
    execq("INSERT INTO `{$prefix}category_path` SET category_id=$id, path_id=$id, level=$level");
  }
  $seo = one("SELECT seo_url_id FROM `{$prefix}seo_url` WHERE `key`='path' AND value='".q((string)$id)."' AND language_id=$lang AND store_id=$store LIMIT 1");
  if (!$seo) execq("INSERT INTO `{$prefix}seo_url` SET store_id=$store, language_id=$lang, `key`='path', value='".q((string)$id)."', keyword='".q($keyword)."', sort_order=0");
  return (int)$id;
}
$root = ensure_category('Adult Wellness', 0, 'Adult Wellness Essentials | Lovanest', 'Private, discreet adult wellness essentials for 18+ shoppers.', '<p>Private adult wellness essentials with discreet packaging and secure checkout.</p>', 'adult-wellness');
$cat = ensure_category('Vibrating Massagers', $root, 'Discreet Vibrating Massagers | Lovanest', 'Body-safe, discreet vibrating massagers for adult wellness shoppers.', '<p>Discreet vibrating massagers selected for private adult wellness shopping, plain packaging, and responsible 18+ use.</p>', 'vibrating-massagers');
$sku = 'LW-FB089';
$product_id = one("SELECT product_id FROM `{$prefix}product` WHERE model='".q($sku)."' LIMIT 1");
$name = 'Discreet Beauty Brush Vibrating Massager';
$slug = 'discreet-beauty-brush-vibrating-massager-fb089';
$image = 'catalog/adult-wellness/beauty-brush-vibrating-massager/beauty-brush-vibrating-massager-01.jpg';
$price = '39.99';
$quantity = 500;
$description = <<<HTML
<section class="product-wellness-copy"><h2>Discreet Beauty Brush Vibrating Massager</h2><p>A private adult wellness massager designed with a subtle beauty-brush inspired look, quiet operation, and a clean travel-friendly profile. Built for 18+ responsible personal wellness shopping.</p><h3>Key Benefits</h3><ul><li>Discreet beauty-brush inspired design for private storage and travel.</li><li>ABS body with smooth finish for easy cleaning.</li><li>Low-noise operation under 50 dB for a calmer experience.</li><li>Multiple color/variant options suitable for private gifting or personal wellness routines.</li><li>Ships in plain packaging with no adult product names on the outside.</li></ul><h3>Specifications</h3><ul><li><strong>Material:</strong> ABS</li><li><strong>Model:</strong> FB089</li><li><strong>Noise Level:</strong> Under 50 dB</li><li><strong>Weight:</strong> Approx. 300 g</li><li><strong>Available Variants:</strong> Green, Black Cat Paw, Rose Gold, Black, First Generation Black</li><li><strong>Lubricant Included:</strong> No</li><li><strong>Recommended Age:</strong> Adults 18+ only</li></ul><h3>Care & Privacy</h3><p>Clean before and after use according to the included product care instructions. Store in a dry place. This product is sold for adults only and ships with discreet packaging.</p></section>
HTML;
if (!$product_id) {
  execq("INSERT INTO `{$prefix}product` SET master_id=0, model='".q($sku)."', location='', variant='', override='', quantity=$quantity, stock_status_id=7, image='".q($image)."', manufacturer_id=0, shipping=1, price=$price, points=0, tax_class_id=0, date_available=CURDATE(), weight='0.30000000', weight_class_id=2, length='0.00000000', width='0.00000000', height='0.00000000', length_class_id=1, subtract=0, minimum=1, sort_order=10, status=1");
  $product_id = $mysqli->insert_id;
} else {
  execq("UPDATE `{$prefix}product` SET quantity=$quantity, stock_status_id=7, image='".q($image)."', shipping=1, price=$price, weight='0.30000000', weight_class_id=2, subtract=0, minimum=1, status=1 WHERE product_id=".(int)$product_id);
  $mysqli->query("DELETE FROM `{$prefix}product_description` WHERE product_id=".(int)$product_id." AND language_id=$lang");
  $mysqli->query("DELETE FROM `{$prefix}product_to_category` WHERE product_id=".(int)$product_id);
  $mysqli->query("DELETE FROM `{$prefix}product_to_store` WHERE product_id=".(int)$product_id);
  $mysqli->query("DELETE FROM `{$prefix}product_image` WHERE product_id=".(int)$product_id);
}
execq("INSERT INTO `{$prefix}product_description` SET product_id=$product_id, language_id=$lang, name='".q($name)."', description='".q($description)."', tag='adult wellness, discreet massager, beauty brush massager, vibrating massager', meta_title='Discreet Beauty Brush Vibrating Massager | Lovanest', meta_description='Shop a discreet beauty-brush inspired vibrating massager for adults 18+. ABS body, low-noise operation, private packaging, and secure PayPal checkout.', meta_keyword='' ");
execq("INSERT IGNORE INTO `{$prefix}product_to_store` SET product_id=$product_id, store_id=$store");
execq("INSERT IGNORE INTO `{$prefix}product_to_category` SET product_id=$product_id, category_id=$cat");
$imgs = ['02','03','04','05','06','07','08','09','10'];
$i=0; foreach($imgs as $n) execq("INSERT INTO `{$prefix}product_image` SET product_id=$product_id, image='catalog/adult-wellness/beauty-brush-vibrating-massager/beauty-brush-vibrating-massager-$n.jpg', sort_order=".(++$i));
$group = one("SELECT attribute_group_id FROM `{$prefix}attribute_group_description` WHERE language_id=$lang AND name='Wellness Details' LIMIT 1");
if (!$group) { execq("INSERT INTO `{$prefix}attribute_group` SET sort_order=1"); $group=$mysqli->insert_id; execq("INSERT INTO `{$prefix}attribute_group_description` SET attribute_group_id=$group, language_id=$lang, name='Wellness Details'"); }
$attrs = ['Material'=>'ABS body with smooth finish','Size & Fit'=>'See product images for detailed sizing; compact handheld profile','Power / Charging'=>'USB rechargeable and battery-style variants may be available depending on selected option','Noise Level'=>'Low noise, under 50 dB','Package Includes'=>'1 discreet beauty-brush style vibrating massager','Best For'=>'Private adult wellness, discreet gifting, travel-friendly storage','Cleaning'=>'Clean before and after use; store dry; follow included care instructions','Discreet Shipping'=>'Ships in plain packaging with no adult product names outside','Available Variants'=>'Green, Black Cat Paw, Rose Gold, Black, First Generation Black'];
$mysqli->query("DELETE FROM `{$prefix}product_attribute` WHERE product_id=$product_id");
foreach($attrs as $an=>$av){$aid = one("SELECT a.attribute_id FROM `{$prefix}attribute` a JOIN `{$prefix}attribute_description` ad ON a.attribute_id=ad.attribute_id WHERE ad.language_id=$lang AND ad.name='".q($an)."' LIMIT 1"); if(!$aid){ execq("INSERT INTO `{$prefix}attribute` SET attribute_group_id=$group, sort_order=1"); $aid=$mysqli->insert_id; execq("INSERT INTO `{$prefix}attribute_description` SET attribute_id=$aid, language_id=$lang, name='".q($an)."'"); } execq("INSERT INTO `{$prefix}product_attribute` SET product_id=$product_id, attribute_id=$aid, language_id=$lang, text='".q($av)."'");}
$seo = one("SELECT seo_url_id FROM `{$prefix}seo_url` WHERE `key`='product_id' AND value='".q((string)$product_id)."' AND language_id=$lang AND store_id=$store LIMIT 1");
if(!$seo) execq("INSERT INTO `{$prefix}seo_url` SET store_id=$store, language_id=$lang, `key`='product_id', value='".q((string)$product_id)."', keyword='".q($slug)."', sort_order=0"); else execq("UPDATE `{$prefix}seo_url` SET keyword='".q($slug)."' WHERE seo_url_id=$seo");
echo "product_id=$product_id\ncategory_id=$cat\n";
