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
		$this->document->setTitle('Discreet Intimacy Essentials | Lovanest Sexual Wellness');
		$this->document->setDescription('Shop premium private wellness and intimacy essentials with discreet packaging, secure checkout, body-safe product details and 18+ responsible retail.');
		$this->document->setKeywords('sexual wellness, intimacy products, discreet packaging, private wellness, adult wellness');

		$this->load->language('product/category');

		$description = $this->config->get('config_description');
		$language_id = $this->config->get('config_language_id');

		if (isset($description[$language_id])) {
			// Keep global store metadata available, but use a conversion-focused wellness title above.
		}

		if (isset($this->request->get['page'])) {
			$page = max(1, (int)$this->request->get['page']);
		} else {
			$page = 1;
		}

		$limit = 12;

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

		// Homepage products: show the full enabled catalog with pagination.
		$this->load->model('catalog/product');
		$this->load->model('tool/image');

		$data['cart_add'] = $this->url->link('checkout/cart.add', 'language=' . $this->config->get('config_language'));
		$data['cart'] = $this->url->link('common/cart.info', 'language=' . $this->config->get('config_language'));
		$data['products'] = [];
		$data['best_sellers'] = [];
		$data['new_arrivals'] = [];
		$data['hero_products'] = [];

		$product_total = $this->model_catalog_product->getTotalProducts([]);

		$results = $this->model_catalog_product->getProducts([
			'sort'  => 'p.sort_order',
			'order' => 'ASC',
			'start' => ($page - 1) * $limit,
			'limit' => $limit
		]);

		$benefits = [
			'Private wellness essential with discreet packaging and clean presentation.',
			'Soft, approachable pick for comfort-focused intimate shopping.',
			'Low-profile design selected for private, responsible adult retail.',
			'Curated for a calm checkout experience and secure PayPal payment.'
		];

		foreach ($results as $index => $result) {
			$description = trim(strip_tags(html_entity_decode($result['description'], ENT_QUOTES, 'UTF-8')));
			if (oc_strlen($description) > 118) {
				$description = oc_substr($description, 0, 118) . '..';
			}

			$image = ($result['image'] && is_file(DIR_IMAGE . html_entity_decode($result['image'], ENT_QUOTES, 'UTF-8'))) ? $result['image'] : 'placeholder.png';
			$price = $this->currency->format($this->tax->calculate($result['price'], $result['tax_class_id'], $this->config->get('config_tax')), $this->session->data['currency']);

			$product = [
				'product_id'    => $result['product_id'],
				'name'          => $result['name'],
				'description'   => $description,
				'short_benefit' => $benefits[$index % count($benefits)],
				'thumb'         => $this->model_tool_image->resize($image, 480, 600),
				'price'         => $price,
				'href'          => $this->url->link('product/product', 'language=' . $this->config->get('config_language') . '&product_id=' . $result['product_id'])
			];

			$data['products'][] = $product;
		}

		$data['best_sellers'] = array_slice($data['products'], 0, 4);
		$data['new_arrivals'] = array_slice($data['products'], 4, 4) ?: array_slice($data['products'], 0, 4);
		$data['hero_products'] = array_slice($data['best_sellers'], 0, 2);

		$data['pagination'] = $this->load->controller('common/pagination', [
			'total' => $product_total,
			'page'  => $page,
			'limit' => $limit,
			'url'   => $this->url->link('common/home', 'language=' . $this->config->get('config_language') . '&page={page}')
		]);

		$data['results'] = sprintf($this->language->get('text_pagination'), ($product_total) ? (($page - 1) * $limit) + 1 : 0, ((($page - 1) * $limit) > ($product_total - $limit)) ? $product_total : ((($page - 1) * $limit) + $limit), $product_total, ceil($product_total / $limit));
		$data['all_products_url'] = $this->url->link('common/home', 'language=' . $this->config->get('config_language'));

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
