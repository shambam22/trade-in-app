import requests
from flask import Flask, render_template, request

app = Flask(__name__)

API_KEY = 'b41074978a21823114f1742ea664fe1ec9a77871'  # Your actual PriceCharting API key

def get_supported_platforms():
    url = f'https://www.pricecharting.com/api/platforms?t={API_KEY}'
    response = requests.get(url)
    data = response.json()
    if isinstance(data, list):
        return {platform['name']: platform['slug'] for platform in data}
    return {}

def get_price_data(game_title, platform_filter=None):
    url = f'https://www.pricecharting.com/api/products?t={API_KEY}&q={game_title}'
    response = requests.get(url)
    data = response.json()

    if data and isinstance(data, list):
        for item in data:
            if platform_filter and platform_filter.lower() in item['console_name'].lower():
                return {
                    'title': item['product_name'],
                    'loose_price': float(item['loose_price']),
                    'cib_price': float(item['complete_price']),
                    'new_price': float(item['new_price']),
                    'image_url': item.get('box_art_url', '')
                }
        item = data[0]
        return {
            'title': item['product_name'],
            'loose_price': float(item['loose_price']),
            'cib_price': float(item['complete_price']),
            'new_price': float(item['new_price']),
            'image_url': item.get('box_art_url', '')
        }
    return None

def calculate_trade_in(price, offer_type):
    if price <= 10:
        return 0.50 if offer_type == 'cash' else 1.00
    elif price <= 30:
        return round(price * 0.20, 2) if offer_type == 'cash' else round(price * 0.40, 2)
    elif price <= 50:
        return round(price * 0.25, 2) if offer_type == 'cash' else round(price * 0.50, 2)
    elif price <= 100:
        return round(price * 0.30, 2) if offer_type == 'cash' else round(price * 0.60, 2)
    else:
        return round(price * 0.35, 2) if offer_type == 'cash' else round(price * 0.70, 2)

@app.route('/', methods=['GET', 'POST'])
def index():
    trade_data = None
    platforms = get_supported_platforms()
    if request.method == 'POST':
        game = request.form['game']
        platform = request.form.get('platform', '')
        data = get_price_data(game, platform)
        if data:
            trade_data = {
                'title': data['title'],
                'image_url': data['image_url'],
                'loose_credit': calculate_trade_in(data['loose_price'], 'credit'),
                'loose_cash': calculate_trade_in(data['loose_price'], 'cash'),
                'cib_credit': calculate_trade_in(data['cib_price'], 'credit'),
                'cib_cash': calculate_trade_in(data['cib_price'], 'cash'),
                'new_credit': calculate_trade_in(data['new_price'], 'credit'),
                'new_cash': calculate_trade_in(data['new_price'], 'cash'),
            }
    return render_template('index.html', trade_data=trade_data, platforms=platforms)

if __name__ == '__main__':
    app.run()
