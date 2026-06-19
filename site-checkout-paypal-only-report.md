# Checkout PayPal-Only Wellness Optimization - 2026-06-19

## Scope
Optimized the OpenCart checkout page for Lovanest as a premium, private, adult wellness checkout experience.

## Key Changes
- Checkout page now uses a cream/white premium card layout with two columns on desktop and one column on mobile.
- PayPal is automatically selected and initialized after address, shipping, and terms state are available.
- Cash On Delivery and Free Checkout were disabled in production settings and filtered from checkout payment methods.
- Flat Shipping Rate is automatically selected when available; shipping radio UI and Refresh buttons are removed from the visible checkout.
- Order summary is rendered as a modern list instead of a table.
- PayPal SDK is configured with `enable-funding=paypal` and `disable-funding=card,credit,paylater,venmo`.
- A code comment notes the PayPal funding policy and official PayPal-hosted guest behavior.

## Production Setting Changes
```sql
UPDATE oc_setting SET value='0' WHERE code='payment_cod' AND `key`='payment_cod_status';
UPDATE oc_setting SET value='0' WHERE code='payment_free_checkout' AND `key`='payment_free_checkout_status';
UPDATE oc_setting SET value='1' WHERE code='payment_paypal' AND `key`='payment_paypal_status';
UPDATE oc_setting SET value='1' WHERE code='shipping_flat' AND `key`='shipping_flat_status';
UPDATE oc_setting SET value='5.00' WHERE code='shipping_flat' AND `key`='shipping_flat_cost';
```
Saved in `database/2026-06-19-checkout-paypal-only.sql`.

## Verification Summary
- Guest checkout: completed address entry and auto-initialized PayPal.
- PayPal button: rendered automatically after checkout initialization.
- PayPal click: opened PayPal sandbox popup/tab successfully.
- Payment methods: Cash On Delivery text not present; Refresh text not present.
- Order summary: no `<table>` present; shows product, subtotal, shipping, total.
- Desktop layout: two-column grid with sticky summary.
- Mobile widths 375/390/430: one-column layout; PayPal container remains present; horizontal overflow suppressed.

## Known Notes
- Full PayPal capture/success-page test still requires a Personal/Buyer PayPal Sandbox account. Seller/business accounts cannot pay themselves.
- Guest checkout form uses a simplified US country/state select to avoid dependency on missing frontend x-country/x-zone component registration in the current theme.
