👗 Velora Style 14 — AI-Powered Fashion Website

A modern fashion-brand website with an integrated AI stylist that helps customers discover products and choose outfits based on their style, occasion, budget, and preferences.

6
🌐 Live Website

Velora Style 14:
Open the live website

GitHub Repository:
View the source code on GitHub

✨ Overview

Velora Style 14 is a fashion-focused web application designed to provide a premium online shopping and styling experience.

The website combines a modern fashion storefront with an AI-powered personal stylist, allowing visitors to browse collections, discover new arrivals, explore trends, filter products by mood or occasion, and interact with Velora AI for personalized fashion recommendations.

The project is built with Python, Flask, JavaScript, HTML, CSS, and Google Gemini AI, and is deployed using Vercel.

The goal is to create a fashion platform where customers don't just browse products—they can also ask an AI stylist for help deciding what to wear, what matches, what fits an occasion, and what works within their budget.

🎯 Key Features
🛍️ Fashion Storefront
Premium fashion-brand homepage
Hero section
New Arrivals
Trending collection
Shop by Mood
Product cards
Product detail modal
Product filtering
Responsive navigation
Search functionality
🤖 Velora AI Stylist

The website includes an AI-powered fashion assistant capable of helping customers with:

Outfit recommendations
Occasion-based styling
Casual outfit suggestions
Party outfit suggestions
Office outfit suggestions
Vacation styling
Budget-based recommendations
Product discovery
Size-related questions
Fashion and styling advice
Catalog-related questions

Example:

User:
I need a party outfit under ₹2000

Velora AI:
Black Satin Midi Dress — ₹1,499
Perfect for parties and evening outings.

The AI uses the available Velora product catalog rather than inventing products.

🔎 Product Search

Users can search the available catalog by:

Product name
Category
Occasion
Color
Description
🆕 New Arrivals

The website provides a dedicated New Arrivals section using products from the current catalog.

🔥 Trending

The Trending section highlights selected products from the available collection.

🎭 Shop by Mood

Customers can explore products based on different fashion moods:

Party Girl
Casual Chic
Work Edit
Vacation Mode
📱 Responsive Design

The website is designed to work across:

Desktop
Laptop
Tablet
Mobile
📩 Instagram Ordering

The current version uses Instagram as the primary ordering/contact channel.

Customers can select a product and continue the purchase conversation through the Velora Instagram account.

Instagram:

@velora_style14

🧠 AI Architecture

The AI system follows a hybrid approach.

Instead of sending every customer message directly to Gemini, the application first checks whether the request can be handled using the local Velora product catalog and predefined logic.

Request flow
Customer
   │
   ▼
Website Chat Interface
   │
   ▼
Flask /chat API
   │
   ▼
Velora AI Chatbot
   │
   ├── Intent Detection
   │
   ├── Product Catalog Search
   │
   ├── Context / Chat Memory
   │
   ├── Predefined Fashion Responses
   │
   └── Gemini AI
   │
   ▼
Personalized Response
   │
   ▼
Customer

This approach helps keep product recommendations grounded in the actual Velora catalog.

🛠️ Technology Stack
Technology	Purpose
Python	Backend programming
Flask	Web framework and API
Google Gemini	AI-powered fashion assistant
HTML5	Website structure
CSS3	Styling and responsive design
JavaScript	Frontend interactions
JSON	Product, FAQ and configuration data
Git	Version control
GitHub	Source-code hosting
Vercel	Cloud deployment
📁 Project Structure
Velora/
│
├── api/
│   ├── __init__.py
│   ├── index.py
│   ├── chatbot.py
│   ├── helpers.py
│   ├── products.py
│   └── test.py
│
├── config/
│   ├── constants.py
│   └── prompt.py
│
├── data/
│   ├── faq.json
│   ├── products.json
│   └── settings.json
│
├── static/
│   ├── css/
│   │   ├── style.css
│   │   ├── animations.css
│   │   └── responsive.css
│   │
│   ├── js/
│   │   ├── script.js
│   │   ├── chat.js
│   │   └── ui.js
│   │
│   ├── images/
│   │   ├── black_satin.jpg
│   │   ├── pink_floral.jpg
│   │   ├── white_shirt.jpg
│   │   ├── blue_jeans.jpg
│   │   └── beige_coord.jpg
│   │
│   ├── fonts/
│   ├── icons/
│   ├── sounds/
│   └── videos/
│
├── templates/
│   ├── components/
│   ├── layouts/
│   └── index.html
│
├── uploads/
│
├── .env
├── .gitignore
├── requirements.txt
├── README.md
└── vercel.json
🛒 Current Product Catalog

The current prototype catalog contains five products:

Product	Category	Price	Occasion
Black Satin Midi Dress	Dress	₹1,499	Party
Pink Floral Maxi Dress	Dress	₹1,699	Vacation
Oversized White Shirt	Top	₹899	Casual
Blue High Waist Jeans	Jeans	₹1,299	Casual
Beige Co-ord Set	Co-ord Set	₹1,999	Office

Product information is stored in:

data/products.json

This makes the catalog easy to update without changing the core application architecture.

⚙️ Backend

The Flask backend provides the main application and AI endpoint.

Main routes
GET /

Loads the main Velora website.

POST /chat

Receives a customer message and returns an AI response.

Example request:

{
  "message": "I need an office outfit"
}

Example response:

{
  "success": true,
  "response": "For an office look, I recommend the Beige Co-ord Set..."
}
GET /health

Returns application health information.

Example:

{
  "status": "running",
  "service": "Velora AI",
  "version": "2.0"
}
🤖 Gemini Integration

Velora AI uses Google's Gemini model for general fashion conversations and styling assistance.

The application currently uses:

gemini-2.5-flash

The API key is loaded through an environment variable:

GEMINI_API_KEY
🔐 Security

Never commit the Gemini API key to GitHub.

For local development, create:

.env

and add:

GEMINI_API_KEY=your_api_key_here

The .env file is excluded from Git using .gitignore.

For production, the API key should be stored in the deployment platform's environment variables.

🚀 Local Development
1. Clone the repository
git clone https://github.com/Imdpkk/Velora.git

Move into the project:

cd Velora
2. Create a virtual environment
Windows
python -m venv venv

Activate it:

venv\Scripts\activate
macOS / Linux
python3 -m venv venv
source venv/bin/activate
3. Install dependencies
pip install -r requirements.txt
4. Configure environment variables

Create a .env file in the project root:

GEMINI_API_KEY=your_api_key_here
5. Start the Flask application

From the project root:

python -m api.index

The application will be available at:

http://127.0.0.1:5000
🧪 Testing

The project contains testing utilities under:

api/test.py

The main functionality that should be tested includes:

Homepage loading
Product rendering
Product search
Product filtering
AI chat
Outfit recommendations
Budget-based recommendations
Size conversations
New Arrivals
Trending products
Health endpoint
Responsive interface

Example AI queries:

Show me your new arrivals
I need a party outfit under ₹2000
I need something casual
What do you have for office?
Help me choose a size
☁️ Deployment

The application is deployed on Vercel.

Deployment architecture:

GitHub
   │
   ▼
Vercel
   │
   ▼
Flask Application
   │
   ├── Website
   ├── Product Catalog
   └── AI Chat API
          │
          ▼
       Gemini AI

The GitHub repository is connected to Vercel, allowing new commits pushed to the main branch to trigger deployments.

Production URL

Velora Style 14 — Live Website

🔄 Updating Products

Product information can be updated in:

data/products.json

A product follows this structure:

{
  "id": 1,
  "name": "Product Name",
  "category": "Dress",
  "price": 1499,
  "sizes": ["S", "M", "L"],
  "colors": ["Black"],
  "occasion": "Party",
  "stock": true,
  "image": "product.jpg",
  "description": "Product description."
}

After changing product data:

git add .
git commit -m "Update product catalog"
git push origin main

Vercel can then deploy the updated version.

🎨 Design Philosophy

Velora follows a premium minimalist fashion aesthetic.

The interface focuses on:

Clean typography
Neutral colors
Large editorial imagery
Generous whitespace
Minimal visual clutter
Responsive layouts
Fashion-oriented interactions
Simple navigation
Premium brand presentation

The design intentionally avoids making the AI assistant feel like a generic chatbot.

🔮 Future Roadmap

The current version is an initial production-ready foundation. Future improvements may include:

🛍️ E-commerce
 Shopping cart
 Wishlist persistence
 Checkout
 Online payments
 Order management
 Order tracking
👤 Customer Accounts
 Email authentication
 Google login
 OTP authentication
 Customer profiles
 Saved sizes
 Order history
🤖 AI Improvements
 Personalized style profiles
 Image-based fashion recommendations
 AI outfit visualization
 More advanced product matching
 Conversation persistence
 Personalized recommendations based on previous interactions
📦 Product Management
 Admin dashboard
 Add/edit/delete products
 Inventory management
 Product image management
 Dynamic collections
 Automated new-arrival updates
📊 Business & Analytics
 Customer analytics
 Product performance analytics
 AI conversation analytics
 Conversion tracking
 Google Analytics / equivalent analytics
🌐 Brand Infrastructure
 Custom domain
 SEO optimization
 Open Graph/social sharing
 Sitemap
 Structured product metadata
 Performance optimization
🔐 Security Considerations

The project follows basic security practices:

API keys are stored using environment variables
.env is excluded from Git
Virtual environments are excluded from Git
Python cache files are excluded
Backend validates incoming chat requests
Frontend user-generated content is escaped before rendering

Production deployments should additionally consider:

Rate limiting
Authentication for administrative functions
Secure payment processing
Database security
Input validation
Monitoring and logging
API abuse protection
📌 Project Status

Current Version: 2.0

Status: 🟢 Live / Active Development

Velora is currently operating as a fashion-brand website with an AI styling assistant and product discovery experience.

The product catalog, branding, ordering workflow, and e-commerce capabilities will continue to evolve as the brand grows.

👨‍💻 Author

Deepak Vishwakarma

GitHub:
@Imdpkk

Project:
Velora Style 14

📄 License

This project is currently maintained as a private brand/application project for Velora Style 14.

Unless otherwise specified, the source code, branding, product information, images, and other project assets should not be reused commercially without permission.

⭐ Velora Style 14

Fashion. Style. Intelligence.

Your style, thoughtfully curated.
