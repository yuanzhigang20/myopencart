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

		$description = $this->config->get('config_description');
		$language_id = $this->config->get('config_language_id');

		if (isset($description[$language_id])) {
			// Keep global store metadata available, but use a conversion-focused wellness title above.
		}

		// Homepage categories
		$this->load->model('catalog/category');
		$data['categories'] = [];
		foreach ($this->model_catalog_category->getCategories(0) as $category) {
			$data['categories'][] = [
				'name' => $category['name'],
				'href' => $this->url->link('product/category', 'language=' . $this->config->get('config_language') . '&path=' . $category['category_id'])
			];
		}

		// Homepage products
		$this->load->model('catalog/product');
		$this->load->model('tool/image');
		$data['products'] = [];
		$results = $this->model_catalog_product->getProducts([
			'sort'  => 'date_added',
			'order' => 'DESC',
			'start' => 0,
			'limit' => 12
		]);

		foreach ($results as $result) {
			$description = trim(strip_tags(html_entity_decode($result['description'], ENT_QUOTES, 'UTF-8')));
			if (oc_strlen($description) > 120) {
				$description = oc_substr($description, 0, 120) . '..';
			}

			$image = ($result['image'] && is_file(DIR_IMAGE . html_entity_decode($result['image'], ENT_QUOTES, 'UTF-8'))) ? $result['image'] : 'placeholder.png';
			$price = $this->currency->format($this->tax->calculate($result['price'], $result['tax_class_id'], $this->config->get('config_tax')), $this->session->data['currency']);

			$data['products'][] = [
				'product_id'   => $result['product_id'],
				'name'         => $result['name'],
				'description'  => $description,
				'thumb'        => $this->model_tool_image->resize($image, 480, 600),
				'price'        => $price,
				'href'         => $this->url->link('product/product', 'language=' . $this->config->get('config_language') . '&product_id=' . $result['product_id'])
			];
		}

		$this->document->addLink($this->url->link('common/home', 'language=' . $this->config->get('config_language')), 'canonical');
		$this->document->setJsonLd(json_encode([
			'@context' => 'https://schema.org',
			'@type' => 'WebSite',
			'name' => $this->config->get('config_name'),
			'url' => $this->config->get('config_ssl') ?: $this->config->get('config_url'),
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
