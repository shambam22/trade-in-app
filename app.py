from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

PRICECHARTING_API_KEY = 'b41074978a21823114f1742ea664fe1ec9a77871'

def calculate_trade_value(market_price):
    if market_price < 10.01:
        return 0.50, 1.00
    elif market_price <= 30.00:
        return round(market_price * 0.20, 2), round(market_price * 0.40, 2)
    elif market_price <= 50.00:
        return round(market_price * 0.25, 2), round(market_price * 0.50, 2)
    elif market_price <= 100.00:
        return round(market_price * 0.30, 2), round(market_price * 0.60, 2)
    elif market_price <= 100000.00:
        return round(market_price * 0.35, 2), round(market_price * 0.70, 2)
    return 0.00, 0.00

@app.route('/get_trade_value', methods=['GET'])
def get_trade_value():
    upc = request.args.get('upc')
    if not upc:
        return jsonify({'error': 'UPC is required'}), 400

    pc_url = f'https://www.pricecharting.com/api/product?t={PRICECHARTING_API_KEY}&upc={upc}'
    response = requests.get(pc_url)

    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch from PriceCharting'}), 500

    data = response.json()
    product = data['product']

    loose_price = float(product.get('loose-price', 0))
    cib_price = float(product.get('complete-price', 0))
    new_price = float(product.get('new-price', 0))

    trade_in_loose_cash, trade_in_loose_credit = calculate_trade_value(loose_price)
    trade_in_cib_cash, trade_in_cib_credit = calculate_trade_value(cib_price)
    trade_in_new_cash, trade_in_new_credit = calculate_trade_value(new_price)

    return jsonify({
        'title': product['product-name'],
        'platform': product['console-name'],
        'pricecharting': {
            'loose': loose_price,
            'cib': cib_price,
            'new': new_price
        },
        'trade_in': {
            'loose': {'cash': trade_in_loose_cash, 'credit': trade_in_loose_credit},
            'cib': {'cash': trade_in_cib_cash, 'credit': trade_in_cib_credit},
            'new': {'cash': trade_in_new_cash, 'credit': trade_in_new_credit}
        }
    })
