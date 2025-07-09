"""
Product Recommendation Service for budget-based recommendations
"""
from typing import Dict, List, Any, Optional
from .analyzer import ReviewAnalyzer
from .store_locator import StoreLocator


class ProductRecommender:
    """Recommends products based on budget and requirements"""
    
    def __init__(self):
        self.review_analyzer = ReviewAnalyzer()
        self.store_locator = StoreLocator()
    
    def get_budget_recommendations(
        self, 
        products: List[Dict[str, Any]], 
        budget: float, 
        priorities: List[str],
        include_stores: bool = True
    ) -> Dict[str, Any]:
        """
        Get product recommendations within budget
        
        Args:
            products: List of all available products
            budget: Maximum budget
            priorities: List of priority features (e.g., ['camera', 'storage', 'gaming'])
            include_stores: Whether to include nearby store prices
            
        Returns:
            Recommendations with scores and store prices
        """
        # Filter products within budget
        eligible_products = [p for p in products if p['price'] <= budget]
        
        if not eligible_products:
            return {
                'recommendations': [],
                'message': f"No products found within budget of ${budget}",
                'best_choice': None
            }
        
        # Score each product based on priorities
        scored_products = []
        
        for product in eligible_products:
            scores = self._calculate_product_scores(product, priorities)
            overall_score = sum(scores.values()) / len(scores) if scores else 0
            
            product_recommendation = {
                'product': product['name'],
                'product_id': product['id'],
                'online_price': product['price'],
                'score': scores,
                'overall_score': round(overall_score, 1),
                'value_score': self._calculate_value_score(overall_score, product['price'], budget)
            }
            
            # Add store prices if requested
            if include_stores:
                product_recommendation['store_prices'] = self.store_locator.get_nearby_stores_with_prices(
                    product['id'], 
                    product['price']
                )
            
            scored_products.append(product_recommendation)
        
        # Sort by overall score
        scored_products.sort(key=lambda x: x['overall_score'], reverse=True)
        
        # Get top 3 recommendations
        top_recommendations = scored_products[:3]
        
        # Determine best choice considering both score and value
        best_choice = self._determine_best_choice(top_recommendations, priorities)
        
        return {
            'recommendations': top_recommendations,
            'best_choice': best_choice,
            'priorities_analyzed': priorities,
            'budget': budget
        }
    
    def _calculate_product_scores(self, product: Dict[str, Any], priorities: List[str]) -> Dict[str, float]:
        """Calculate scores for each priority feature"""
        scores = {}
        
        # Map priorities to scoring functions
        scoring_functions = {
            'camera': self._score_camera,
            'storage': self._score_storage,
            'gaming': self._score_gaming,
            'battery': self._score_battery,
            'display': self._score_display,
            'performance': self._score_performance
        }
        
        for priority in priorities:
            if priority in scoring_functions:
                score = scoring_functions[priority](product)
                scores[priority] = score
            else:
                # Default scoring based on reviews if available
                scores[priority] = self._score_from_reviews(product, priority)
        
        return scores
    
    def _score_camera(self, product: Dict[str, Any]) -> float:
        """Score camera quality (0-100)"""
        score = 50  # Base score
        
        specs = product.get('specifications', {})
        camera_spec = specs.get('main_camera', '')
        
        # Extract megapixels
        import re
        mp_match = re.search(r'(\d+)\s*MP', camera_spec, re.IGNORECASE)
        if mp_match:
            megapixels = int(mp_match.group(1))
            if megapixels >= 108:
                score = 95
            elif megapixels >= 64:
                score = 85
            elif megapixels >= 48:
                score = 75
            elif megapixels >= 12:
                score = 65
        
        # Adjust based on reviews if available
        if 'reviews' in product:
            review_score = self._get_review_score_for_feature(product['reviews'], 'camera')
            if review_score > 0:
                score = (score + review_score * 20) / 2
        
        return min(score, 100)
    
    def _score_storage(self, product: Dict[str, Any]) -> float:
        """Score storage capacity (0-100)"""
        score = 50
        
        specs = product.get('specifications', {})
        storage_spec = specs.get('storage', '')
        
        # Extract GB
        gb_match = re.search(r'(\d+)\s*GB', storage_spec, re.IGNORECASE)
        if gb_match:
            gb = int(gb_match.group(1))
            if gb >= 512:
                score = 95
            elif gb >= 256:
                score = 85
            elif gb >= 128:
                score = 70
            elif gb >= 64:
                score = 55
        
        return min(score, 100)
    
    def _score_gaming(self, product: Dict[str, Any]) -> float:
        """Score gaming performance (0-100)"""
        score = 50
        
        specs = product.get('specifications', {})
        
        # Check processor
        processor = specs.get('processor', '').lower()
        if 'snapdragon 8' in processor or 'a17' in processor or 'a16' in processor:
            score = 90
        elif 'snapdragon 7' in processor or 'a15' in processor:
            score = 75
        elif 'snapdragon 6' in processor or 'a14' in processor:
            score = 60
        
        # Check RAM
        ram_spec = specs.get('ram', '')
        ram_match = re.search(r'(\d+)\s*GB', ram_spec, re.IGNORECASE)
        if ram_match:
            ram_gb = int(ram_match.group(1))
            if ram_gb >= 12:
                score += 10
            elif ram_gb >= 8:
                score += 5
        
        # Check refresh rate
        display = specs.get('display', '').lower()
        if '120hz' in display or '144hz' in display:
            score += 5
        
        return min(score, 100)
    
    def _score_battery(self, product: Dict[str, Any]) -> float:
        """Score battery life (0-100)"""
        score = 50
        
        specs = product.get('specifications', {})
        battery_spec = specs.get('battery', '')
        
        # Extract mAh
        mah_match = re.search(r'(\d+)\s*mAh', battery_spec, re.IGNORECASE)
        if mah_match:
            mah = int(mah_match.group(1))
            if mah >= 5000:
                score = 90
            elif mah >= 4500:
                score = 80
            elif mah >= 4000:
                score = 70
            elif mah >= 3500:
                score = 60
        
        return min(score, 100)
    
    def _score_display(self, product: Dict[str, Any]) -> float:
        """Score display quality (0-100)"""
        score = 60
        
        specs = product.get('specifications', {})
        display = specs.get('display', '').lower()
        
        if 'amoled' in display or 'oled' in display:
            score += 20
        if '120hz' in display or '144hz' in display:
            score += 15
        if '1080p' in display or 'fhd' in display:
            score += 5
        elif '1440p' in display or 'qhd' in display:
            score += 10
        
        return min(score, 100)
    
    def _score_performance(self, product: Dict[str, Any]) -> float:
        """Score overall performance (0-100)"""
        # Similar to gaming but more general
        return self._score_gaming(product) * 0.9
    
    def _score_from_reviews(self, product: Dict[str, Any], feature: str) -> float:
        """Generic scoring based on reviews"""
        if 'reviews' not in product:
            return 60  # Default middle score
        
        score = self._get_review_score_for_feature(product['reviews'], feature)
        return score * 20  # Convert 5-star to 100
    
    def _get_review_score_for_feature(self, reviews: List[Dict[str, Any]], feature: str) -> float:
        """Get average review score for a specific feature"""
        analysis = self.review_analyzer.analyze_reviews_for_features(reviews, [feature])
        feature_data = analysis.get(feature, {})
        return feature_data.get('average_rating', 3.0)
    
    def _calculate_value_score(self, overall_score: float, price: float, budget: float) -> float:
        """Calculate value for money score"""
        # Higher score for products that deliver good performance at lower price
        price_ratio = price / budget
        value_score = overall_score * (1 - price_ratio * 0.3)
        return round(value_score, 1)
    
    def _determine_best_choice(self, recommendations: List[Dict[str, Any]], priorities: List[str]) -> Dict[str, Any]:
        """Determine the best overall choice"""
        if not recommendations:
            return None
        
        # Weight overall score and value score
        best_product = None
        best_combined_score = 0
        
        for rec in recommendations:
            combined_score = rec['overall_score'] * 0.7 + rec['value_score'] * 0.3
            if combined_score > best_combined_score:
                best_combined_score = combined_score
                best_product = rec
        
        if best_product:
            # Generate reasoning
            reasons = []
            
            # Check which priorities it excels in
            for priority in priorities:
                if priority in best_product['score'] and best_product['score'][priority] >= 80:
                    reasons.append(f"excellent {priority}")
            
            # Add value proposition
            if best_product['value_score'] >= 70:
                reasons.append("great value for money")
            
            # Find best store deal if available
            best_store_deal = None
            if 'store_prices' in best_product and best_product['store_prices']:
                best_store_deal = min(best_product['store_prices'], key=lambda x: x['price'])
            
            return {
                'product': best_product['product'],
                'product_id': best_product['product_id'],
                'overall_score': best_product['overall_score'],
                'reasons': reasons,
                'best_store_deal': best_store_deal,
                'savings': best_product['online_price'] - best_store_deal['price'] if best_store_deal else 0
            }
        
        return None


import re