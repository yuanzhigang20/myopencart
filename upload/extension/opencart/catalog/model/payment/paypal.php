<?php
namespace Opencart\Catalog\Model\Extension\Opencart\Payment;

class Paypal extends \Opencart\System\Engine\Model {
	public function getMethods(array $address = []): array {
		$this->load->language('extension/opencart/payment/paypal');

		if (!$this->config->get('payment_paypal_status')) {
			$status = false;
		} elseif ($this->cart->hasSubscription()) {
			$status = false;
		} elseif ($this->cart->hasShipping() && $this->config->get('config_checkout_payment_address') && $this->config->get('payment_paypal_geo_zone_id')) {
			$this->load->model('localisation/geo_zone');

			$results = $this->model_localisation_geo_zone->getGeoZone((int)$this->config->get('payment_paypal_geo_zone_id'), (int)($address['country_id'] ?? 0), (int)($address['zone_id'] ?? 0));

			$status = (bool)$results;
		} else {
			$status = true;
		}

		$method_data = [];

		if ($status) {
			$option_data['paypal'] = [
				'code' => 'paypal.paypal',
				'name' => $this->language->get('heading_title')
			];

			$method_data = [
				'code'       => 'paypal',
				'name'       => $this->language->get('heading_title'),
				'option'     => $option_data,
				'sort_order' => $this->config->get('payment_paypal_sort_order')
			];
		}

		return $method_data;
	}
}
