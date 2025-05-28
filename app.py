from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "b41074978a21823114f1742ea664fe1ec9a77871"
API_URL = "https://www.pricecharting.com/api/products"

def calculate_trade_value(price):
    if price <= 10:
        return 0.50, 1.00
    elif price <= 30:
        return round(price * 0.20, 2), round(price * 0.40, 2)
    elif price <= 50:
        return round(price * 0.25, 2), round(price * 0.50, 2)
    elif price <= 100:
        return round(price * 0.30, 2), round(price * 0.60, 2)
    else:
        return round(price * 0.35, 2), round(price * 0.70, 2)

@app.route("/tradein", methods=["GET"])
def get_tradein_value():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Missing 'query' parameter"}), 400

    response = requests.get(API_URL, params={"t": API_KEY, "product-name": query})
    data = response.json()

    if "products" not in data or not data["products"]:
        return jsonify({"error": "No products found"}), 404

    product = data["products"][0]
    title = product.get("product-name")
    console = product.get("console-name")
    price = float(product.get("loose-price", 0.0))

    cash, credit = calculate_trade_value(price)

    return jsonify({
        "title": title,
        "console": console,
        "loose_price": price,
        "cash_value": cash,
        "store_credit": credit,
    })

if __name__ == "__main__":
    app.run(debug=True)
