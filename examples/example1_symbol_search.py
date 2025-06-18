#!/usr/bin/env python3
"""
Example 1: Symbol Search
Demonstrates how to search for trading symbols using the TradingView API.
"""

from TradingView import SymbolSearch

def main():
    print("=== Example 1: Symbol Search ===")
    
    # Create search client
    search = SymbolSearch()
    
    # Search for Apple stock
    print("\n1. Searching for 'AAPL':")
    results = search.search("AAPL")
    for result in results[:3]:  # Show first 3 results
        print(f"  - {result['symbol']}: {result['description']} ({result['exchange']})")
    
    # Search for Bitcoin
    print("\n2. Searching for 'BTC':")
    results = search.search("BTC")
    for result in results[:3]:  # Show first 3 results
        print(f"  - {result['symbol']}: {result['description']} ({result['exchange']})")
    
    # Search for Tesla
    print("\n3. Searching for 'TSLA':")
    results = search.search("TSLA")
    for result in results[:3]:  # Show first 3 results
        print(f"  - {result['symbol']}: {result['description']} ({result['exchange']})")
    
    print("\n✅ Symbol search examples completed!")

if __name__ == "__main__":
    main() 