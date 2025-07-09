"""
Data models for analysis results
"""
from pydantic import BaseModel
from typing import Dict, List, Any, Optional


class FeatureAnalysis(BaseModel):
    """Analysis result for a specific feature"""
    average_rating: float
    mention_count: int
    positive_mentions: int
    negative_mentions: int
    sentiment_score: float
    sample_reviews: List[str]


class ProductComparison(BaseModel):
    """Comparison data for a single product"""
    name: str
    price: float
    specs: Dict[str, Any]
    review_analysis: Dict[str, FeatureAnalysis]


class ComparisonResult(BaseModel):
    """Full comparison result"""
    comparison: Dict[str, ProductComparison]
    summary: str
    recommendation: Dict[str, Any]
    winner_by_criteria: Dict[str, str]


class ProductScore(BaseModel):
    """Scoring for a product recommendation"""
    product: str
    product_id: int
    online_price: float
    score: Dict[str, float]
    overall_score: float
    value_score: float
    store_prices: Optional[List[Dict[str, Any]]] = None


class BestChoice(BaseModel):
    """Best choice recommendation"""
    product: str
    product_id: int
    overall_score: float
    reasons: List[str]
    best_store_deal: Optional[Dict[str, Any]] = None
    savings: float


class StorePrice(BaseModel):
    """Store pricing information"""
    store: str
    store_id: int
    distance: str
    address: str
    price: float
    availability: str
    rating: float
    savings: float
    price_match: bool