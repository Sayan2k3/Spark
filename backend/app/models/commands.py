from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from enum import Enum

class ActionType(str, Enum):
    NAVIGATE = "navigate"
    SEARCH = "search"
    ADD_TO_CART = "add_to_cart"
    SUMMARIZE = "summarize"
    EXTRACT = "extract"
    SHOW_ORDERS = "show_orders"
    UNKNOWN = "unknown"

class CommandRequest(BaseModel):
    command: str
    context: Optional[Dict[str, Any]] = {}
    session_id: Optional[str] = None

class NavigationTarget(BaseModel):
    page: str
    params: Optional[Dict[str, Any]] = {}

class AgentResponse(BaseModel):
    action: ActionType
    message: str
    navigation: Optional[NavigationTarget] = None
    data: Optional[Dict[str, Any]] = None
    summary: Optional[str] = None
    status: str = "success"
    suggestions: Optional[List[str]] = None

class ExtractRequest(BaseModel):
    page_content: str
    extract_type: str = "general"

class SummarizeRequest(BaseModel):
    content: str
    summary_type: str = "brief"
    max_length: Optional[int] = 150

class ActionRequest(BaseModel):
    action_type: str
    product_id: Optional[str] = None
    quantity: Optional[int] = 1
    context: Optional[Dict[str, Any]] = {}