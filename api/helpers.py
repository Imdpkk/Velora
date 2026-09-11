import json
import os
from datetime import datetime


# ==========================================
# File & JSON Helpers
# ==========================================

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def load_json(relative_path):
    """
    Load a JSON file from the project.
    """
    file_path = os.path.join(BASE_DIR, relative_path)

    if not os.path.exists(file_path):
        return None

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


# ==========================================
# Date & Time
# ==========================================

def get_today():
    return datetime.now().strftime("%d %B %Y")


def get_time():
    return datetime.now().strftime("%I:%M %p")


# ==========================================
# Text Helpers
# ==========================================

def normalize_text(text):
    """
    Convert text to lowercase and remove extra spaces.
    """
    if not text:
        return ""

    return " ".join(text.lower().strip().split())


# ==========================================
# Fashion Intent Detection
# ==========================================

FASHION_KEYWORDS = [
    "dress",
    "dresses",
    "top",
    "tops",
    "shirt",
    "shirts",
    "tshirt",
    "jeans",
    "trouser",
    "pants",
    "kurti",
    "hoodie",
    "jacket",
    "coord",
    "co-ord",
    "fashion",
    "style",
    "styling",
    "outfit",
    "look",
    "party",
    "wedding",
    "casual",
    "office",
    "size",
    "sizes",
    "delivery",
    "shipping",
    "exchange",
    "return",
    "refund",
    "payment",
    "price",
    "buy",
    "order",
    "catalog",
    "collection",
    "fabric",
    "colour",
    "color",
    "instagram",
    "velora"
]


def is_fashion_query(message):
    """
    Returns True if the user's message appears to be related
    to fashion or shopping.
    """
    text = normalize_text(message)

    return any(keyword in text for keyword in FASHION_KEYWORDS)


# ==========================================
# Product Helpers
# ==========================================

def search_products(products, keyword):
    """
    Search products by name, category, color or occasion.
    """
    keyword = normalize_text(keyword)

    results = []

    for product in products:

        searchable = " ".join([
            str(product.get("name", "")),
            str(product.get("category", "")),
            str(product.get("occasion", "")),
            " ".join(product.get("colors", []))
        ]).lower()

        if keyword in searchable:
            results.append(product)

    return results


# ==========================================
# Response Helpers
# ==========================================

def success(message):
    return {
        "success": True,
        "message": message
    }


def error(message):
    return {
        "success": False,
        "message": message
    }


# ==========================================
# Chat Memory
# ==========================================

class ChatMemory:

    def __init__(self, max_messages=8):
        self.max_messages = max_messages
        self.messages = []

    def add(self, role, content):
        self.messages.append({
            "role": role,
            "content": content
        })

        if len(self.messages) > self.max_messages:
            self.messages.pop(0)

    def history(self):
        return self.messages

    def clear(self):
        self.messages = []


# ==========================================
# Product Card Formatter
# ==========================================

def product_card(product):
    """
    Convert a product dictionary into a readable text card.
    """

    return f"""
👗 {product['name']}

💰 Price: ₹{product['price']}

📏 Sizes: {", ".join(product['sizes'])}

🎨 Colors: {", ".join(product['colors'])}

✨ Occasion: {product['occasion']}

📝 {product['description']}

📦 {"In Stock ✅" if product['stock'] else "Out of Stock ❌"}

💖 DM us on @velora_style14 to order.
""".strip()