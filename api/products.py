import random
from api.helpers import load_json, normalize_text

# Load products once
PRODUCTS = load_json("data/products.json") or []


class ProductManager:

    def __init__(self):
        self.products = PRODUCTS

    # -------------------------
    # Get all products
    # -------------------------
    def all_products(self):
        return self.products

    # -------------------------
    # Product by ID
    # -------------------------
    def get_by_id(self, product_id):
        for product in self.products:
            if product["id"] == product_id:
                return product
        return None

    # -------------------------
    # Search everything
    # -------------------------
    def search(self, query):

        query = normalize_text(query)

        results = []

        for product in self.products:

            searchable_text = " ".join([
                product.get("name", ""),
                product.get("category", ""),
                product.get("occasion", ""),
                " ".join(product.get("colors", [])),
                product.get("description", "")
            ]).lower()

            if query in searchable_text:
                results.append(product)

        return results

    # -------------------------
    # Category
    # -------------------------
    def by_category(self, category):

        category = normalize_text(category)

        return [
            p for p in self.products
            if category in p["category"].lower()
        ]

    # -------------------------
    # Occasion
    # -------------------------
    def by_occasion(self, occasion):

        occasion = normalize_text(occasion)

        return [
            p for p in self.products
            if occasion in p["occasion"].lower()
        ]

    # -------------------------
    # Color
    # -------------------------
    def by_color(self, color):

        color = normalize_text(color)

        matches = []

        for product in self.products:

            colors = [c.lower() for c in product["colors"]]

            if color in colors:
                matches.append(product)

        return matches

    # -------------------------
    # In Stock
    # -------------------------
    def in_stock(self):

        return [
            p for p in self.products
            if p["stock"]
        ]

    # -------------------------
    # Best Sellers
    # -------------------------
    def best_sellers(self, limit=3):

        available = self.in_stock()

        random.shuffle(available)

        return available[:limit]

    # -------------------------
    # Latest Arrivals
    # -------------------------
    def latest(self, limit=4):

        return self.products[-limit:]

    # -------------------------
    # Random Suggestions
    # -------------------------
    def random_products(self, limit=3):

        if len(self.products) <= limit:
            return self.products

        return random.sample(self.products, limit)

    # -------------------------
    # Price Range
    # -------------------------
    def by_price(self, minimum, maximum):

        return [
            p for p in self.products
            if minimum <= p["price"] <= maximum
        ]

    # -------------------------
    # Format product
    # -------------------------
    def format_product(self, product):

        return f"""
👗 {product['name']}

💰 ₹{product['price']}

📏 Sizes: {", ".join(product['sizes'])}

🎨 Colors: {", ".join(product['colors'])}

✨ Occasion:
{product['occasion']}

📝 {product['description']}

📦 {'In Stock ✅' if product['stock'] else 'Out of Stock ❌'}
""".strip()


# Singleton
product_manager = ProductManager()