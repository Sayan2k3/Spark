import re
from typing import Dict, Any, Tuple
from app.models import ActionType

class CommandParser:
    """Parse natural language commands into structured actions"""
    
    def __init__(self):
        self.patterns = {
            ActionType.SEARCH: [
                r"(?:get|show|find|search|look for)\s+(?:me\s+)?(.+?)(?:\s+for me)?$",
                r"(?:i want|i need|looking for)\s+(.+)$",
                r"^(.+?)\s+(?:please|pls)?$"
            ],
            ActionType.ADD_TO_CART: [
                r"add (?:it|this|that) to (?:my\s+)?cart",
                r"(?:put|place) (?:it|this|that) in (?:my\s+)?cart",
                r"cart (?:it|this|that)",
                r"buy (?:it|this|that)"
            ],
            ActionType.SUMMARIZE: [
                r"(?:summarize|summary of)\s+(?:the\s+)?reviews?",
                r"what do (?:the\s+)?reviews? say",
                r"tell me about (?:the\s+)?reviews?",
                r"(?:summarize|summary|describe)\s+(?:this|the)\s+(?:product|item)"
            ],
            ActionType.SHOW_ORDERS: [
                r"(?:show|get|display)\s+(?:me\s+)?(?:my\s+)?(?:last|recent)?\s*(\d*)\s*orders?",
                r"(?:my\s+)?order history",
                r"what did i (?:order|buy)",
                r"(?:take me to|show)\s+(?:my\s+)?orders?"
            ],
            ActionType.NAVIGATE: [
                r"(?:go to|take me to|navigate to)\s+(.+)",
                r"(?:open|show)\s+(.+)\s+page"
            ]
        }
    
    def parse_command(self, command: str) -> Tuple[ActionType, Dict[str, Any]]:
        """Parse a command and return the action type and extracted data"""
        command_lower = command.lower().strip()
        
        # Check each pattern type
        for action_type, patterns in self.patterns.items():
            for pattern in patterns:
                match = re.match(pattern, command_lower, re.IGNORECASE)
                if match:
                    return self._extract_action_data(action_type, match, command_lower)
        
        # If no pattern matches, try to infer from keywords
        return self._infer_action(command_lower)
    
    def _extract_action_data(self, action_type: ActionType, match: re.Match, command: str) -> Tuple[ActionType, Dict[str, Any]]:
        """Extract relevant data based on action type"""
        data = {}
        
        if action_type == ActionType.SEARCH and match.groups():
            # Extract search query
            query = match.group(1).strip()
            data["query"] = query
            data["original_query"] = query
            
        elif action_type == ActionType.SHOW_ORDERS and match.groups():
            # Extract number of orders if specified
            order_count = match.group(1) if len(match.groups()) > 0 and match.group(1) else "10"
            try:
                data["count"] = int(order_count) if order_count else 10
            except:
                data["count"] = 10
                
        elif action_type == ActionType.NAVIGATE and match.groups():
            # Extract navigation target
            target = match.group(1).strip()
            data["target"] = target
        
        return action_type, data
    
    def _infer_action(self, command: str) -> Tuple[ActionType, Dict[str, Any]]:
        """Infer action from keywords when no pattern matches"""
        
        # Product-specific keywords suggest search
        product_keywords = ["phone", "laptop", "tv", "iphone", "samsung", "electronics", 
                          "groceries", "clothing", "shoes", "toys"]
        for keyword in product_keywords:
            if keyword in command:
                return ActionType.SEARCH, {"query": command}
        
        # Cart-related keywords
        if any(word in command for word in ["cart", "buy", "purchase", "checkout"]):
            return ActionType.ADD_TO_CART, {}
        
        # Review/summary keywords
        if any(word in command for word in ["review", "rating", "summary", "describe"]):
            return ActionType.SUMMARIZE, {}
        
        # Order-related keywords
        if any(word in command for word in ["order", "history", "bought", "purchased"]):
            return ActionType.SHOW_ORDERS, {"count": 10}
        
        # Default to search if command seems like a product query
        if len(command.split()) <= 3:
            return ActionType.SEARCH, {"query": command}
        
        return ActionType.UNKNOWN, {"original_command": command}