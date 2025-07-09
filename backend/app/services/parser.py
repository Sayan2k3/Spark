import re
from typing import Dict, Any, Tuple, List
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
            ],
            ActionType.COMPARE: [
                r"compare (?:the\s+)?(?:phones?|products?|items?) in (?:my\s+)?cart(?:\s+for\s+(.+))?",
                r"which (?:one\s+)?is better(?:\s+for\s+(.+))?",
                r"compare (.+?) (?:and|vs\.?|versus) (.+?)(?:\s+for\s+(.+))?",
                r"what(?:'s| is) the difference between (.+?) and (.+)"
            ],
            ActionType.RECOMMEND: [
                r"(?:find|show|recommend|suggest)\s+(?:me\s+)?(?:the\s+)?best (.+?) under \$?(\d+(?:k)?)",
                r"i have \$?(\d+(?:k)?)\s*(?:budget)?.*?(?:need|want|for)\s+(.+)",
                r"(?:what|which) (?:phone|product) (?:should i|do you recommend).*?(?:under|below|within) \$?(\d+(?:k)?)",
                r"recommend (?:a|me|the best) (.+?) (?:under|below|within) \$?(\d+(?:k)?)"
            ]
        }
        
        # Feature extraction patterns for comparison
        self.feature_patterns = {
            'battery': r'battery|battery life|charge|charging|power',
            'camera': r'camera|photo|picture|selfie|video',
            'storage': r'storage|memory|space|gb',
            'display': r'display|screen|oled|refresh',
            'performance': r'performance|speed|gaming|fast|processor',
            'price': r'price|cost|value|money'
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
            
        elif action_type == ActionType.COMPARE:
            # Extract comparison criteria
            groups = match.groups()
            if groups:
                # Extract features to compare
                features_text = groups[-1] if groups[-1] else ""
                data["criteria"] = self._extract_features(features_text)
                
                # Check if comparing specific products
                if len(groups) >= 2 and groups[0] and groups[1]:
                    data["product1"] = groups[0].strip()
                    data["product2"] = groups[1].strip()
                else:
                    data["use_cart"] = True
                    
        elif action_type == ActionType.RECOMMEND:
            # Extract budget and requirements
            groups = match.groups()
            if len(groups) >= 2:
                # Parse budget
                budget_str = groups[1] if groups[0].isdigit() else groups[0]
                requirements_str = groups[0] if groups[0].isdigit() else groups[1]
                
                data["budget"] = self._parse_budget(budget_str)
                data["priorities"] = self._extract_priorities(requirements_str)
        
        return action_type, data
    
    def _infer_action(self, command: str) -> Tuple[ActionType, Dict[str, Any]]:
        """Infer action from keywords when no pattern matches"""
        
        # Comparison keywords
        if any(word in command for word in ["compare", "versus", "vs", "better", "difference"]):
            criteria = self._extract_features(command)
            return ActionType.COMPARE, {"criteria": criteria, "use_cart": True}
        
        # Recommendation keywords with budget
        budget_match = re.search(r'\$?(\d+(?:k)?)', command)
        if budget_match and any(word in command for word in ["recommend", "suggest", "best", "under", "budget"]):
            budget = self._parse_budget(budget_match.group(1))
            priorities = self._extract_priorities(command)
            return ActionType.RECOMMEND, {"budget": budget, "priorities": priorities}
        
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
    
    def _extract_features(self, text: str) -> List[str]:
        """Extract feature criteria from text"""
        features = []
        text_lower = text.lower()
        
        for feature, pattern in self.feature_patterns.items():
            if re.search(pattern, text_lower):
                features.append(feature)
        
        # Default features if none found
        if not features and text:
            features = ['performance', 'camera', 'battery']
        
        return features
    
    def _extract_priorities(self, text: str) -> List[str]:
        """Extract priority features from text"""
        priorities = []
        text_lower = text.lower()
        
        # Check for specific features mentioned
        feature_mapping = {
            'camera': ['camera', 'photo', 'picture', 'selfie'],
            'storage': ['storage', 'memory', 'space', 'gb'],
            'gaming': ['gaming', 'game', 'pubg', 'cod', 'performance'],
            'battery': ['battery', 'charge', 'power'],
            'display': ['display', 'screen', 'oled']
        }
        
        for feature, keywords in feature_mapping.items():
            if any(keyword in text_lower for keyword in keywords):
                priorities.append(feature)
        
        # Default priorities if none found
        if not priorities:
            priorities = ['performance', 'camera', 'battery']
        
        return priorities[:3]  # Limit to top 3 priorities
    
    def _parse_budget(self, budget_str: str) -> float:
        """Parse budget string to float value"""
        budget_str = budget_str.lower().strip()
        
        # Remove $ symbol
        budget_str = budget_str.replace('$', '')
        
        # Handle 'k' notation (e.g., "30k" -> 30000)
        if 'k' in budget_str:
            try:
                return float(budget_str.replace('k', '')) * 1000
            except:
                return 0
        
        try:
            return float(budget_str)
        except:
            return 0