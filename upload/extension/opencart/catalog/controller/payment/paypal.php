<?php
namespace Opencart\Catalog\Controller\Extension\Opencart\Payment;

class Paypal extends \Opencart\System\Engine\Controller {
	public function index(): string {
		$this->load->language('extension/opencart/payment/paypal');

		$client_id = (string)$this->config->get('payment_paypal_client_id');
		$intent = strtolower((string)($this->config->get('payment_paypal_intent') ?: 'CAPTURE'));

		$data['language'] = $this->config->get('config_language');
		$data['client_id'] = $client_id;
		$data['currency'] = $this->session->data['currency'] ?? $this->config->get('config_currency');
		$data['intent'] = $intent === 'authorize' ? 'authorize' : 'capture';
		$data['error_credentials'] = $this->language->get('error_credentials');
		$data['create_url'] = html_entity_decode($this->url->link('extension/opencart/payment/paypal.create', 'language=' . $this->config->get('config_language'), true));
		$data['capture_url'] = html_entity_decode($this->url->link('extension/opencart/payment/paypal.capture', 'language=' . $this->config->get('config_language'), true));

		return $this->load->view('extension/opencart/payment/paypal', $data);
	}

	public function create(): void {
		$this->load->language('extension/opencart/payment/paypal');
		$json = [];

		$order_info = $this->validateOrder();

		if (!$order_info) {
			$json['error'] = $this->language->get('error_order');
		} elseif (!$this->hasCredentials()) {
			$json['error'] = $this->language->get('error_credentials');
		} else {
			$intent = strtoupper((string)($this->config->get('payment_paypal_intent') ?: 'CAPTURE'));
			$currency = $order_info['currency_code'] ?: ($this->session->data['currency'] ?? $this->config->get('config_currency'));
			$value = $this->currency->format((float)$order_info['total'], $currency, (float)$order_info['currency_value'], false);

			$payload = [
				'intent' => $intent === 'AUTHORIZE' ? 'AUTHORIZE' : 'CAPTURE',
				'purchase_units' => [[
					'reference_id' => (string)$order_info['order_id'],
					'invoice_id' => (string)$order_info['order_id'],
					'amount' => [
						'currency_code' => $currency,
						'value' => number_format((float)$value, 2, '.', '')
					]
				]],
				'application_context' => [
					'brand_name' => $this->config->get('config_name'),
					'shipping_preference' => 'NO_SHIPPING',
					'user_action' => 'PAY_NOW'
				]
			];

			$result = $this->paypalRequest('POST', '/v2/checkout/orders', $payload);

			if (!empty($result['id'])) {
				$json['id'] = $result['id'];
			} else {
				$json['error'] = $this->extractError($result, $this->language->get('error_create'));
			}
		}

		$this->response->addHeader('Content-Type: application/json');
		$this->response->setOutput(json_encode($json));
	}

	public function capture(): void {
		$this->load->language('extension/opencart/payment/paypal');
		$json = [];

		$order_info = $this->validateOrder();
		$paypal_order_id = $this->request->post['order_id'] ?? '';

		if (!$order_info) {
			$json['error'] = $this->language->get('error_order');
		} elseif (!$paypal_order_id) {
			$json['error'] = $this->language->get('error_capture');
		} elseif (!$this->hasCredentials()) {
			$json['error'] = $this->language->get('error_credentials');
		} else {
			$intent = strtoupper((string)($this->config->get('payment_paypal_intent') ?: 'CAPTURE'));
			$action = $intent === 'AUTHORIZE' ? 'authorize' : 'capture';
			$result = $this->paypalRequest('POST', '/v2/checkout/orders/' . rawurlencode($paypal_order_id) . '/' . $action, new \stdClass());

			$status = $result['status'] ?? '';
			$transaction_id = $paypal_order_id;

			if (!empty($result['purchase_units'][0]['payments']['captures'][0]['id'])) {
				$transaction_id = $result['purchase_units'][0]['payments']['captures'][0]['id'];
			} elseif (!empty($result['purchase_units'][0]['payments']['authorizations'][0]['id'])) {
				$transaction_id = $result['purchase_units'][0]['payments']['authorizations'][0]['id'];
			}

			if (in_array($status, ['COMPLETED', 'APPROVED'], true)) {
				$this->load->model('checkout/order');
				$this->model_checkout_order->editTransactionId((int)$this->session->data['order_id'], $transaction_id);
				$this->model_checkout_order->addHistory((int)$this->session->data['order_id'], (int)$this->config->get('payment_paypal_order_status_id'), sprintf($this->language->get('text_payment_captured'), $transaction_id));

				$json['redirect'] = $this->url->link('checkout/success', 'language=' . $this->config->get('config_language'), true);
			} else {
				$json['error'] = $this->extractError($result, $this->language->get('error_capture'));
			}
		}

		$this->response->addHeader('Content-Type: application/json');
		$this->response->setOutput(json_encode($json));
	}

	private function validateOrder(): array {
		if (empty($this->session->data['order_id'])) {
			return [];
		}

		if (empty($this->session->data['payment_method']) || ($this->session->data['payment_method']['code'] ?? '') !== 'paypal.paypal') {
			return [];
		}

		$this->load->model('checkout/order');

		return $this->model_checkout_order->getOrder((int)$this->session->data['order_id']);
	}

	private function hasCredentials(): bool {
		return (bool)$this->config->get('payment_paypal_client_id') && (bool)$this->config->get('payment_paypal_secret');
	}

	private function paypalRequest(string $method, string $path, mixed $payload = null): array {
		$access_token = $this->getAccessToken();

		if (!$access_token) {
			return ['error' => 'Unable to obtain PayPal access token'];
		}

		$ch = curl_init($this->getApiBase() . $path);
		$headers = [
			'Content-Type: application/json',
			'Authorization: Bearer ' . $access_token
		];

		curl_setopt($ch, CURLOPT_CUSTOMREQUEST, $method);
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
		curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
		curl_setopt($ch, CURLOPT_TIMEOUT, 30);

		if ($payload !== null) {
			curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($payload));
		}

		$response = curl_exec($ch);
		$error = curl_error($ch);

		if ($response === false) {
			return ['error' => $error ?: 'PayPal request failed'];
		}

		$result = json_decode($response, true);

		return is_array($result) ? $result : ['error' => $response];
	}

	private function getAccessToken(): string {
		$ch = curl_init($this->getApiBase() . '/v1/oauth2/token');

		curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
		curl_setopt($ch, CURLOPT_POST, true);
		curl_setopt($ch, CURLOPT_POSTFIELDS, 'grant_type=client_credentials');
		curl_setopt($ch, CURLOPT_USERPWD, $this->config->get('payment_paypal_client_id') . ':' . $this->config->get('payment_paypal_secret'));
		curl_setopt($ch, CURLOPT_HTTPHEADER, ['Accept: application/json', 'Accept-Language: en_US']);
		curl_setopt($ch, CURLOPT_TIMEOUT, 30);

		$response = curl_exec($ch);

		$result = json_decode((string)$response, true);

		return is_array($result) && !empty($result['access_token']) ? $result['access_token'] : '';
	}

	private function getApiBase(): string {
		return $this->config->get('payment_paypal_environment') === 'live' ? 'https://api-m.paypal.com' : 'https://api-m.sandbox.paypal.com';
	}

	private function extractError(array $result, string $fallback): string {
		if (!empty($result['message'])) {
			return sprintf($this->language->get('error_paypal'), $result['message']);
		}

		if (!empty($result['error'])) {
			return sprintf($this->language->get('error_paypal'), is_string($result['error']) ? $result['error'] : json_encode($result['error']));
		}

		return $fallback;
	}
}
