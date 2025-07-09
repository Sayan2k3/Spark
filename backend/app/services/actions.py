from typing import Dict, Any, List
import random
from .mock_data import get_mock_products

class ActionHandler:
    """Handle various agent actions"""
    
    def __init__(self):
        # Mock data for demo
        self.mock_products = {
            "iphone-13": {
                "name": "iPhone 13",
                "price": 699.99,
                "rating": 4.5,
                "reviews_count": 1250,
                "in_stock": True
            },
            "samsung-tv-55": {
                "name": "Samsung 55\" 4K Smart TV",
                "price": 499.99,
                "rating": 4.3,
                "reviews_count": 856,
                "in_stock": True
            },
            "laptop-dell": {
                "name": "Dell Inspiron 15 Laptop",
                "price": 649.99,
                "rating": 4.2,
                "reviews_count": 432,
                "in_stock": True
            }
        }
        
        self.mock_orders = [
            {
                "order_id": "WM-2024-001",
                "date": "2024-01-15",
                "total": 156.47,
                "items": 3,
                "status": "Delivered"
            },
            {
                "order_id": "WM-2024-002",
                "date": "2024-01-18",
                "total": 89.99,
                "items": 1,
                "status": "Delivered"
            },
            {
                "order_id": "WM-2024-003",
                "date": "2024-01-22",
                "total": 234.56,
                "items": 5,
                "status": "In Transit"
            }
        ]
    
    def add_to_cart(self, product_id: str, quantity: int = 1) -> Dict[str, Any]:
        """Simulate adding item to cart"""
        
        # Mock successful addition
        return {
            "success": True,
            "product_id": product_id,
            "quantity": quantity,
            "cart_total_items": random.randint(1, 5),
            "message": f"Added {quantity} item(s) to your cart"
        }
    
    def get_product_summary(self, product_id: str) -> str:
        """Get a summary of product information"""
        
        # Mock product summaries
        summaries = {
            "iphone-13": "The iPhone 13 features a 6.1-inch display, A15 Bionic chip, and excellent camera system. Users praise its battery life and performance. Most reviews highlight the smooth iOS experience and build quality.",
            "samsung-tv-55": "This Samsung 55-inch 4K TV offers vibrant colors and smart features. Customers appreciate the picture quality and easy setup. The built-in streaming apps and voice control are frequently mentioned positives.",
            "laptop-dell": "The Dell Inspiron 15 is a reliable laptop for everyday use. Reviews mention good performance for the price, comfortable keyboard, and decent battery life. Some users note it's great for students and office work."
        }
        
        return summaries.get(product_id, "This product has received positive reviews from customers. It offers good value for money and reliable performance.")
    
    def get_review_summary(self, product_id: str) -> Dict[str, Any]:
        """Summarize product reviews"""
        
        # Mock review summaries
        positive_aspects = [
            "Great build quality",
            "Excellent value for money",
            "Fast shipping",
            "Works as advertised",
            "Easy to use"
        ]
        
        concerns = [
            "Could be cheaper",
            "Packaging could be better",
            "Instructions could be clearer"
        ]
        
        return {
            "overall_rating": random.uniform(4.0, 4.8),
            "total_reviews": random.randint(100, 2000),
            "summary": f"Customers are generally satisfied with this product. Common praises include: {', '.join(random.sample(positive_aspects, 3))}. Some minor concerns: {random.choice(concerns)}.",
            "recommendation": "87% of customers would recommend this product",
            "key_points": random.sample(positive_aspects, 3)
        }
    
    def get_recent_orders(self, count: int = 10) -> List[Dict[str, Any]]:
        """Get recent orders (mocked)"""
        
        # Return mock orders up to requested count
        return self.mock_orders[:min(count, len(self.mock_orders))]
    
    def search_products(self, query: str) -> List[Dict[str, Any]]:
        """Search for products (mocked)"""
        
        query_lower = query.lower()
        results = []
        
        # Simple keyword matching
        for product_id, product in self.mock_products.items():
            if query_lower in product["name"].lower():
                results.append({
                    "id": product_id,
                    "name": product["name"],
                    "price": product["price"],
                    "rating": product["rating"],
                    "match_score": 0.9
                })
        
        # If no exact matches, return some products anyway (simulating fuzzy search)
        if not results:
            results = [
                {
                    "id": list(self.mock_products.keys())[0],
                    "name": list(self.mock_products.values())[0]["name"],
                    "price": list(self.mock_products.values())[0]["price"],
                    "rating": list(self.mock_products.values())[0]["rating"],
                    "match_score": 0.6
                }
            ]
        
        return results