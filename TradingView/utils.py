"""
Utility functions for TradingView API
"""

import random
import string
from typing import Optional


def gen_session_id(session_type: str = "xs") -> str:
    """
    Generate a unique session ID
    
    Args:
        session_type: Type of session (e.g., 'cs' for chart session)
        
    Returns:
        Unique session ID string
    """
    # Generate 12 random alphanumeric characters
    chars = string.ascii_letters + string.digits
    random_part = ''.join(random.choice(chars) for _ in range(12))
    return f"{session_type}_{random_part}"


def gen_auth_cookies(session_id: str = "", signature: str = "") -> str:
    """
    Generate authentication cookies string
    
    Args:
        session_id: Session ID
        signature: Session signature
        
    Returns:
        Formatted cookie string
    """
    if not session_id:
        return ""
    if not signature:
        return f"sessionid={session_id}"
    return f"sessionid={session_id};sessionid_sign={signature}" 