from flask import Flask, request, jsonify, send_from_directory  # ✅ Added send_from_directory
import pandas as pd
import random

# Load inventory data
inventory_df = pd.read_csv("inventory_extended.csv")

# Agents
class ForecastingAgent:
    def predict_demand(self, product_name, customer_score):
        base = random.randint(20, 40)
        return base + int(customer_score * 0.6)

class InventoryAgent:
    def get_product_info(self, product_name):
        item = inventory_df[inventory_df['product_name'].str.lower() == product_name.lower()]
        if item.empty:
            return None
        return item.iloc[0]

class OrderAgent:
    def place_order(self, product_name, quantity, supplier):
        return f"Order placed: {quantity} units of {product_name} from {supplier}"

class SupplierAgent:
    def get_supplier(self, product):
        return product['supplier']

class WarehouseAgent:
    def get_warehouse_location(self, product):
        return product['warehouse']

class CustomerAgent:
    def get_customer_demand_score(self, product):
        return product['customer_demand_score']

# Flask App
app = Flask(__name__)

# ✅ Serve HTML page
@app.route("/")
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route("/check_inventory", methods=["GET"])
def check_inventory():
    product_name = request.args.get("product")

    inventory_agent = InventoryAgent()
    forecasting_agent = ForecastingAgent()
    order_agent = OrderAgent()
    supplier_agent = SupplierAgent()
    warehouse_agent = WarehouseAgent()
    customer_agent = CustomerAgent()

    product = inventory_agent.get_product_info(product_name)
    if product is None:
        return jsonify({"error": f"Product '{product_name}' not found."}), 404

    customer_score = customer_agent.get_customer_demand_score(product)
    predicted_demand = forecasting_agent.predict_demand(product['product_name'], customer_score)

    reorder_needed = product['current_stock'] < predicted_demand
    order_info = None
    if reorder_needed:
        order_qty = predicted_demand - product['current_stock']
        order_info = order_agent.place_order(product['product_name'], order_qty, product['supplier'])

        return jsonify({
        "product": str(product['product_name']),
        "stock": int(product['current_stock']),
        "reorder_level": int(product['reorder_level']),
        "warehouse": str(warehouse_agent.get_warehouse_location(product)),
        "supplier": str(supplier_agent.get_supplier(product)),
        "customer_score": int(customer_score),
        "predicted_demand": int(predicted_demand),
        "reorder_needed": bool(reorder_needed),
        "order_info": str(order_info) if order_info else None
    })


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

