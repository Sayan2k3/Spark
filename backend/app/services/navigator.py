from typing import Dict, Any, Optional
from app.models import NavigationTarget, ActionType

class Navigator:
    """Handle navigation logic and page routing"""
    
    def __init__(self):
        self.page_mappings = {
            "home": "index.html",
            "products": "products.html",
            "product": "product.html",
            "cart": "cart.html",
            "orders": "orders.html",
            "account": "account.html",
            "search": "products.html"
        }
    
    def get_navigation_target(self, action: ActionType, data: Dict[str, Any]) -> Optional[NavigationTarget]:
        """Determine where to navigate based on action"""
        
        if action == ActionType.SEARCH:
            return NavigationTarget(
                page="products.html",
                params={
                    "search": data.get("query", ""),
                    "aiMode": True
                }
            )
        
        elif action == ActionType.SHOW_ORDERS:
            return NavigationTarget(
                page="orders.html",
                params={
                    "count": data.get("count", 10),
                    "aiMode": True
                }
            )
        
        elif action == ActionType.NAVIGATE:
            target = data.get("target", "").lower()
            
            # Map common navigation targets
            if "cart" in target:
                return NavigationTarget(page="cart.html")
            elif "order" in target:
                return NavigationTarget(page="orders.html")
            elif "product" in target:
                return NavigationTarget(page="products.html")
            elif "home" in target or "main" in target:
                return NavigationTarget(page="index.html")
            elif "account" in target or "profile" in target:
                return NavigationTarget(page="account.html")
            
            # Default to products page for unknown targets
            return NavigationTarget(
                page="products.html",
                params={"search": target}
            )
        
        # No navigation needed for other actions
        return None
    
    def get_breadcrumb(self, page: str) -> str:
        """Get breadcrumb for current page"""
        breadcrumbs = {
            "index.html": "Home",
            "products.html": "Home > Products",
            "product.html": "Home > Products > Product Details",
            "cart.html": "Home > Cart",
            "orders.html": "Home > My Orders",
            "account.html": "Home > My Account"
        }
        return breadcrumbs.get(page, "Home")