"""
TradingView Symbol Search API
Provides functionality to search for symbols on TradingView
"""

import requests
import json
import time
import re
from typing import Optional, List, Dict, Any


def clean_text(text: str) -> str:
    """
    Clean text by removing HTML tags, converting to uppercase, and replacing special characters.
    
    Args:
        text (str): Text to clean
    
    Returns:
        str: Cleaned text                   
    """
    return re.sub(r'<[^>]+>', '', text or '').upper().replace('&', '_').replace(' ', '_')


class SymbolSearch:
    """
    TradingView Symbol Search client
    """
    
    def __init__(self, retries: int = 3):
        """
        Initialize SymbolSearch client
        
        Args:
            retries (int): Number of retry attempts for failed requests
        """
        self.retries = retries
    
    def search(self, symbol: str, exchange: str = None, country: str = None) -> Optional[List[Dict[str, Any]]]:
        """
        Search for symbols on TradingView using symbol search API.
        
        Args:
            symbol (str): The symbol to search for (e.g., "NIFTY")
            exchange (str, optional): The exchange to search for (e.g., "NSE")
            country (str, optional): Country code for filtering results (e.g., "IN" for India)
        
        Returns:
            Optional[List[Dict[str, Any]]]: List of symbols with filtered fields or None if request fails
        """
        url = "https://symbol-search.tradingview.com/symbol_search/v3/"
        
        # Clean input parameters
        symbol = clean_text(symbol)
        if exchange:
            exchange = clean_text(exchange)
        if country:
            country = clean_text(country)
        
        params = {
            "text": symbol,
            "hl": "1",
            "search_type": "undefined",
            "domain": "production",
            "promo": "true"
        }
        
        # Add optional parameters only if they are provided
        if exchange:
            params["exchange"] = exchange
        if country:
            params["country"] = country
        
        # Headers to mimic a browser request
        headers = {
            "Origin": "https://www.tradingview.com"
        }
        
        # Retry logic
        for attempt in range(self.retries):
            try:
                response = requests.get(url, params=params, headers=headers, timeout=10)
                response.raise_for_status()
                
                data = response.json()
                
                # Extract only the symbols field and filter each object
                if 'symbols' in data:
                    filtered_symbols = []
                    for symbol_obj in data['symbols']:
                        filtered_symbol = {
                            'symbol': clean_text(symbol_obj.get('symbol', '')),
                            'description': clean_text(symbol_obj.get('description', '')),
                            'type': symbol_obj.get('type', ''),
                            'exchange': clean_text(symbol_obj.get('exchange', '')),
                            'currency_code': symbol_obj.get('currency_code', ''),
                            'country': clean_text(symbol_obj.get('country', ''))
                        }
                        filtered_symbols.append(filtered_symbol)
                    return filtered_symbols
                else:
                    return []
            
            except requests.exceptions.RequestException as e:
                print(f"Attempt {attempt + 1}/{self.retries} failed: {e}")
                
                # If this is the last attempt, return None
                if attempt == self.retries - 1:
                    print(f"All {self.retries} attempts failed. Giving up.")
                    return None
                
                # Wait before retrying (exponential backoff)
                wait_time = 2 ** attempt  # 1s, 2s, 4s
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON response: {e}")
                return None 