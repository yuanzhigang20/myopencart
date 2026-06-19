-- Lovanest PayPal-only checkout settings
-- Applied to production on 2026-06-19.

UPDATE oc_setting SET value='0' WHERE code='payment_cod' AND `key`='payment_cod_status';
UPDATE oc_setting SET value='0' WHERE code='payment_free_checkout' AND `key`='payment_free_checkout_status';
UPDATE oc_setting SET value='1' WHERE code='payment_paypal' AND `key`='payment_paypal_status';
UPDATE oc_setting SET value='1' WHERE code='shipping_flat' AND `key`='shipping_flat_status';
UPDATE oc_setting SET value='5.00' WHERE code='shipping_flat' AND `key`='shipping_flat_cost';
