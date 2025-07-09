"""
Product Comparison Service for comparing multiple products
"""
from typing import Dict, List, Any, Optional
from .analyzer import ReviewAnalyzer


class ProductComparator:
    """Compares products based on specifications and review analysis"""
    
    def __init__(self):
        self.review_analyzer = ReviewAnalyzer()
    
    def compare_products(self, products: List[Dict[str, Any]], criteria: List[str]) -> Dict[str, Any]:
        """
        Compare multiple products based on specified criteria
        
        Args:
            products: List of product dictionaries with specs and reviews
            criteria: List of comparison criteria (e.g., ['battery', 'camera'])
            
        Returns:
            Comparison results with recommendations
        """
        comparison = {}
        
        for product in products:
            product_id = product['id']
            comparison[f"product_{product_id}"] = {
                'name': product['name'],
                'price': product['price'],
                'specs': {},
                'review_analysis': {}
            }
            
            # Extract specifications for each criterion
            for criterion in criteria:
                spec_value = self._extract_spec(product.get('specifications', {}), criterion)
                comparison[f"product_{product_id}"]['specs'][criterion] = spec_value
                
                # Analyze reviews for this criterion
                if 'reviews' in product:
                    review_analysis = self.review_analyzer.analyze_reviews_for_features(
                        product['reviews'], [criterion]
                    )
                    comparison[f"product_{product_id}"]['review_analysis'][criterion] = review_analysis.get(criterion, {})
        
        # Generate comparison summary and recommendation
        summary = self._generate_comparison_summary(comparison, criteria)
        recommendation = self._generate_recommendation(comparison, criteria)
        
        return {
            'comparison': comparison,
            'summary': summary,
            'recommendation': recommendation,
            'winner_by_criteria': self._determine_winners_by_criteria(comparison, criteria)
        }
    
    def _extract_spec(self, specifications: Dict[str, Any], criterion: str) -> Any:
        """Extract specification value for a criterion"""
        spec_mapping = {
            'battery': ['battery_capacity', 'battery', 'battery_mah'],
            'camera': ['main_camera', 'camera', 'rear_camera'],
            'storage': ['storage', 'internal_storage', 'memory'],
            'display': ['display_size', 'screen_size', 'display'],
            'processor': ['processor', 'chipset', 'cpu'],
            'ram': ['ram', 'memory_ram']
        }
        
        possible_keys = spec_mapping.get(criterion, [criterion])
        
        for key in possible_keys:
            if key in specifications:
                return specifications[key]
        
        return "Not specified"
    
    def _generate_comparison_summary(self, comparison: Dict[str, Any], criteria: List[str]) -> str:
        """Generate a human-readable comparison summary"""
        product_names = []
        for key, data in comparison.items():
            if key.startswith('product_'):
                product_names.append(data['name'])
        
        summary_parts = [f"Comparing {' vs '.join(product_names)}:"]
        
        for criterion in criteria:
            criterion_summary = f"\n{criterion.capitalize()}:"
            
            for key, data in comparison.items():
                if key.startswith('product_'):
                    spec = data['specs'].get(criterion, 'N/A')
                    review_data = data['review_analysis'].get(criterion, {})
                    
                    if review_data and review_data.get('mention_count', 0) > 0:
                        rating = review_data['average_rating']
                        criterion_summary += f"\n- {data['name']}: {spec} (User rating: {rating}/5)"
                    else:
                        criterion_summary += f"\n- {data['name']}: {spec}"
            
            summary_parts.append(criterion_summary)
        
        return '\n'.join(summary_parts)
    
    def _generate_recommendation(self, comparison: Dict[str, Any], criteria: List[str]) -> Dict[str, Any]:
        """Generate AI recommendation based on comparison"""
        scores = {}
        
        for key, data in comparison.items():
            if not key.startswith('product_'):
                continue
                
            product_name = data['name']
            total_score = 0
            criteria_scores = {}
            
            for criterion in criteria:
                # Score based on review ratings
                review_data = data['review_analysis'].get(criterion, {})
                if review_data and review_data.get('mention_count', 0) > 0:
                    score = review_data['average_rating'] * 20  # Convert 5-star to 100
                else:
                    score = 60  # Default score if no reviews
                
                # Bonus for better specs (simplified)
                spec = str(data['specs'].get(criterion, ''))
                if criterion == 'battery' and 'mAh' in spec:
                    battery_value = int(re.findall(r'\d+', spec)[0]) if re.findall(r'\d+', spec) else 0
                    if battery_value > 5000:
                        score += 10
                elif criterion == 'camera' and 'MP' in spec:
                    camera_value = int(re.findall(r'\d+', spec)[0]) if re.findall(r'\d+', spec) else 0
                    if camera_value > 100:
                        score += 10
                
                criteria_scores[criterion] = min(score, 100)
                total_score += score
            
            scores[product_name] = {
                'total': total_score / len(criteria),
                'criteria_scores': criteria_scores
            }
        
        # Find the best product
        best_product = max(scores.keys(), key=lambda x: scores[x]['total'])
        
        return {
            'recommended_product': best_product,
            'reason': self._generate_recommendation_reason(best_product, scores, criteria),
            'scores': scores
        }
    
    def _generate_recommendation_reason(self, best_product: str, scores: Dict[str, Any], criteria: List[str]) -> str:
        """Generate explanation for recommendation"""
        best_scores = scores[best_product]['criteria_scores']
        
        strengths = []
        for criterion in criteria:
            if best_scores.get(criterion, 0) >= 80:
                strengths.append(criterion)
        
        reason = f"{best_product} is recommended because it "
        
        if len(strengths) > 1:
            reason += f"excels in {', '.join(strengths[:-1])} and {strengths[-1]}"
        elif strengths:
            reason += f"excels in {strengths[0]}"
        else:
            reason += "offers the best overall balance"
        
        reason += f" with an overall score of {scores[best_product]['total']:.1f}/100."
        
        return reason
    
    def _determine_winners_by_criteria(self, comparison: Dict[str, Any], criteria: List[str]) -> Dict[str, str]:
        """Determine which product wins for each criterion"""
        winners = {}
        
        for criterion in criteria:
            best_product = None
            best_score = 0
            
            for key, data in comparison.items():
                if not key.startswith('product_'):
                    continue
                
                review_data = data['review_analysis'].get(criterion, {})
                if review_data and review_data.get('average_rating', 0) > best_score:
                    best_score = review_data['average_rating']
                    best_product = data['name']
            
            if best_product:
                winners[criterion] = best_product
            else:
                winners[criterion] = "Tie"
        
        return winners


import re