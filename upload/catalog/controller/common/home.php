<?php
namespace Opencart\Catalog\Controller\Common;
/**
 * Class Home
 *
 * Can be called from $this->load->controller('common/home');
 *
 * @package Opencart\Catalog\Controller\Common
 */
class Home extends \Opencart\System\Engine\Controller {
	/**
	 * Index
	 *
	 * @return void
	 */
	public function index(): void {
		$this->document->setTitle('Private Wellness Delivered Discreetly | Lovanest Adult Wellness');
		$this->document->setDescription('Shop curated adult wellness essentials with plain packaging, secure checkout, private billing language, and 18+ responsible retail from Lovanest.');
		$this->document->setKeywords('adult wellness, private wellness, discreet packaging, secure checkout, beginner friendly wellness products');

		$this->load->language('product/category');

		$limit = 24;

		// Homepage categories: expose real catalog categories and child categories.
		$this->load->model('catalog/category');
		$data['categories'] = [];
		$data['category_groups'] = [];

		foreach ($this->model_catalog_category->getCategories(0) as $category) {
			$children = [];

			foreach ($this->model_catalog_category->getCategories((int)$category['category_id']) as $child) {
				$children[] = [
					'name' => $child['name'],
					'href' => $this->url->link('product/category', 'language=' . $this->config->get('config_language') . '&path=' . $category['category_id'] . '_' . $child['category_id'])
				];
			}

			$category_data = [
				'name' => $category['name'],
				'href' => $this->url->link('product/category', 'language=' . $this->config->get('config_language') . '&path=' . $category['category_id']),
				'children' => $children
			];

			$data['categories'][] = $category_data;
			$data['category_groups'][] = $category_data;
		}

		// Homepage products: curated, homepage-safe products only. Avoid default full catalog pagination on the landing page.
		$this->load->model('catalog/product');
		$this->load->model('tool/image');

		$data['cart_add'] = $this->url->link('checkout/cart.add', 'language=' . $this->config->get('config_language'));
		$data['cart'] = $this->url->link('common/cart.info', 'language=' . $this->config->get('config_language'));
		$data['products'] = [];
		$data['best_sellers'] = [];
		$data['new_arrivals'] = [];
		$data['hero_products'] = [];
		$data['image_review_needed'] = [];

		$results = $this->model_catalog_product->getProducts([
			'sort'  => 'p.sort_order',
			'order' => 'ASC',
			'start' => 0,
			'limit' => $limit
		]);

		$presentation_products = [
			['name' => 'G-Spot Vibrator for Women', 'image' => 'catalog/adult-wellness/adult-seahorse-008.png', 'benefit' => 'Quiet curved design for private, confident discovery.'],
			['name' => 'Suction Clitoral Stimulator', 'image' => 'catalog/adult-wellness/adult-rabbit-004.png', 'benefit' => 'Soft-touch wellness pick with simple controls.'],
			['name' => 'Wearable Remote Vibrator', 'image' => 'catalog/adult-wellness/adult-bullet-001.png', 'benefit' => 'Low-profile option for discreet everyday storage.'],
			['name' => 'Kegel Exercise Balls Set', 'image' => 'catalog/adult-wellness/adult-care-kit-002.png', 'benefit' => 'Beginner-friendly care set with clean presentation.'],
			['name' => 'Mini Wand Massager', 'image' => 'catalog/adult-wellness/adult-wand-007.png', 'benefit' => 'Compact wand for approachable private wellness.'],
			['name' => 'Air Pulse Clitoral Stimulator', 'image' => 'catalog/adult-wellness/adult-rabbit-004.png', 'benefit' => 'Comfort-focused design selected for gentle exploration.'],
			['name' => 'Couples Vibrator with App Control', 'image' => 'catalog/adult-wellness/adult-bullet-001.png', 'benefit' => 'Connected intimacy essential for shared moments.'],
			['name' => 'Silicone Butt Plug Beginner Set', 'image' => 'catalog/adult-wellness/adult-male-006.png', 'benefit' => 'Smooth beginner set with privacy-first delivery.']
		];

		$banned_terms = ['1688', 'taobao', 'pinduoduo', '拼多多', '阿里', '淘宝', '中文', '水印', 'watermark', 'рус', 'russian', 'demo', 'test'];

		foreach ($results as $index => $result) {
			if ((float)$result['price'] < 1) {
				continue;
			}

			$description = trim(strip_tags(html_entity_decode($result['description'], ENT_QUOTES, 'UTF-8')));
			$review_text = oc_strtolower($result['name'] . ' ' . $description . ' ' . (string)$result['image']);
			$needs_review = false;

			foreach ($banned_terms as $term) {
				if (str_contains($review_text, oc_strtolower($term))) {
					$needs_review = true;
					break;
				}
			}

			if ($needs_review) {
				$data['image_review_needed'][] = $result['name'];
				continue;
			}

			if (oc_strlen($description) > 112) {
				$description = oc_substr($description, 0, 112) . '..';
			}

			$presentation = $presentation_products[count($data['products']) % count($presentation_products)];
			$image = is_file(DIR_IMAGE . $presentation['image']) ? $presentation['image'] : (($result['image'] && is_file(DIR_IMAGE . html_entity_decode($result['image'], ENT_QUOTES, 'UTF-8'))) ? $result['image'] : 'placeholder.png');
			$price = $this->currency->format($this->tax->calculate($result['price'], $result['tax_class_id'], $this->config->get('config_tax')), $this->session->data['currency']);

			$product = [
				'product_id'    => $result['product_id'],
				'name'          => $presentation['name'],
				'description'   => $description,
				'short_benefit' => $presentation['benefit'],
				'thumb'         => $this->model_tool_image->resize($image, 480, 600),
				'price'         => $price,
				'href'          => $this->url->link('product/product', 'language=' . $this->config->get('config_language') . '&product_id=' . $result['product_id'])
			];

			$data['products'][] = $product;
		}

		$data['best_sellers'] = array_slice($data['products'], 0, 4);
		$data['new_arrivals'] = array_slice($data['products'], 4, 4) ?: array_slice($data['products'], 0, 4);
		$data['hero_products'] = array_slice($data['best_sellers'], 0, 2);
		$data['all_products_url'] = $this->url->link('product/search', 'language=' . $this->config->get('config_language') . '&search=wellness');

		$site_url = rtrim($this->config->get('config_ssl') ?: $this->config->get('config_url'), '/') . '/';
		$this->document->addLink($site_url, 'canonical');
		$this->document->addMeta(['property' => 'og:url', 'content' => $site_url]);
		$this->document->addMeta(['property' => 'og:type', 'content' => 'website']);
		$this->document->setJsonLd(json_encode([
			'@context' => 'https://schema.org',
			'@type' => 'WebSite',
			'name' => $this->config->get('config_name'),
			'url' => $site_url,
			'potentialAction' => [
				'@type' => 'SearchAction',
				'target' => ($this->config->get('config_ssl') ?: $this->config->get('config_url')) . 'index.php?route=product/search&language=' . $this->config->get('config_language') . '&search={search_term_string}',
				'query-input' => 'required name=search_term_string'
			]
		], JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE));

		$data['footer'] = $this->load->controller('common/footer');
		$data['header'] = $this->load->controller('common/header');

		$this->response->setOutput($this->load->view('common/home', $data));
	}
}
