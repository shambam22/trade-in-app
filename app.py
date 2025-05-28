from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

PRICECHARTING_API_KEY = "b41074978a21823114f1742ea664fe1ec9a77871"

def calculate_offers(loose_value):
    if loose_value < 10:
        return 0.50, 1.00
    elif loose_value <= 30:
        return loose_value * 0.20, loose_value * 0.40
    elif loose_value <= 50:
        return loose_value * 0.25, loose_value * 0.50
    elif loose_value <= 100:
        return loose_value * 0.30, loose_value * 0.60
    else:
        return loose_value * 0.35, loose_value * 0.70

def get_product_data_by_upc(upc):
    response = requests.get(f"https://www.pricecharting.com/api/product?upc={upc}&token={PRICECHARTING_API_KEY}")
    return response.json()

def get_product_data_by_name(name, console=None):
    query = name
    if console:
        query += f" {console}"
    response = requests.get(f"https://www.pricecharting.com/api/products?t={query}&token={PRICECHARTING_API_KEY}")
    results = response.json().get("products", [])
    if results:
        return results[0]  # Assume first result is best match
    return None

def get_product_data_by_id(product_id):
    response = requests.get(f"https://www.pricecharting.com/api/product?id={product_id}&token={PRICECHARTING_API_KEY}")
    return response.json()

@app.route("/", methods=["POST"])
def trade_in_lookup():
    data = request.get_json()
    product = None

    if "product_id" in data:
        product = get_product_data_by_id(data["product_id"])
    elif "upc" in data:
        product = get_product_data_by_upc(data["upc"])
    elif "name" in data:
        product = get_product_data_by_name(data["name"], data.get("console"))

    if not product or "product" not in product:
        return jsonify({"error": "Product not found"}), 404

    loose_value = float(product["product"]["loose-price"]) if isinstance(product["product"]["loose-price"], str) else product["product"]["loose-price"]
    cash, trade = calculate_offers(loose_value)

    return jsonify({
        "name": product["product"]["product-name"],
        "loose_value": loose_value,
        "cash": round(cash, 2),
        "trade": round(trade, 2)
    })

if __name__ == "__main__":
    app.run(debug=True)
