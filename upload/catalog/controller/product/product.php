<?php
namespace Opencart\Catalog\Controller\Product;
/**
 * Class Product
 *
 * @package Opencart\Catalog\Controller\Product
 */
class Product extends \Opencart\System\Engine\Controller {
	/**
	 * Index
	 *
	 * @return ?\Opencart\System\Engine\Action
	 */
	public function index() {
		$this->load->language('product/product');

		// Product
		if (isset($this->request->get['product_id'])) {
			$product_id = (int)$this->request->get['product_id'];
		} else {
			$product_id = 0;
		}

		$this->load->model('catalog/product');

		$product_info = $this->model_catalog_product->getProduct($product_id);

		if (!$product_info) {
			return new \Opencart\System\Engine\Action('error/not_found');
		}

		$plain_description = trim(strip_tags(html_entity_decode($product_info['description'], ENT_QUOTES, 'UTF-8')));
		$this->document->setTitle($product_info['meta_title'] ?: ($product_info['name'] . ' | Discreet Sexual Wellness | Lovanest'));
		$this->document->setDescription($product_info['meta_description'] ?: oc_substr(($plain_description ?: 'Premium private wellness product with discreet packaging, secure checkout, care guidance and 18+ responsible shopping.'), 0, 155));
		$this->document->setKeywords($product_info['meta_keyword']);
		$product_url = html_entity_decode($this->url->link('product/product', 'product_id=' . $product_id, true));
		$this->document->addLink($product_url, 'canonical');
		$this->document->addMeta(['property' => 'og:type', 'content' => 'product']);
		$this->document->addMeta(['property' => 'og:url', 'content' => $product_url]);

		$this->document->addScript('catalog/view/javascript/product.js');
		$this->document->addScript('assets/magnific/jquery.magnific-popup.min.js');
		$this->document->addStyle('assets/view/javascript/jquery/magnific/magnific-popup.css');

		$data['breadcrumbs'] = [];

		$data['breadcrumbs'][] = [
			'text' => $this->language->get('text_home'),
			'href' => $this->url->link('common/home', 'language=' . $this->config->get('config_language'))
		];

		// Category
		$this->load->model('catalog/category');

		if (isset($this->request->get['path'])) {
			$path = '';

			$parts = explode('_', (string)$this->request->get['path']);

			$category_id = (int)array_pop($parts);

			foreach ($parts as $path_id) {
				if (!$path) {
					$path = $path_id;
				} else {
					$path .= '_' . $path_id;
				}

				$category_info = $this->model_catalog_category->getCategory((int)$path_id);

				if ($category_info) {
					$data['breadcrumbs'][] = [
						'text' => $category_info['name'],
						'href' => $this->url->link('product/category', 'language=' . $this->config->get('config_language') . '&path=' . $path)
					];
				}
			}

			// Set the last category breadcrumb
			$category_info = $this->model_catalog_category->getCategory($category_id);

			if ($category_info) {
				$url = '';

				if (isset($this->request->get['sort'])) {
					$url .= '&sort=' . $this->request->get['sort'];
				}

				if (isset($this->request->get['order'])) {
					$url .= '&order=' . $this->request->get['order'];
				}

				if (isset($this->request->get['page'])) {
					$url .= '&page=' . $this->request->get['page'];
				}

				if (isset($this->request->get['limit'])) {
					$url .= '&limit=' . $this->request->get['limit'];
				}

				$data['breadcrumbs'][] = [
					'text' => $category_info['name'],
					'href' => $this->url->link('product/category', 'language=' . $this->config->get('config_language') . '&path=' . $this->request->get['path'] . $url)
				];
			}
		}

		// Manufacturer
		$this->load->model('catalog/manufacturer');

		if (isset($this->request->get['manufacturer_id'])) {
			$data['breadcrumbs'][] = [
				'text' => $this->language->get('text_brand'),
				'href' => $this->url->link('product/manufacturer', 'language=' . $this->config->get('config_language'))
			];

			$url = '';

			if (isset($this->request->get['sort'])) {
				$url .= '&sort=' . $this->request->get['sort'];
			}

			if (isset($this->request->get['order'])) {
				$url .= '&order=' . $this->request->get['order'];
			}

			if (isset($this->request->get['page'])) {
				$url .= '&page=' . $this->request->get['page'];
			}

			if (isset($this->request->get['limit'])) {
				$url .= '&limit=' . $this->request->get['limit'];
			}

			$manufacturer_info = $this->model_catalog_manufacturer->getManufacturer($this->request->get['manufacturer_id']);

			if ($manufacturer_info) {
				$data['breadcrumbs'][] = [
					'text' => $manufacturer_info['name'],
					'href' => $this->url->link('product/manufacturer.info', 'language=' . $this->config->get('config_language') . '&manufacturer_id=' . $this->request->get['manufacturer_id'] . $url)
				];
			}
		}

		if (isset($this->request->get['search']) || isset($this->request->get['tag'])) {
			$url = '';

			if (isset($this->request->get['search'])) {
				$url .= '&search=' . $this->request->get['search'];
			}

			if (isset($this->request->get['tag'])) {
				$url .= '&tag=' . $this->request->get['tag'];
			}

			if (isset($this->request->get['description'])) {
				$url .= '&description=' . $this->request->get['description'];
			}

			if (isset($this->request->get['category_id'])) {
				$url .= '&category_id=' . $this->request->get['category_id'];
			}

			if (isset($this->request->get['sub_category'])) {
				$url .= '&sub_category=' . $this->request->get['sub_category'];
			}

			if (isset($this->request->get['sort'])) {
				$url .= '&sort=' . $this->request->get['sort'];
			}

			if (isset($this->request->get['order'])) {
				$url .= '&order=' . $this->request->get['order'];
			}

			if (isset($this->request->get['page'])) {
				$url .= '&page=' . $this->request->get['page'];
			}

			if (isset($this->request->get['limit'])) {
				$url .= '&limit=' . $this->request->get['limit'];
			}

			$data['breadcrumbs'][] = [
				'text' => $this->language->get('text_search'),
				'href' => $this->url->link('product/search', 'language=' . $this->config->get('config_language') . $url)
			];
		}

		$url = '';

		if (isset($this->request->get['path'])) {
			$url .= '&path=' . $this->request->get['path'];
		}

		if (isset($this->request->get['filter'])) {
			$url .= '&filter=' . $this->request->get['filter'];
		}

		if (isset($this->request->get['manufacturer_id'])) {
			$url .= '&manufacturer_id=' . $this->request->get['manufacturer_id'];
		}

		if (isset($this->request->get['search'])) {
			$url .= '&search=' . $this->request->get['search'];
		}

		if (isset($this->request->get['tag'])) {
			$url .= '&tag=' . $this->request->get['tag'];
		}

		if (isset($this->request->get['description'])) {
			$url .= '&description=' . $this->request->get['description'];
		}

		if (isset($this->request->get['category_id'])) {
			$url .= '&category_id=' . $this->request->get['category_id'];
		}

		if (isset($this->request->get['sub_category'])) {
			$url .= '&sub_category=' . $this->request->get['sub_category'];
		}

		if (isset($this->request->get['sort'])) {
			$url .= '&sort=' . $this->request->get['sort'];
		}

		if (isset($this->request->get['order'])) {
			$url .= '&order=' . $this->request->get['order'];
		}

		if (isset($this->request->get['page'])) {
			$url .= '&page=' . $this->request->get['page'];
		}

		if (isset($this->request->get['limit'])) {
			$url .= '&limit=' . $this->request->get['limit'];
		}

		$data['breadcrumbs'][] = [
			'text' => $product_info['name'],
			'href' => $this->url->link('product/product', 'language=' . $this->config->get('config_language') . $url . '&product_id=' . $product_id)
		];

		$data['heading_title'] = $product_info['name'];

		$data['text_minimum'] = sprintf($this->language->get('text_minimum'), $product_info['minimum']);
		$data['text_login'] = sprintf($this->language->get('text_login'), $this->url->link('account/login', 'language=' . $this->config->get('config_language')), $this->url->link('account/register', 'language=' . $this->config->get('config_language')));
		$data['text_reviews'] = sprintf($this->language->get('text_reviews'), (int)$product_info['reviews']);

		$data['tab_review'] = sprintf($this->language->get('tab_review'), $product_info['reviews']);

		$data['error_upload_size'] = sprintf($this->language->get('error_upload_size'), $this->config->get('config_file_max_size'));

		$data['config_file_max_size'] = ((int)$this->config->get('config_file_max_size') * 1024 * 1024);

		$this->session->data['upload_token'] = oc_token(32);

		$data['upload'] = $this->url->link('tool/upload', 'language=' . $this->config->get('config_language') . '&upload_token=' . $this->session->data['upload_token']);

		$data['product_id'] = $product_id;

		$manufacturer_info = $this->model_catalog_manufacturer->getManufacturer($product_info['manufacturer_id']);

		if ($manufacturer_info) {
			$data['manufacturer'] = $manufacturer_info['name'];
		} else {
			$data['manufacturer'] = '';
		}

		$data['manufacturers'] = $this->url->link('product/manufacturer.info', 'language=' . $this->config->get('config_language') . '&manufacturer_id=' . $product_info['manufacturer_id']);
		$data['model'] = $product_info['model'];

		$data['product_codes'] = [];

		$results = $this->model_catalog_product->getCodes($product_id);

		foreach ($results as $result) {
			if ($result['status']) {
				$data['product_codes'][] = $result;
			}
		}

		$data['reward'] = $product_info['reward'];
		$data['points'] = $product_info['points'];
		$data['description'] = html_entity_decode($product_info['description'], ENT_QUOTES, 'UTF-8');

		// Stock Status
		if ($product_info['quantity'] <= 0) {
			$stock_status_id = $product_info['stock_status_id'];

			$data['stock'] = false;
		} elseif (!$this->config->get('config_stock_display')) {
			$stock_status_id = (int)$this->config->get('config_stock_status_id');

			$data['stock'] = true;
		} else {
			$stock_status_id = 0;

			$data['stock'] = true;
		}

		$this->load->model('localisation/stock_status');

		$stock_status_info = $this->model_localisation_stock_status->getStockStatus($stock_status_id);

		if ($stock_status_info) {
			$data['stock_status'] = $stock_status_info['name'];
		} else {
			$data['stock_status'] = $product_info['quantity'];
		}

		$data['rating'] = (int)$product_info['rating'];
		$data['review_status'] = (int)$this->config->get('config_review_status');
		$data['review'] = $this->load->controller('product/review');

		$data['wishlist_add'] = $this->url->link('account/wishlist.add', 'language=' . $this->config->get('config_language'));
		$data['compare_add'] = $this->url->link('product/compare.add', 'language=' . $this->config->get('config_language'));
		$data['cart_add'] = $this->url->link('checkout/cart.add', 'language=' . $this->config->get('config_language'));
		$data['checkout'] = $this->url->link('checkout/checkout', 'language=' . $this->config->get('config_language'));

		// Image
		$this->load->model('tool/image');

		if ($product_info['image'] && is_file(DIR_IMAGE . html_entity_decode($product_info['image'], ENT_QUOTES, 'UTF-8'))) {
			$data['popup'] = HTTP_SERVER . 'image/' . $product_info['image'];
			$data['thumb'] = $this->model_tool_image->resize($product_info['image'], $this->config->get('config_image_thumb_width'), $this->config->get('config_image_thumb_height'));
			$this->document->addMeta(['property' => 'og:image', 'content' => $data['popup']]);
			$this->document->addMeta(['name' => 'twitter:image', 'content' => $data['popup']]);
		} else {
			$data['popup'] = '';
			$data['thumb'] = '';
		}

		$data['images'] = [];

		$results = $this->model_catalog_product->getImages($product_id);

		foreach ($results as $result) {
			if ($result['image'] && is_file(DIR_IMAGE . html_entity_decode($result['image'], ENT_QUOTES, 'UTF-8'))) {
				$data['images'][] = [
					'popup' => HTTP_SERVER . 'image/' . $result['image'],
					'thumb' => $this->model_tool_image->resize($result['image'], $this->config->get('config_image_thumb_width'), $this->config->get('config_image_thumb_height'))
				];
			}
		}

		if ($this->customer->isLogged() || !$this->config->get('config_customer_price')) {
			$data['price'] = $this->tax->calculate($product_info['price'], $product_info['tax_class_id'], $this->config->get('config_tax'));
		} else {
			$data['price'] = false;
		}

		if ((float)$product_info['special']) {
			$data['special'] = $this->tax->calculate($product_info['special'], $product_info['tax_class_id'], $this->config->get('config_tax'));
		} else {
			$data['special'] = false;
		}

		if ($this->config->get('config_tax')) {
			$data['tax'] = (float)$product_info['special'] ? $product_info['special'] : $product_info['price'];
		} else {
			$data['tax'] = false;
		}

		$discounts = $this->model_catalog_product->getDiscounts($product_id);

		$data['discounts'] = [];

		if ($this->customer->isLogged() || !$this->config->get('config_customer_price')) {
			foreach ($discounts as $discount) {
				$data['discounts'][] = ['price' => $this->tax->calculate($discount['price'], $product_info['tax_class_id'], $this->config->get('config_tax'))] + $discount;
			}
		}

		$data['options'] = [];

		// Check if product is variant
		if ($product_info['master_id']) {
			$master_id = (int)$product_info['master_id'];
		} else {
			$master_id = (int)$product_id;
		}

		$product_options = $this->model_catalog_product->getOptions($master_id);

		foreach ($product_options as $option) {
			if ($product_id && !isset($product_info['override']['variant'][$option['product_option_id']])) {
				$product_option_value_data = [];

				foreach ($option['product_option_value'] as $option_value) {
					if (!$option_value['subtract'] || ($option_value['quantity'] > 0)) {
						if ((($this->config->get('config_customer_price') && $this->customer->isLogged()) || !$this->config->get('config_customer_price')) && (float)$option_value['price']) {
							$price = $this->tax->calculate($option_value['price'], $product_info['tax_class_id'], $this->config->get('config_tax'));
						} else {
							$price = false;
						}

						if ($option_value['image'] && is_file(DIR_IMAGE . html_entity_decode($option_value['image'], ENT_QUOTES, 'UTF-8'))) {
							$image = $option_value['image'];
						} else {
							$image = '';
						}

						$product_option_value_data[] = [
							'image' => $this->model_tool_image->resize($image, 72, 72),
							'variant_main' => $image ? $this->model_tool_image->resize($image, $this->config->get('config_image_thumb_width'), $this->config->get('config_image_thumb_height')) : '',
							'variant_popup' => $image ? HTTP_SERVER . 'image/' . $image : '',
							'price' => $price
					] + $option_value;
					}
				}

				$data['options'][] = ['product_option_value' => $product_option_value_data] + $option;
			}
		}

		// Subscription Plans
		$data['subscription_plans'] = [];

		$results = $this->model_catalog_product->getSubscriptions($product_id);

		foreach ($results as $result) {
			$description = '';

			if ($this->customer->isLogged() || !$this->config->get('config_customer_price')) {
				if ($result['duration']) {
					$price = ($product_info['special'] ?: $product_info['price']) / $result['duration'];
				} else {
					$price = ($product_info['special'] ?: $product_info['price']);
				}

				$price = $this->tax->calculate($price, $product_info['tax_class_id'], $this->config->get('config_tax'));
				$cycle = $result['cycle'];
				$frequency = $this->language->get('text_' . $result['frequency']);
				$duration = $result['duration'];

				if ($duration) {
					$description = sprintf($this->language->get('text_subscription_duration'), $price, $cycle, $frequency, $duration);
				} else {
					$description = sprintf($this->language->get('text_subscription_cancel'), $price, $cycle, $frequency);
				}
			}

			$data['subscription_plans'][] = ['description' => $description] + $result;
		}

		if ($product_info['minimum']) {
			$data['minimum'] = $product_info['minimum'];
		} else {
			$data['minimum'] = 1;
		}

		$data['share'] = $product_url;

		$schema = [
			'@context' => 'https://schema.org',
			'@type' => 'Product',
			'name' => $product_info['name'],
			'description' => trim(strip_tags(html_entity_decode($product_info['description'], ENT_QUOTES, 'UTF-8'))) ?: $product_info['meta_description'],
			'sku' => $product_info['model'],
			'mpn' => $product_info['model'],
			'url' => html_entity_decode($data['share']),
			'offers' => [
				'@type' => 'Offer',
				'url' => html_entity_decode($data['share']),
				'priceCurrency' => $this->session->data['currency'],
				'price' => number_format((float)($product_info['special'] ?: $product_info['price']), 2, '.', ''),
				'availability' => $product_info['quantity'] > 0 ? 'https://schema.org/InStock' : 'https://schema.org/OutOfStock',
				'itemCondition' => 'https://schema.org/NewCondition'
			]
		];

		if ($data['thumb']) {
			$schema['image'] = [$data['thumb']];
		}

		if ($product_info['reviews'] && $product_info['rating']) {
			$schema['aggregateRating'] = [
				'@type' => 'AggregateRating',
				'ratingValue' => (float)$product_info['rating'],
				'reviewCount' => (int)$product_info['reviews']
			];

			$this->load->model('catalog/review');

			$review_results = $this->model_catalog_review->getReviewsByProductId($product_id, 0, 3);

			foreach ($review_results as $review_result) {
				$schema['review'][] = [
					'@type' => 'Review',
					'author' => [
						'@type' => 'Person',
						'name' => $review_result['author']
					],
					'datePublished' => date('Y-m-d', strtotime($review_result['date_added'])),
					'reviewBody' => trim(strip_tags(html_entity_decode($review_result['text'], ENT_QUOTES, 'UTF-8'))),
					'reviewRating' => [
						'@type' => 'Rating',
						'ratingValue' => (int)$review_result['rating'],
						'bestRating' => 5,
						'worstRating' => 1
					]
				];
			}
		}

		$faq_schema = [
			'@type' => 'FAQPage',
			'mainEntity' => [
				[
					'@type' => 'Question',
					'name' => 'Will the package be discreet?',
					'acceptedAnswer' => ['@type' => 'Answer', 'text' => 'The store is designed around discreet packaging and private delivery expectations, without explicit wording on the public-facing parcel.']
				],
				[
					'@type' => 'Question',
					'name' => 'How do I choose the right product?',
					'acceptedAnswer' => ['@type' => 'Answer', 'text' => 'Use scenario categories such as Beginner Friendly, For Couples, Solo Wellness, Quiet & Discreet, Waterproof, and Lubricants & Care.']
				],
				[
					'@type' => 'Question',
					'name' => 'How should intimate products be cleaned?',
					'acceptedAnswer' => ['@type' => 'Answer', 'text' => 'Follow the product-specific material and care instructions. Clean before and after use, dry fully, and store in a clean private place.']
				]
			]
		];

		$this->document->setJsonLd(json_encode([
			'@context' => 'https://schema.org',
			'@graph' => [$schema, $faq_schema]
		], JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE));

		// Attribute Groups
		$data['attribute_groups'] = $this->model_catalog_product->getAttributes($product_id);

		// Related
		$data['related'] = $this->load->controller('product/related');

		// Tag
		$data['tags'] = [];

		if ($product_info['tag']) {
			$tags = explode(',', $product_info['tag']);

			foreach ($tags as $tag) {
				$data['tags'][] = [
					'tag'  => trim($tag),
					'href' => $this->url->link('product/search', 'language=' . $this->config->get('config_language') . '&tag=' . trim($tag))
				];
			}
		}

		if ($this->config->get('config_product_report_status')) {
			$this->model_catalog_product->addReport($product_id, oc_get_ip());
		}

		$data['language'] = $this->config->get('config_language');
		$data['currency'] = $this->session->data['currency'];

		$data['column_left'] = $this->load->controller('common/column_left');
		$data['column_right'] = $this->load->controller('common/column_right');
		$data['content_top'] = $this->load->controller('common/content_top');
		$data['content_bottom'] = $this->load->controller('common/content_bottom');
		$data['footer'] = $this->load->controller('common/footer');
		$data['header'] = $this->load->controller('common/header');

		$this->response->setOutput($this->load->view('product/product', $data));

		return null;
	}
}
