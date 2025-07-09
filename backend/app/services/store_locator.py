"""
Store Locator Service for finding nearby stores and prices
"""
from typing import Dict, List, Any
import random


class StoreLocator:
    """Mock service for locating nearby stores with product prices"""
    
    def __init__(self):
        # Mock store data
        self.stores = [
            {
                'id': 1,
                'name': 'TechZone Express',
                'address': '123 Main Street, Downtown',
                'distance': '2.1 km',
                'rating': 4.5,
                'price_modifier': 0.95  # 5% cheaper than online
            },
            {
                'id': 2,
                'name': 'MobileHub Plus',
                'address': '456 Park Avenue, Westside',
                'distance': '3.5 km',
                'rating': 4.2,
                'price_modifier': 1.02  # 2% more expensive
            },
            {
                'id': 3,
                'name': 'SmartStore Central',
                'address': '789 Tech Boulevard, North Point',
                'distance': '5.8 km',
                'rating': 4.7,
                'price_modifier': 0.98  # 2% cheaper
            },
            {
                'id': 4,
                'name': 'Digital Dreams',
                'address': '321 Innovation Drive, Tech Park',
                'distance': '7.2 km',
                'rating': 4.3,
                'price_modifier': 1.05  # 5% more expensive
            }
        ]
    
    def get_nearby_stores_with_prices(self, product_id: int, online_price: float, limit: int = 3) -> List[Dict[str, Any]]:
        """
        Get nearby stores with their prices for a product
        
        Args:
            product_id: ID of the product
            online_price: Online price of the product
            limit: Maximum number of stores to return
            
        Returns:
            List of stores with prices and availability
        """
        # Randomly select stores (simulating availability)
        available_stores = random.sample(self.stores, min(limit, len(self.stores)))
        
        store_prices = []
        
        for store in available_stores:
            # Calculate store price with some randomization
            base_modifier = store['price_modifier']
            # Add some random variation (-2% to +2%)
            random_variation = random.uniform(-0.02, 0.02)
            final_modifier = base_modifier + random_variation
            
            store_price = round(online_price * final_modifier, 2)
            
            # Determine availability
            availability = self._generate_availability()
            
            store_prices.append({
                'store': store['name'],
                'store_id': store['id'],
                'distance': store['distance'],
                'address': store['address'],
                'price': store_price,
                'availability': availability,
                'rating': store['rating'],
                'savings': round(online_price - store_price, 2),
                'price_match': store_price < online_price
            })
        
        # Sort by price
        store_prices.sort(key=lambda x: x['price'])
        
        return store_prices
    
    def _generate_availability(self) -> str:
        """Generate random availability status"""
        availability_options = [
            'In Stock',
            'In Stock',
            'In Stock',  # Make "In Stock" more common
            'Limited Stock',
            'Display Unit Available',
            'Available for Order'
        ]
        return random.choice(availability_options)
    
    def get_store_details(self, store_id: int) -> Dict[str, Any]:
        """Get detailed information about a specific store"""
        store = next((s for s in self.stores if s['id'] == store_id), None)
        
        if not store:
            return None
        
        return {
            'id': store['id'],
            'name': store['name'],
            'address': store['address'],
            'distance': store['distance'],
            'rating': store['rating'],
            'hours': 'Mon-Sat: 10:00 AM - 9:00 PM, Sun: 11:00 AM - 7:00 PM',
            'phone': f'+1-555-{random.randint(1000, 9999):04d}',
            'services': ['Price Match', 'Extended Warranty', 'Free Setup', 'Trade-In'],
            'payment_options': ['Cash', 'Credit/Debit', 'EMI Available', 'Digital Wallets']
        }
    
    def calculate_best_deal(self, product_id: int, online_price: float) -> Dict[str, Any]:
        """Calculate the best overall deal considering price and distance"""
        stores = self.get_nearby_stores_with_prices(product_id, online_price, limit=4)
        
        if not stores:
            return {
                'best_deal': None,
                'reason': 'No nearby stores available'
            }
        
        # Score each store based on price and distance
        for store in stores:
            # Extract distance value (assuming format like "2.1 km")
            distance_value = float(store['distance'].split()[0])
            
            # Calculate score (lower is better)
            # Weight: 70% price, 30% distance
            price_score = store['price'] / online_price
            distance_score = distance_value / 10  # Normalize to 0-1 range
            
            store['deal_score'] = (price_score * 0.7) + (distance_score * 0.3)
        
        # Find best deal
        best_store = min(stores, key=lambda x: x['deal_score'])
        
        return {
            'best_deal': best_store,
            'reason': self._generate_deal_reason(best_store, online_price),
            'all_stores': stores
        }
    
    def _generate_deal_reason(self, store: Dict[str, Any], online_price: float) -> str:
        """Generate explanation for why this is the best deal"""
        if store['savings'] > 0:
            return f"Save ${store['savings']:.2f} at {store['store']} ({store['distance']} away)"
        elif store['price'] == online_price:
            return f"Same price as online but available immediately at {store['store']} ({store['distance']} away)"
        else:
            return f"{store['store']} is closest ({store['distance']}) with {store['availability'].lower()}"