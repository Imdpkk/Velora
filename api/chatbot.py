import os
import re
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types

from api.helpers import (
    ChatMemory,
    get_today,
    normalize_text,
    is_fashion_query
)

from api.products import product_manager


# =========================================================
# ENVIRONMENT
# =========================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is missing in the .env file."
    )


# =========================================================
# GEMINI CLIENT
# =========================================================

client = genai.Client(api_key=API_KEY)


# =========================================================
# BRAND CONFIGURATION
# =========================================================

BRAND_NAME = "Velora Style 14"

INSTAGRAM = "@velora_style14"

DELIVERY = "3–7 business days"

EXCHANGE = (
    "Size exchange is available within 48 hours if the item "
    "is unused and tags are attached."
)


# =========================================================
# CHAT MEMORY
# =========================================================

memory = ChatMemory(max_messages=8)


# =========================================================
# VELORA AI
# =========================================================

class VeloraChatbot:

    def __init__(self):

        self.client = client
        self.memory = memory

    # =====================================================
    # TEXT HELPERS
    # =====================================================

    def clean_text(self, text):

        return normalize_text(text).strip().lower()

    # =====================================================
    # BUDGET EXTRACTION
    # =====================================================

    def extract_budget(self, message):

        text = self.clean_text(message)

        patterns = [

            r"(?:under|below|less than|within|upto|up to)"
            r"[^\d₹]*(\d+(?:\.\d+)?)",

            r"₹\s*(\d+(?:\.\d+)?)"
            r"\s*(?:budget|max|maximum)",

            r"(\d+(?:\.\d+)?)"
            r"\s*(?:budget|max|maximum)"
        ]

        for pattern in patterns:

            match = re.search(pattern, text)

            if match:

                try:
                    return float(match.group(1))

                except ValueError:
                    pass

        return None

    # =====================================================
    # DISCOVERY INTENT
    # =====================================================

    def detect_discovery_intent(self, message):

        text = self.clean_text(message)

        # -------------------------------------------------
        # NEW ARRIVALS
        # -------------------------------------------------

        new_phrases = [
            "new",
            "new clothes",
            "new cloths",
            "new arrivals",
            "new arrival",
            "latest",
            "latest collection",
            "new collection",
            "show me new",
            "show new clothes"
        ]

        if (
            text in new_phrases
            or "new arrivals" in text
            or "new collection" in text
        ):
            return "new"

        # -------------------------------------------------
        # TRENDING
        # -------------------------------------------------

        trending_phrases = [
            "trending",
            "trend",
            "trends",
            "what is trending",
            "whats trending",
            "what's trending",
            "show trending",
            "show me trending"
        ]

        if (
            text in trending_phrases
            or "trending" in text
        ):
            return "trending"

        # -------------------------------------------------
        # CATALOG
        # -------------------------------------------------

        catalog_phrases = [
            "what do you have",
            "what's available",
            "whats available",
            "show me everything",
            "show everything",
            "show all",
            "all products",
            "all clothes",
            "available clothes",
            "available products",
            "catalog",
            "catalogue"
        ]

        if text in catalog_phrases:
            return "catalog"

        return None

    # =====================================================
    # MAIN INTENT DETECTION
    # =====================================================

    def detect_intent(self, message):

        text = self.clean_text(message)

        # -------------------------------------------------
        # GREETINGS
        # -------------------------------------------------

        greetings = {
            "hi",
            "hii",
            "hiii",
            "hello",
            "hey",
            "heyy",
            "good morning",
            "good afternoon",
            "good evening"
        }

        if text in greetings:
            return "greeting"

        # -------------------------------------------------
        # PRODUCT REQUESTS
        #
        # Product detection happens BEFORE generic
        # size/order/price detection.
        # -------------------------------------------------

        product_words = [

            "dress",
            "dresses",

            "top",
            "tops",

            "shirt",
            "shirts",

            "jeans",
            "jean",

            "hoodie",

            "kurti",

            "co-ord",
            "coord",

            "jacket",

            "outfit",

            "clothes",
            "clothing",

            "wear",

            "look",

            "party",
            "partywear",

            "casual",

            "office",

            "work",

            "vacation",

            "holiday",

            "wedding",

            "college",

            "festive"
        ]

        if any(word in text for word in product_words):
            return "product"

        # -------------------------------------------------
        # DELIVERY
        # -------------------------------------------------

        delivery_words = [
            "delivery",
            "shipping",
            "ship",
            "deliver",
            "courier"
        ]

        if any(word in text for word in delivery_words):
            return "delivery"

        # -------------------------------------------------
        # EXCHANGE
        # -------------------------------------------------

        exchange_words = [
            "exchange",
            "replace",
            "replacement"
        ]

        if any(word in text for word in exchange_words):
            return "exchange"

        # -------------------------------------------------
        # SIZE
        # -------------------------------------------------

        size_words = [
            "size",
            "sizes",
            "fit",
            "measurement",
            "measurements"
        ]

        if any(word in text for word in size_words):
            return "size"

        # -------------------------------------------------
        # ORDER
        # -------------------------------------------------

        order_words = [
            "checkout",
            "place order",
            "how to order",
            "want to order"
        ]

        if any(word in text for word in order_words):
            return "order"

        # -------------------------------------------------
        # GENERAL FASHION
        # -------------------------------------------------

        if is_fashion_query(message):
            return "general"

        return "unrelated"

    # =====================================================
    # PRODUCT SEARCH
    # =====================================================

    def search_products(self, message):

        text = self.clean_text(message)

        products = product_manager.in_stock()

        # -------------------------------------------------
        # CATEGORY
        # -------------------------------------------------

        category = None

        if (
            "dress" in text
            or "dresses" in text
        ):

            category = "dress"

        elif (
            "shirt" in text
            or "top" in text
            or "tops" in text
        ):

            category = "top"

        elif (
            "jeans" in text
            or "jean" in text
        ):

            category = "jeans"

        elif (
            "co-ord" in text
            or "coord" in text
        ):

            category = "co-ord set"

        elif "hoodie" in text:

            category = "hoodie"

        elif "jacket" in text:

            category = "jacket"

        # -------------------------------------------------
        # OCCASION
        # -------------------------------------------------

        occasion = None

        if any(word in text for word in [
            "party",
            "partywear",
            "evening",
            "night out"
        ]):

            occasion = "party"

        elif any(word in text for word in [
            "casual",
            "everyday",
            "daily"
        ]):

            occasion = "casual"

        elif any(word in text for word in [
            "office",
            "work",
            "formal"
        ]):

            occasion = "office"

        elif any(word in text for word in [
            "vacation",
            "holiday",
            "brunch"
        ]):

            occasion = "vacation"

        elif "wedding" in text:

            occasion = "wedding"

        elif "college" in text:

            occasion = "college"

        elif any(word in text for word in [
            "festive",
            "festival"
        ]):

            occasion = "festive"

        # -------------------------------------------------
        # COLOR
        # -------------------------------------------------

        color = None

        colors = [
            "black",
            "white",
            "pink",
            "blue",
            "red",
            "green",
            "beige"
        ]

        for item in colors:

            if item in text:

                color = item
                break

        # -------------------------------------------------
        # BUDGET
        # -------------------------------------------------

        budget = self.extract_budget(message)

        # -------------------------------------------------
        # FILTER PRODUCTS
        # -------------------------------------------------

        results = []

        for product in products:

            product_category = (
                product.get(
                    "category",
                    ""
                ).lower()
            )

            product_occasion = (
                product.get(
                    "occasion",
                    ""
                ).lower()
            )

            product_colors = [
                color_item.lower()
                for color_item in product.get(
                    "colors",
                    []
                )
            ]

            # Category filter
            if (
                category
                and category not in product_category
            ):
                continue

            # Occasion filter
            if (
                occasion
                and occasion not in product_occasion
            ):
                continue

            # Color filter
            if (
                color
                and color not in product_colors
            ):
                continue

            # Budget filter
            if (
                budget is not None
                and product.get(
                    "price",
                    0
                ) > budget
            ):
                continue

            results.append(product)

        return results

    # =====================================================
    # PRODUCT RECOMMENDATIONS
    # =====================================================

    def recommend_products(self, message):

        text = self.clean_text(message)

        results = self.search_products(message)

        # Exact matches
        if results:
            return results[:3]

        # -------------------------------------------------
        # DRESS FALLBACK
        # -------------------------------------------------

        if (
            "dress" in text
            or "dresses" in text
        ):

            dresses = [

                product
                for product in product_manager.in_stock()

                if "dress" in product.get(
                    "category",
                    ""
                ).lower()
            ]

            budget = self.extract_budget(message)

            if budget is not None:

                dresses = [

                    product
                    for product in dresses

                    if product.get(
                        "price",
                        0
                    ) <= budget
                ]

            return dresses[:3]

        # -------------------------------------------------
        # CASUAL FALLBACK
        # -------------------------------------------------

        if "casual" in text:

            casual = [

                product
                for product in product_manager.in_stock()

                if "casual" in product.get(
                    "occasion",
                    ""
                ).lower()
            ]

            return casual[:3]

        # -------------------------------------------------
        # GENERAL FALLBACK
        # -------------------------------------------------

        return product_manager.best_sellers(
            limit=3
        )

    # =====================================================
    # PRODUCT RESPONSE
    # =====================================================

    def product_response(self, message):

        text = self.clean_text(message)

        products = self.recommend_products(
            message
        )

        # -------------------------------------------------
        # CASUAL DRESS
        # -------------------------------------------------

        if (
            "casual" in text
            and "dress" in text
        ):

            dress_products = [

                product
                for product in product_manager.in_stock()

                if "dress" in product.get(
                    "category",
                    ""
                ).lower()
            ]

            casual_dresses = [

                product
                for product in dress_products

                if "casual" in product.get(
                    "occasion",
                    ""
                ).lower()
            ]

            if not casual_dresses:

                if dress_products:

                    response = (
                        "We don't currently have a dress "
                        "specifically listed for a casual "
                        "occasion. Our closest dress options "
                        "are:\n\n"
                    )

                    for product in dress_products[:2]:

                        response += (
                            f"• {product['name']} — "
                            f"₹{product['price']:,}\n"
                        )

                    response += (
                        "\nI can also suggest a casual outfit "
                        "using our shirts or jeans."
                    )

                    return response

        # -------------------------------------------------
        # NO PRODUCTS
        # -------------------------------------------------

        if not products:

            if "dress" in text:

                return (
                    "I couldn't find a dress matching those "
                    "exact requirements in our current "
                    "collection. Try changing the budget, "
                    "color or occasion."
                )

            return (
                "I couldn't find an exact match in our "
                "current collection. Tell me your preferred "
                "style, color or budget and I'll narrow "
                "it down."
            )

        # -------------------------------------------------
        # ONE PRODUCT
        # -------------------------------------------------

        if len(products) == 1:

            product = products[0]

            return (
                f"I'd recommend the "
                f"{product['name']} "
                f"at ₹{product['price']:,}. "
                f"{product['description']} "
                f"Available in "
                f"{', '.join(product['sizes'])}."
            )

        # -------------------------------------------------
        # MULTIPLE PRODUCTS
        # -------------------------------------------------

        response = (
            "Here are a few options that match "
            "your request:\n\n"
        )

        for product in products:

            response += (
                f"• {product['name']} — "
                f"₹{product['price']:,}\n"
            )

        response += (
            "\nTell me which one you like and I can "
            "help with sizing, styling or ordering."
        )

        return response

    # =====================================================
    # NEW ARRIVALS
    # =====================================================

    def new_arrivals_response(self):

        products = product_manager.in_stock()

        if not products:

            return (
                "There are no new arrivals available "
                "right now."
            )

        # Current catalog is the source of truth.
        # Show latest products from the catalog.
        products = products[-5:]

        response = (
            "Here are some of our latest styles:\n\n"
        )

        for product in products:

            response += (
                f"• {product['name']} — "
                f"₹{product['price']:,}\n"
            )

        response += (
            "\nTell me which style you like and I can "
            "help you choose the right size or outfit."
        )

        return response

    # =====================================================
    # TRENDING
    # =====================================================

    def trending_response(self):

        products = product_manager.in_stock()

        trending_names = [
            "Black Satin Midi Dress",
            "Beige Co-ord Set",
            "Oversized White Shirt"
        ]

        trending = [

            product
            for product in products

            if product.get("name")
            in trending_names
        ]

        if not trending:

            trending = products[:3]

        response = (
            "Here are a few styles from our "
            "current collection:\n\n"
        )

        for product in trending:

            response += (
                f"• {product['name']} — "
                f"₹{product['price']:,}\n"
            )

        response += (
            "\nWant something for party, casual, "
            "office or vacation?"
        )

        return response

    # =====================================================
    # FULL CATALOG
    # =====================================================

    def catalog_response(self):

        products = product_manager.in_stock()

        if not products:

            return (
                "Our collection is currently "
                "unavailable."
            )

        response = (
            "Here's what's currently available "
            "at Velora:\n\n"
        )

        for product in products:

            response += (
                f"• {product['name']} — "
                f"₹{product['price']:,}\n"
            )

        response += (
            "\nTell me a category, occasion or budget "
            "and I'll narrow it down for you."
        )

        return response

    # =====================================================
    # CONTEXTUAL SHORT RESPONSES
    # =====================================================

    def contextual_response(self, message):

        text = self.clean_text(message)

        history = self.memory.history()

        # Find previous assistant message
        previous_assistant = None

        for item in reversed(history[:-1]):

            if item["role"] == "assistant":

                previous_assistant = item["content"]
                break

        # -------------------------------------------------
        # SIZE FOLLOW-UP
        # -------------------------------------------------

        size_values = {
            "xs": "XS",
            "s": "S",
            "small": "S",
            "m": "M",
            "medium": "M",
            "l": "L",
            "large": "L",
            "xl": "XL",
            "xxl": "XXL"
        }

        if text in size_values:

            size = size_values[text]

            if previous_assistant:

                previous_lower = (
                    previous_assistant.lower()
                )

                if (
                    "size" in previous_lower
                    or "measurements" in previous_lower
                    or "usual size" in previous_lower
                ):

                    return (
                        f"Got it — {size}. "
                        "Which product are you choosing? "
                        f"I can check whether {size} is "
                        "available for that item."
                    )

        # -------------------------------------------------
        # YES / OKAY
        # -------------------------------------------------

        if text in [
            "yes",
            "yeah",
            "yep",
            "sure",
            "okay",
            "ok",
            "haan",
            "ha"
        ]:

            if previous_assistant:

                previous_lower = (
                    previous_assistant.lower()
                )

                if "size" in previous_lower:

                    return (
                        "Sure. Tell me the product name "
                        "and your usual size, and I'll "
                        "help you choose."
                    )

        return None

    # =====================================================
    # GREETING
    # =====================================================

    def greeting_response(self):

        return (
            "Hi! Welcome to Velora Style 14. "
            "I'm your AI fashion stylist. "
            "What are you looking for today — "
            "a dress, casual look, party outfit "
            "or office wear?"
        )

    # =====================================================
    # DELIVERY
    # =====================================================

    def delivery_response(self):

        return (
            f"Our standard delivery time is {DELIVERY}. "
            "If you have a specific order, tell me "
            "the details and I'll help you with the "
            "next step."
        )

    # =====================================================
    # EXCHANGE
    # =====================================================

    def exchange_response(self):

        return EXCHANGE

    # =====================================================
    # SIZE
    # =====================================================

    def size_response(self):

        return (
            "Of course. Tell me the product you're "
            "interested in and your usual size. "
            "If you're between sizes, you can also "
            "share your measurements and I'll help "
            "you choose."
        )

    # =====================================================
    # ORDER
    # =====================================================

    def order_response(self):

        return (
            "Sure. Tell me which product you'd like "
            "to order and your preferred size. "
            "I'll guide you through the next step."
        )

    # =====================================================
    # UNRELATED
    # =====================================================

    def unrelated_response(self):

        return (
            "I'm Velora's fashion assistant, so I can "
            "help with our women's collection, styling, "
            "sizes, delivery and orders. What would "
            "you like to explore?"
        )

    # =====================================================
    # GEMINI GENERAL FASHION RESPONSE
    # =====================================================

    def gemini_response(self, message):

        history = self.memory.history()

        conversation = "\n".join(
            [
                f"{item['role']}: {item['content']}"
                for item in history
            ]
        )

        prompt = f"""
You are the professional AI fashion stylist
for {BRAND_NAME}.

Your personality:

- Professional
- Warm
- Natural
- Helpful
- Fashion-aware
- Concise
- Conversational
- Not childish
- Not overly enthusiastic

You help customers with:

- Women's fashion
- Dresses
- Tops
- Shirts
- Jeans
- Co-ord sets
- Outfit ideas
- Styling
- Sizes
- Delivery
- Exchanges
- Orders

Important rules:

1. Only talk about Velora Style 14 and women's fashion.
2. Never invent products, prices, sizes or policies.
3. Do not use emojis unless genuinely useful.
4. Do not repeat the same sentence structure.
5. Do not force Instagram into every response.
6. Mention Instagram only when the customer is clearly
   ready to order.
7. Keep the response under 100 words.
8. If you don't know something, say so honestly.
9. Speak like a real fashion stylist.
10. Never pretend that unavailable products exist.

Current date:
{get_today()}

Conversation history:
{conversation}

Customer:
{message}

Respond naturally and professionally.
"""

        for attempt in range(3):

            try:

                response = self.client.models.generate_content(

                    model="gemini-2.5-flash",

                    contents=prompt,

                    config=types.GenerateContentConfig(
                        temperature=0.6
                    )
                )

                if response and response.text:

                    return response.text.strip()

            except Exception as error:

                print(
                    f"GEMINI ERROR "
                    f"(attempt {attempt + 1}): "
                    f"{error}"
                )

                if attempt < 2:

                    time.sleep(2)

        return (
            "I'm having trouble connecting right now. "
            "You can still ask me about our products, "
            "sizes, delivery or exchanges."
        )

    # =====================================================
    # MAIN RESPONSE
    # =====================================================

    def generate_response(self, message):

        message = message.strip()

        if not message:

            return (
                "What would you like to explore today?"
            )

        # -------------------------------------------------
        # DISCOVERY REQUESTS
        # -------------------------------------------------

        discovery = self.detect_discovery_intent(
            message
        )

        if discovery == "new":

            self.memory.add(
                "user",
                message
            )

            reply = self.new_arrivals_response()

            self.memory.add(
                "assistant",
                reply
            )

            return reply

        if discovery == "trending":

            self.memory.add(
                "user",
                message
            )

            reply = self.trending_response()

            self.memory.add(
                "assistant",
                reply
            )

            return reply

        if discovery == "catalog":

            self.memory.add(
                "user",
                message
            )

            reply = self.catalog_response()

            self.memory.add(
                "assistant",
                reply
            )

            return reply

        # -------------------------------------------------
        # CONTEXTUAL SHORT MESSAGE
        # -------------------------------------------------

        contextual = self.contextual_response(
            message
        )

        if contextual:

            self.memory.add(
                "user",
                message
            )

            self.memory.add(
                "assistant",
                contextual
            )

            return contextual

        # -------------------------------------------------
        # NORMAL MESSAGE
        # -------------------------------------------------

        self.memory.add(
            "user",
            message
        )

        intent = self.detect_intent(
            message
        )

        # -------------------------------------------------
        # GREETING
        # -------------------------------------------------

        if intent == "greeting":

            reply = self.greeting_response()

        # -------------------------------------------------
        # PRODUCT
        # -------------------------------------------------

        elif intent == "product":

            reply = self.product_response(
                message
            )

        # -------------------------------------------------
        # DELIVERY
        # -------------------------------------------------

        elif intent == "delivery":

            reply = self.delivery_response()

        # -------------------------------------------------
        # EXCHANGE
        # -------------------------------------------------

        elif intent == "exchange":

            reply = self.exchange_response()

        # -------------------------------------------------
        # SIZE
        # -------------------------------------------------

        elif intent == "size":

            reply = self.size_response()

        # -------------------------------------------------
        # ORDER
        # -------------------------------------------------

        elif intent == "order":

            reply = self.order_response()

        # -------------------------------------------------
        # UNRELATED
        # -------------------------------------------------

        elif intent == "unrelated":

            reply = self.unrelated_response()

        # -------------------------------------------------
        # GEMINI
        # -------------------------------------------------

        else:

            reply = self.gemini_response(
                message
            )

        # -------------------------------------------------
        # SAVE RESPONSE
        # -------------------------------------------------

        self.memory.add(
            "assistant",
            reply
        )

        return reply


# =========================================================
# GLOBAL CHATBOT INSTANCE
# =========================================================

chatbot = VeloraChatbot()