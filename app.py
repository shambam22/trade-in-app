from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

PRICECHARTING_API_KEY = 'b41074978a21823114f1742ea664fe1ec9a77871'

def calculate_trade_value(price):
    if price < 10.01:
        return 0.50, 1.00
    elif price <= 30.00:
        return round(price * 0.20, 2), round(price * 0.40, 2)
    elif price <= 50.00:
        return round(price * 0.25, 2), round(price * 0.50, 2)
    elif price <= 100.00:
        return round(price * 0.30, 2), round(price * 0.60, 2)
    elif price <= 100000.00:
        return round(price * 0.35, 2), round(price * 0.70, 2)
    return 0.00, 0.00

@app.route('/get_trade_value', methods=['GET'])
def get_trade_value():
    upc = request.args.get('upc')
    if not upc:
        return jsonify({'error': 'UPC is required'}), 400

    api_url = f'https://www.pricecharting.com/api/product?t={PRICECHARTING_API_KEY}&upc={upc}'
    response = requests.get(api_url)

    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch from PriceCharting'}), 500

    data = response.json()
    product = data['product']

    loose = float(product.get('loose-price', 0))
    cib = float(product.get('complete-price', 0))
    new = float(product.get('new-price', 0))

    loose_cash, loose_credit = calculate_trade_value(loose)
    cib_cash, cib_credit = calculate_trade_value(cib)
    new_cash, new_credit = calculate_trade_value(new)

    return jsonify({
        'title': product['product-name'],
        'platform': product['console-name'],
        'pricecharting': {
            'loose': loose,
            'cib': cib,
            'new': new
        },
        'trade_in': {
            'loose': {'cash': loose_cash, 'credit': loose_credit},
            'cib': {'cash': cib_cash, 'credit': cib_credit},
            'new': {'cash': new_cash, 'credit': new_credit}
        }
    })
